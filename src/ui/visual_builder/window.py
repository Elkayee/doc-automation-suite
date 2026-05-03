import html
import re
import sys
from pathlib import Path

import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

from src.core.assembler import DocumentAssembler
from src.core.chapter_settings import ChapterSettings
from src.core.docx_builder import DocxBuilder
from src.core.markdown_utils import MarkdownUtils
from src.ui.preview_utils import PreviewUtils


class VisualBuilderWindow(tk.Toplevel):
    PREVIEW_DEBOUNCE_MS = 800
    AUTOSAVE_DEBOUNCE_MS = 800
    HIGHLIGHT_DEBOUNCE_MS = 120
    WATCH_INTERVAL_MS = 1500

    TOP_LEVEL_RE = re.compile(r'^Ch(?P<chapter>\d{2})_(?!S\d{2}_)(?P<slug>.+)\.md$')
    SUBCHAPTER_RE = re.compile(r'^Ch(?P<chapter>\d{2})_S(?P<subchapter>\d{2})_(?P<slug>.+)\.md$')
    FRONTMATTER_RE = re.compile(r'^F(?P<index>\d{2})_(?P<slug>.+)\.md$')

    def __init__(self, master, project_path: Path):
        super().__init__(master)
        self.project_path = Path(project_path)
        self.assembler = DocumentAssembler(self.project_path)
        self.current_file: Path | None = None
        self.chapter_filenames: list[str] = []
        self.search_results: list[dict] = []
        self.selected_filename: str | None = None
        self._is_dirty = False
        self._preview_after_id = None
        self._autosave_after_id = None
        self._highlight_after_id = None
        self._preview_sync_after_id = None
        self._watch_after_id = None
        self._known_mtimes: dict[Path, float] = {}
        self._suspend_change_events = False
        self._html_preview_error = None
        self._has_html_preview = False
        self._last_preview_fraction = 0.0
        self._suppress_preview_sync = False
        self._forced_preview_fraction: float | None = None
        self._preview_anchors_by_file: dict[str, list[dict]] = {}

        self.title(f'Visual Builder - {self.project_path.name}')
        self.geometry('1560x900')
        self.minsize(1240, 760)
        self.configure(bg='#f3efe5')
        self.protocol('WM_DELETE_WINDOW', self._on_close)

        self._load_preview_capability()
        self._build_ui()
        self._load_chapter_list()
        self._start_file_watch()

    def _load_preview_capability(self):
        try:
            from tkinterweb import HtmlFrame

            self._html_frame_cls = HtmlFrame
            self._has_html_preview = True
        except Exception as exc:
            self._html_frame_cls = None
            self._html_preview_error = str(exc)

    def _build_ui(self):
        self.status_var = tk.StringVar(value='Ready')
        self.current_path_var = tk.StringVar(value='No chapter selected')
        self.search_query_var = tk.StringVar()
        self.search_in_name_var = tk.BooleanVar(value=True)
        self.search_in_content_var = tk.BooleanVar(value=True)
        self.search_case_var = tk.BooleanVar(value=False)
        self.search_whole_word_var = tk.BooleanVar(value=False)

        toolbar = ttk.Frame(self, padding=(12, 10))
        toolbar.pack(fill='x')

        ttk.Button(toolbar, text='Save', command=self.save_current_file).pack(side='left')
        ttk.Button(toolbar, text='Refresh', command=self.refresh_preview).pack(side='left', padx=(8, 0))
        ttk.Button(toolbar, text='New Chapter', command=self.create_chapter).pack(side='left', padx=(16, 0))
        ttk.Button(toolbar, text='New Subchapter', command=self.create_subchapter).pack(side='left', padx=(8, 0))
        ttk.Button(toolbar, text='Rename', command=self.rename_chapter).pack(side='left', padx=(8, 0))
        ttk.Button(toolbar, text='Delete', command=self.delete_chapter).pack(side='left', padx=(8, 0))
        ttk.Button(toolbar, text='Reformat', command=self.reformat_current_chapter).pack(side='left', padx=(8, 0))
        ttk.Button(toolbar, text='Paragraph', command=self.open_paragraph_settings).pack(side='left', padx=(16, 0))
        ttk.Button(toolbar, text='Margins', command=self.open_page_settings).pack(side='left', padx=(8, 0))
        ttk.Button(toolbar, text='List Markers', command=self.open_list_marker_settings).pack(side='left', padx=(8, 0))
        ttk.Button(toolbar, text='Move Up', command=lambda: self.move_selected_chapter(-1)).pack(side='left', padx=(16, 0))
        ttk.Button(toolbar, text='Move Down', command=lambda: self.move_selected_chapter(1)).pack(side='left', padx=(8, 0))
        ttk.Button(toolbar, text='Build DOCX', command=self.build_docx).pack(side='right')

        header = ttk.Frame(self, padding=(12, 0, 12, 8))
        header.pack(fill='x')
        ttk.Label(header, textvariable=self.current_path_var).pack(side='left')
        ttk.Label(header, textvariable=self.status_var).pack(side='right')

        self.paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.paned.pack(fill='both', expand=True, padx=12, pady=(0, 12))

        self.nav_frame = ttk.Frame(self.paned, width=320)
        self.editor_frame = ttk.Frame(self.paned, width=560)
        self.preview_frame = ttk.Frame(self.paned, width=720)

        self.paned.add(self.nav_frame, weight=2)
        self.paned.add(self.editor_frame, weight=3)
        self.paned.add(self.preview_frame, weight=4)

        self._build_navigator()
        self._build_editor()
        self._build_preview()

    def _build_navigator(self):
        ttk.Label(self.nav_frame, text='Project Outline').pack(anchor='w', padx=8, pady=(8, 4))

        button_row = ttk.Frame(self.nav_frame)
        button_row.pack(fill='x', padx=8, pady=(0, 6))
        ttk.Button(button_row, text='Add', command=self.create_chapter).pack(side='left')
        ttk.Button(button_row, text='Add Child', command=self.create_subchapter).pack(side='left', padx=(6, 0))
        ttk.Button(button_row, text='Rename', command=self.rename_chapter).pack(side='left', padx=(6, 0))
        ttk.Button(button_row, text='Delete', command=self.delete_chapter).pack(side='left', padx=(6, 0))

        list_wrapper = ttk.Frame(self.nav_frame)
        list_wrapper.pack(fill='both', expand=True, padx=8, pady=(0, 10))

        self.chapter_listbox = tk.Listbox(
            list_wrapper,
            font=('Consolas', 10),
            activestyle='none',
            exportselection=False,
        )
        self.chapter_listbox.pack(side='left', fill='both', expand=True)
        scrollbar = ttk.Scrollbar(list_wrapper, orient='vertical', command=self.chapter_listbox.yview)
        scrollbar.pack(side='right', fill='y')
        self.chapter_listbox.configure(yscrollcommand=scrollbar.set)
        self.chapter_listbox.bind('<<ListboxSelect>>', self._on_chapter_selected)

        search_frame = ttk.LabelFrame(self.nav_frame, text='Advanced Search', padding=8)
        search_frame.pack(fill='both', expand=False, padx=8, pady=(0, 8))

        entry_row = ttk.Frame(search_frame)
        entry_row.pack(fill='x')
        search_entry = ttk.Entry(search_frame, textvariable=self.search_query_var)
        search_entry.pack(fill='x')
        search_entry.bind('<Return>', lambda _event: self.run_advanced_search())

        options_row = ttk.Frame(search_frame)
        options_row.pack(fill='x', pady=(8, 6))
        ttk.Checkbutton(options_row, text='Filename', variable=self.search_in_name_var).pack(side='left')
        ttk.Checkbutton(options_row, text='Content', variable=self.search_in_content_var).pack(side='left', padx=(8, 0))
        ttk.Checkbutton(options_row, text='Case', variable=self.search_case_var).pack(side='left', padx=(8, 0))
        ttk.Checkbutton(options_row, text='Whole Word', variable=self.search_whole_word_var).pack(side='left', padx=(8, 0))

        action_row = ttk.Frame(search_frame)
        action_row.pack(fill='x', pady=(0, 6))
        ttk.Button(action_row, text='Search', command=self.run_advanced_search).pack(side='left')
        ttk.Button(action_row, text='Clear', command=self.clear_search).pack(side='left', padx=(6, 0))

        self.search_results_listbox = tk.Listbox(search_frame, font=('Consolas', 9), height=10, activestyle='none')
        self.search_results_listbox.pack(fill='both', expand=True)
        self.search_results_listbox.bind('<Double-1>', self._open_selected_search_result)

        ttk.Button(self.nav_frame, text='Reload Chapters', command=self._load_chapter_list).pack(
            fill='x', padx=8, pady=(0, 8)
        )

    def _build_editor(self):
        ttk.Label(self.editor_frame, text='Markdown').pack(anchor='w', padx=8, pady=(8, 4))

        helper_text = (
            'Scholar-style draft flow: research question, argument, evidence, analysis, conclusion. '
            'Use subchapters to break claims into smaller units.'
        )
        ttk.Label(self.editor_frame, text=helper_text, foreground='#666', wraplength=520, justify='left').pack(
            anchor='w', padx=8, pady=(0, 6)
        )

        text_wrapper = ttk.Frame(self.editor_frame)
        text_wrapper.pack(fill='both', expand=True, padx=8, pady=(0, 8))

        self.editor_text = tk.Text(text_wrapper, font=('Consolas', 11), wrap='word', undo=True)
        self.editor_text.pack(side='left', fill='both', expand=True)
        scrollbar = ttk.Scrollbar(text_wrapper, orient='vertical', command=self.editor_text.yview)
        scrollbar.pack(side='right', fill='y')
        self.editor_text.configure(yscrollcommand=scrollbar.set)

        self._configure_editor_tags()
        self.editor_text.bind('<<Modified>>', self._on_editor_modified)
        self.editor_text.bind('<<Paste>>', self._handle_markdown_paste)
        self.editor_text.bind('<Control-v>', self._handle_markdown_paste)
        self.editor_text.bind('<Control-V>', self._handle_markdown_paste)
        self.editor_text.bind('<Return>', self._handle_editor_return)
        self.editor_text.bind('<Tab>', self._handle_editor_tab)
        self.editor_text.bind('<ISO_Left_Tab>', self._handle_editor_shift_tab)
        self.editor_text.bind('<Shift-Tab>', self._handle_editor_shift_tab)
        self.editor_text.bind('<KeyRelease>', self._schedule_preview_sync)
        self.editor_text.bind('<ButtonRelease-1>', self._schedule_preview_sync)
        self.editor_text.bind('<MouseWheel>', self._schedule_preview_sync)
        self.editor_text.bind('<Configure>', self._schedule_preview_sync)

    def _build_preview(self):
        ttk.Label(self.preview_frame, text='Assembled Preview').pack(anchor='w', padx=8, pady=(8, 4))

        if self._has_html_preview:
            self.preview_widget = self._html_frame_cls(self.preview_frame, messages_enabled=False)
            self.preview_widget.pack(fill='both', expand=True, padx=8, pady=(0, 8))
        else:
            self.preview_widget = tk.Text(
                self.preview_frame,
                font=('Consolas', 10),
                wrap='word',
                bg='#fffdf8',
                fg='#2b241b',
                state='disabled',
            )
            self.preview_widget.pack(fill='both', expand=True, padx=8, pady=(0, 8))
            PreviewUtils.configure_preview_text_tags(self.preview_widget)

            if self._html_preview_error:
                ttk.Label(
                    self.preview_frame,
                    text=(
                        'Using text preview fallback because HtmlFrame is unavailable.\n'
                        f'Python: {sys.executable}\n'
                        f'Reason: {self._html_preview_error}'
                    ),
                    foreground='#777',
                ).pack(anchor='w', padx=8, pady=(0, 8))

        self.preview_widget.bind('<MouseWheel>', self._schedule_editor_sync)
        self.preview_widget.bind('<ButtonRelease-1>', self._schedule_editor_sync)
        self.preview_widget.bind('<KeyRelease>', self._schedule_editor_sync)
        self.preview_widget.bind('<Configure>', self._schedule_editor_sync)

    def _configure_editor_tags(self):
        self.editor_text.tag_configure('heading1', foreground='#1A3A5C', font=('Consolas', 11, 'bold'))
        self.editor_text.tag_configure('heading2', foreground='#1F619E', font=('Consolas', 11, 'bold'))
        self.editor_text.tag_configure('heading3', foreground='#2E86AB', font=('Consolas', 11, 'bold'))
        self.editor_text.tag_configure('heading4', foreground='#449DD1', font=('Consolas', 11, 'bold'))
        self.editor_text.tag_configure('bold', font=('Consolas', 11, 'bold'))
        self.editor_text.tag_configure('italic', font=('Consolas', 11, 'italic'))
        self.editor_text.tag_configure('code', background='#f0f0f0', foreground='#9c2f52')
        self.editor_text.tag_configure('search_hit', background='#fff3a3')

    def _load_chapter_list(self, select_filename: str | None = None):
        current_name = select_filename or (self.current_file.name if self.current_file else None)
        self.chapter_filenames = self.assembler.get_chapter_filenames()

        self.chapter_listbox.delete(0, tk.END)
        for filename in self.chapter_filenames:
            self.chapter_listbox.insert(tk.END, self._format_chapter_label(filename))
            file_path = self.project_path / 'chapters' / filename
            if file_path.exists():
                self._known_mtimes[file_path] = file_path.stat().st_mtime

        if not self.chapter_filenames:
            self.current_path_var.set('No chapters found')
            self.refresh_preview()
            return

        selected_index = 0
        if current_name and current_name in self.chapter_filenames:
            selected_index = self.chapter_filenames.index(current_name)

        self.chapter_listbox.selection_clear(0, tk.END)
        self.chapter_listbox.selection_set(selected_index)
        self.chapter_listbox.activate(selected_index)
        self.selected_filename = self.chapter_filenames[selected_index]
        self._load_selected_chapter()

    def _format_chapter_label(self, filename: str) -> str:
        title = self._humanize_filename(filename)
        if self.SUBCHAPTER_RE.match(filename):
            return f'    {title}'
        if self.FRONTMATTER_RE.match(filename):
            return f'[Front] {title}'
        return title

    def _humanize_filename(self, filename: str) -> str:
        stem = Path(filename).stem
        stem = re.sub(r'^F\d{2}_', '', stem)
        stem = re.sub(r'^Ch\d{2}_S\d{2}_', '', stem)
        stem = re.sub(r'^Ch\d{2}_', '', stem)
        return stem.replace('_', ' ')

    def _get_selected_index(self) -> int | None:
        selection = self.chapter_listbox.curselection()
        if not selection:
            return None
        return selection[0]

    def _get_selected_filename(self) -> str | None:
        if self.selected_filename and self.selected_filename in self.chapter_filenames:
            return self.selected_filename
        index = self._get_selected_index()
        if index is None or index >= len(self.chapter_filenames):
            return None
        return self.chapter_filenames[index]

    def _on_chapter_selected(self, _event=None):
        index = self._get_selected_index()
        if index is not None and index < len(self.chapter_filenames):
            self.selected_filename = self.chapter_filenames[index]
        self._load_selected_chapter()

    def _load_selected_chapter(self):
        filename = self._get_selected_filename()
        if not filename:
            return

        self.selected_filename = filename
        file_path = self.project_path / 'chapters' / filename
        if self.current_file == file_path:
            return

        if self._is_dirty:
            self.save_current_file()

        self.current_file = file_path
        self.current_path_var.set(str(file_path.relative_to(self.project_path)))
        self._read_current_file_into_editor()
        self.refresh_preview()
        self._set_status(f'Loaded {filename}')

    def _read_current_file_into_editor(self):
        if not self.current_file:
            return

        content = self.current_file.read_text(encoding='utf-8')
        self._suspend_change_events = True
        self.editor_text.delete('1.0', tk.END)
        self.editor_text.insert('1.0', content)
        self.editor_text.edit_modified(False)
        self._suspend_change_events = False
        self._is_dirty = False
        self._clear_search_highlight()
        self._refresh_title()
        self._schedule_highlight()

    def _on_editor_modified(self, _event=None):
        if self._suspend_change_events:
            self.editor_text.edit_modified(False)
            return

        if self.editor_text.edit_modified():
            self.editor_text.edit_modified(False)
            self._is_dirty = True
            self._refresh_title()
            self._schedule_autosave()
            self._schedule_preview_refresh()
            self._schedule_highlight()
            self._set_status('Editing...')

    def _schedule_autosave(self):
        if self._autosave_after_id is not None:
            self.after_cancel(self._autosave_after_id)
        self._autosave_after_id = self.after(self.AUTOSAVE_DEBOUNCE_MS, self.save_current_file)

    def _schedule_preview_refresh(self):
        if self._preview_after_id is not None:
            self.after_cancel(self._preview_after_id)
        self._preview_after_id = self.after(self.PREVIEW_DEBOUNCE_MS, self.refresh_preview)

    def _schedule_highlight(self):
        if self._highlight_after_id is not None:
            self.after_cancel(self._highlight_after_id)
        self._highlight_after_id = self.after(self.HIGHLIGHT_DEBOUNCE_MS, self._apply_editor_highlighting)

    def _schedule_preview_sync(self, _event=None):
        if self._preview_sync_after_id is not None:
            self.after_cancel(self._preview_sync_after_id)
        self._preview_sync_after_id = self.after(80, self.sync_preview_to_editor)

    def _schedule_editor_sync(self, _event=None):
        if self._suppress_preview_sync:
            return
        if self._preview_sync_after_id is not None:
            self.after_cancel(self._preview_sync_after_id)
        self._preview_sync_after_id = self.after(80, self.sync_editor_to_preview)

    def _apply_editor_highlighting(self):
        text = self.editor_text.get('1.0', 'end-1c')
        for tag in ('heading1', 'heading2', 'heading3', 'heading4', 'bold', 'italic', 'code'):
            self.editor_text.tag_remove(tag, '1.0', tk.END)

        for match in re.finditer(r'^(#{1,4})\s+.*$', text, re.MULTILINE):
            level = len(match.group(1))
            start = f'1.0+{match.start()}c'
            end = f'1.0+{match.end()}c'
            self.editor_text.tag_add(f'heading{level}', start, end)

        for match in re.finditer(r'\*\*[^*\n]+\*\*', text):
            self.editor_text.tag_add('bold', f'1.0+{match.start()}c', f'1.0+{match.end()}c')

        for match in re.finditer(r'(?<!\*)\*[^*\n]+\*(?!\*)', text):
            self.editor_text.tag_add('italic', f'1.0+{match.start()}c', f'1.0+{match.end()}c')

        for match in re.finditer(r'`[^`\n]+`', text):
            self.editor_text.tag_add('code', f'1.0+{match.start()}c', f'1.0+{match.end()}c')

        self._highlight_after_id = None

    def _handle_markdown_paste(self, _event=None):
        try:
            clipboard_text = self.clipboard_get()
        except tk.TclError:
            return 'break'

        normalized = MarkdownUtils.normalize_pasted_markdown(clipboard_text)
        if not normalized:
            return 'break'

        try:
            if self.editor_text.tag_ranges(tk.SEL):
                self.editor_text.delete(tk.SEL_FIRST, tk.SEL_LAST)
        except tk.TclError:
            pass

        insert_index = self.editor_text.index(tk.INSERT)
        prefix = self.editor_text.get(f'{insert_index} linestart', insert_index)
        if prefix.strip():
            normalized = '\n' + normalized

        self.editor_text.insert(tk.INSERT, normalized)
        self._is_dirty = True
        self._refresh_title()
        self._schedule_autosave()
        self._schedule_preview_refresh()
        self._schedule_highlight()
        self._set_status('Pasted and normalized to markdown')
        return 'break'

    def _handle_editor_return(self, _event=None):
        editor_text = self.editor_text.get('1.0', 'end-1c')
        current_line_number = int(self.editor_text.index(tk.INSERT).split('.')[0])
        if MarkdownUtils.is_line_inside_fenced_block(editor_text, current_line_number):
            return None

        line_start = self.editor_text.index('insert linestart')
        line_end = self.editor_text.index('insert lineend')
        current_line = self.editor_text.get(line_start, line_end)

        markers = ChapterSettings.get_list_markers_by_level(
            self.assembler.get_config(),
            self.current_file.name if self.current_file else '',
        )
        continuation = MarkdownUtils.get_list_continuation_for_line(current_line, markers)
        if continuation is None:
            return None

        insert_index = self.editor_text.index(tk.INSERT)
        if insert_index != line_end:
            return None

        self.editor_text.insert(tk.INSERT, continuation)
        self.editor_text.see(tk.INSERT)
        self._is_dirty = True
        self._refresh_title()
        self._schedule_autosave()
        self._schedule_preview_refresh()
        self._schedule_highlight()
        self._set_status('Continued list item')
        return 'break'

    def _handle_editor_tab(self, _event=None):
        if self._shift_selected_list_lines(1):
            return 'break'
        return None

    def _handle_editor_shift_tab(self, _event=None):
        if self._shift_selected_list_lines(-1):
            return 'break'
        return None

    def _shift_selected_list_lines(self, delta: int) -> bool:
        editor_text = self.editor_text.get('1.0', 'end-1c')
        markers = ChapterSettings.get_list_markers_by_level(
            self.assembler.get_config(),
            self.current_file.name if self.current_file else '',
        )

        try:
            sel_start = self.editor_text.index(tk.SEL_FIRST)
            sel_end = self.editor_text.index(tk.SEL_LAST)
            start_line = int(sel_start.split('.')[0])
            end_line = int(sel_end.split('.')[0])
            if sel_end.endswith('.0') and end_line > start_line:
                end_line -= 1
        except tk.TclError:
            insert_index = self.editor_text.index(tk.INSERT)
            start_line = end_line = int(insert_index.split('.')[0])

        lines = []
        changed = False
        for line_number in range(start_line, end_line + 1):
            if MarkdownUtils.is_line_inside_fenced_block(editor_text, line_number):
                return False
            line_start = f'{line_number}.0'
            line_end = f'{line_number}.end'
            original = self.editor_text.get(line_start, line_end)
            shifted = MarkdownUtils.shift_list_line(original, delta, markers)
            if shifted != original:
                changed = True
            lines.append(shifted)

        if not changed:
            return False

        block_start = f'{start_line}.0'
        block_end = f'{end_line}.end'
        self.editor_text.delete(block_start, block_end)
        self.editor_text.insert(block_start, '\n'.join(lines))
        self.editor_text.mark_set(tk.INSERT, block_start)
        self.editor_text.see(block_start)
        self._is_dirty = True
        self._refresh_title()
        self._schedule_autosave()
        self._schedule_preview_refresh()
        self._schedule_highlight()
        self._set_status('Updated list indentation')
        return True

    def reformat_current_chapter(self):
        if not self.current_file:
            return

        markers = ChapterSettings.get_list_markers_by_level(
            self.assembler.get_config(),
            self.current_file.name,
        )
        original = self.editor_text.get('1.0', 'end-1c')
        reformatted = MarkdownUtils.reformat_markdown_document(original, markers)
        reformatted = reformatted.rstrip('\n')
        if reformatted == original:
            self._set_status('Chapter already formatted')
            return

        insert_index = self.editor_text.index(tk.INSERT)
        self.editor_text.delete('1.0', tk.END)
        self.editor_text.insert('1.0', reformatted)
        try:
            self.editor_text.mark_set(tk.INSERT, insert_index)
        except tk.TclError:
            self.editor_text.mark_set(tk.INSERT, 'end-1c')
        self.editor_text.see(tk.INSERT)
        self._is_dirty = True
        self._refresh_title()
        self._schedule_autosave()
        self._schedule_preview_refresh()
        self._schedule_highlight()
        self._set_status(f'Reformatted {self.current_file.name}')

    @staticmethod
    def _compute_global_line_for_file(entries, filename: str | None, local_line_number: int) -> int:
        if not entries:
            return max(1, local_line_number)

        safe_local_line = max(1, local_line_number)
        if filename:
            for entry in entries:
                if entry.filename != filename:
                    continue
                chapter_line_count = max(1, entry.end_line - entry.start_line + 1)
                return min(entry.end_line, entry.start_line + min(safe_local_line, chapter_line_count) - 1)

        return safe_local_line

    @staticmethod
    def _compute_preview_scroll_fraction(entries, global_line_number: int) -> float:
        if not entries:
            return 0.0

        total_lines = max(entry.end_line for entry in entries)
        if total_lines <= 0:
            return 0.0

        safe_global_line = min(max(1, global_line_number), total_lines)
        return max(0.0, min(1.0, (safe_global_line - 1) / total_lines))

    def _get_editor_view_line_number(self) -> int:
        try:
            visible_index = self.editor_text.index('@0,0')
        except tk.TclError:
            visible_index = self.editor_text.index(tk.INSERT)
        return max(1, int(str(visible_index).split('.')[0]))

    def _get_preview_scroll_fraction_from_editor(self, entries) -> float:
        filename = self.current_file.name if self.current_file else self._get_selected_filename()
        editor_line = self._get_editor_view_line_number()
        global_line = self._compute_global_line_for_file(entries, filename, editor_line)
        return self._compute_preview_scroll_fraction(entries, global_line)

    @staticmethod
    def _compute_global_line_from_preview_fraction(entries, fraction: float) -> int:
        if not entries:
            return 1

        total_lines = max(entry.end_line for entry in entries)
        if total_lines <= 0:
            return 1

        safe_fraction = max(0.0, min(1.0, fraction))
        return min(total_lines, max(1, int(safe_fraction * total_lines) + 1))

    @staticmethod
    def _resolve_file_line_from_global_line(entries, global_line_number: int) -> tuple[str | None, int]:
        if not entries:
            return None, 1

        safe_global_line = max(1, global_line_number)
        for entry in entries:
            if entry.start_line <= safe_global_line <= entry.end_line:
                return entry.filename, safe_global_line - entry.start_line + 1

        last_entry = entries[-1]
        return last_entry.filename, max(1, last_entry.end_line - last_entry.start_line + 1)

    def _get_preview_yview_fraction(self) -> float:
        try:
            view = self.preview_widget.yview()
        except Exception:
            return self._last_preview_fraction
        if not view:
            return self._last_preview_fraction
        return max(0.0, min(1.0, float(view[0])))

    def _apply_preview_scroll_fraction(self, fraction: float):
        safe_fraction = max(0.0, min(1.0, fraction))
        self._last_preview_fraction = safe_fraction

        def _move():
            try:
                self._suppress_preview_sync = True
                self.preview_widget.yview_moveto(safe_fraction)
            except Exception:
                pass
            finally:
                self.after(150, self._clear_preview_sync_suppression)

        if self._has_html_preview:
            self.after_idle(_move)
        else:
            _move()

    def _clear_preview_sync_suppression(self):
        self._suppress_preview_sync = False

    def sync_preview_to_editor(self):
        self._preview_sync_after_id = None
        try:
            _final_md, entries = self.assembler.assemble_with_metadata()
        except Exception:
            return
        if not entries:
            return
        if self._has_html_preview:
            self._scroll_html_preview_to_anchor(self._get_preview_fragment_from_editor())
        else:
            self._apply_preview_scroll_fraction(self._get_preview_scroll_fraction_from_editor(entries))

    def sync_editor_to_preview(self):
        self._preview_sync_after_id = None
        if self._suppress_preview_sync:
            return

        try:
            _final_md, entries = self.assembler.assemble_with_metadata()
        except Exception:
            return
        if not entries:
            return

        fraction = self._get_preview_yview_fraction()
        global_line = self._compute_global_line_from_preview_fraction(entries, fraction)
        filename, local_line = self._resolve_file_line_from_global_line(entries, global_line)
        if not filename:
            return

        if not self.current_file or self.current_file.name != filename:
            self.selected_filename = filename
            self._forced_preview_fraction = fraction
            self._load_chapter_list(select_filename=filename)

        line_index = f'{local_line}.0'
        self.editor_text.mark_set(tk.INSERT, line_index)
        self.editor_text.see(line_index)

    def save_current_file(self):
        if self._autosave_after_id is not None:
            self.after_cancel(self._autosave_after_id)
            self._autosave_after_id = None

        if not self.current_file or not self._is_dirty:
            return

        content = self.editor_text.get('1.0', tk.END).rstrip('\n') + '\n'
        self.current_file.write_text(content, encoding='utf-8')
        self._known_mtimes[self.current_file] = self.current_file.stat().st_mtime
        self._is_dirty = False
        self._refresh_title()
        self._set_status(f'Saved {self.current_file.name}')

    def create_chapter(self):
        anchor_filename = self._get_selected_filename()
        title = self._prompt_for_title('New Chapter', 'Enter chapter title:')
        if not title:
            return

        filename = self._create_chapter_file(title, anchor_filename=anchor_filename)
        self._load_chapter_list(select_filename=filename)
        self.refresh_preview()
        self._set_status(f'Created {filename}')

    def create_subchapter(self):
        anchor_filename = self._get_selected_filename()
        title = self._prompt_for_title('New Subchapter', 'Enter subchapter title:')
        if not title:
            return

        try:
            filename = self._create_subchapter_file(title, anchor_filename=anchor_filename)
        except ValueError as exc:
            messagebox.showwarning('New Subchapter', str(exc), parent=self)
            return

        self._load_chapter_list(select_filename=filename)
        self.refresh_preview()
        self._set_status(f'Created {filename}')

    def rename_chapter(self):
        selected_filename = self._get_selected_filename()
        if not selected_filename:
            return

        initial_title = self._humanize_filename(selected_filename)
        title = self._prompt_for_title('Rename Chapter', 'Enter new title:', initial_value=initial_title)
        if not title or title == initial_title:
            return

        if self._is_dirty:
            self.save_current_file()

        try:
            new_filename = self._rename_chapter_file(selected_filename, title)
        except ValueError as exc:
            messagebox.showwarning('Rename Chapter', str(exc), parent=self)
            return

        self._load_chapter_list(select_filename=new_filename)
        self.selected_filename = new_filename
        self.refresh_preview()
        self._set_status(f'Renamed to {new_filename}')

    def delete_chapter(self):
        selected_filename = self._get_selected_filename()
        if not selected_filename:
            return

        if not messagebox.askyesno(
            'Delete Chapter',
            f'Delete "{self._humanize_filename(selected_filename)}"?',
            parent=self,
        ):
            return

        next_selection = self._delete_chapter_file(selected_filename)
        self._load_chapter_list(select_filename=next_selection)
        self.selected_filename = next_selection
        self.refresh_preview()
        self._set_status(f'Deleted {selected_filename}')

    def _prompt_for_title(self, dialog_title: str, prompt_text: str, initial_value: str = '') -> str | None:
        value = simpledialog.askstring(dialog_title, prompt_text, initialvalue=initial_value, parent=self)
        if value is None:
            return None
        value = value.strip()
        return value or None

    def _create_chapter_file(self, title: str, anchor_filename: str | None = None) -> str:
        chapter_number = self._next_top_level_number()
        filename = f'Ch{chapter_number:02d}_{self._slugify_title(title)}.md'
        target_path = self.project_path / 'chapters' / filename
        target_path.write_text(self._build_scholarly_chapter_content(title), encoding='utf-8')

        order = self.assembler.get_chapter_filenames()
        insert_index = self._chapter_insert_index(order, anchor_filename)
        order.insert(insert_index, filename)
        self.assembler.save_chapter_order(order)
        self._known_mtimes[target_path] = target_path.stat().st_mtime
        return filename

    def _create_subchapter_file(self, title: str, anchor_filename: str | None = None) -> str:
        parent_filename = self._resolve_subchapter_parent(anchor_filename or self._get_selected_filename())
        if not parent_filename:
            raise ValueError('Select a chapter or subchapter before creating a child item.')

        parent_match = self.TOP_LEVEL_RE.match(parent_filename)
        if not parent_match:
            raise ValueError('Subchapters can only be created under top-level chapters.')

        chapter_number = int(parent_match.group('chapter'))
        subchapter_number = self._next_subchapter_number(chapter_number)
        filename = f'Ch{chapter_number:02d}_S{subchapter_number:02d}_{self._slugify_title(title)}.md'
        target_path = self.project_path / 'chapters' / filename
        target_path.write_text(
            self._build_scholarly_subchapter_content(title, self._humanize_filename(parent_filename)),
            encoding='utf-8',
        )

        order = self.assembler.get_chapter_filenames()
        insert_index = self._subchapter_insert_index(order, parent_filename)
        order.insert(insert_index, filename)
        self.assembler.save_chapter_order(order)
        self._known_mtimes[target_path] = target_path.stat().st_mtime
        return filename

    def _rename_chapter_file(self, selected_filename: str, new_title: str) -> str:
        front_match = self.FRONTMATTER_RE.match(selected_filename)
        top_match = self.TOP_LEVEL_RE.match(selected_filename)
        sub_match = self.SUBCHAPTER_RE.match(selected_filename)

        if front_match:
            new_filename = f'F{front_match.group("index")}_{self._slugify_title(new_title)}.md'
        elif top_match:
            new_filename = f'Ch{int(top_match.group("chapter")):02d}_{self._slugify_title(new_title)}.md'
        elif sub_match:
            new_filename = (
                f'Ch{int(sub_match.group("chapter")):02d}_'
                f'S{int(sub_match.group("subchapter")):02d}_{self._slugify_title(new_title)}.md'
            )
        else:
            stem = Path(selected_filename).stem
            prefix = stem.split('_', 1)[0]
            new_filename = f'{prefix}_{self._slugify_title(new_title)}.md'

        source_path = self.project_path / 'chapters' / selected_filename
        target_path = self.project_path / 'chapters' / new_filename
        if target_path.exists() and target_path != source_path:
            raise ValueError(f'{new_filename} already exists.')

        source_path.rename(target_path)

        order = self.assembler.get_chapter_filenames()
        order = [new_filename if item == selected_filename else item for item in order]
        self.assembler.save_chapter_order(order)

        self._known_mtimes.pop(source_path, None)
        self._known_mtimes[target_path] = target_path.stat().st_mtime
        if self.current_file == source_path:
            self.current_file = target_path
        if self.selected_filename == selected_filename:
            self.selected_filename = new_filename
        return new_filename

    def _delete_chapter_file(self, selected_filename: str) -> str | None:
        order = self.assembler.get_chapter_filenames()
        selected_index = order.index(selected_filename)
        target_path = self.project_path / 'chapters' / selected_filename

        if self.current_file == target_path:
            self.current_file = None
            self.current_path_var.set('No chapter selected')
            self._suspend_change_events = True
            self.editor_text.delete('1.0', tk.END)
            self.editor_text.edit_modified(False)
            self._suspend_change_events = False
            self._is_dirty = False
            self._refresh_title()
        if self.selected_filename == selected_filename:
            self.selected_filename = None

        if target_path.exists():
            target_path.unlink()
        self._known_mtimes.pop(target_path, None)

        order.remove(selected_filename)
        self.assembler.save_chapter_order(order)

        if not order:
            return None
        return order[min(selected_index, len(order) - 1)]

    def _chapter_insert_index(self, order: list[str], anchor_filename: str | None = None) -> int:
        selected_filename = anchor_filename or self._get_selected_filename()
        if not selected_filename or selected_filename not in order:
            return len(order)

        selected_index = order.index(selected_filename)
        if self.TOP_LEVEL_RE.match(selected_filename):
            insert_index = selected_index + 1
            while insert_index < len(order) and self._belongs_to_parent(order[insert_index], selected_filename):
                insert_index += 1
            return insert_index
        return selected_index + 1

    def _subchapter_insert_index(self, order: list[str], parent_filename: str) -> int:
        parent_index = order.index(parent_filename)
        insert_index = parent_index + 1
        while insert_index < len(order) and self._belongs_to_parent(order[insert_index], parent_filename):
            insert_index += 1
        return insert_index

    def _resolve_subchapter_parent(self, selected_filename: str | None) -> str | None:
        if not selected_filename:
            return None
        if self.TOP_LEVEL_RE.match(selected_filename):
            return selected_filename
        sub_match = self.SUBCHAPTER_RE.match(selected_filename)
        if not sub_match:
            return None
        chapter_number = int(sub_match.group('chapter'))
        for candidate in self.assembler.get_chapter_filenames():
            top_match = self.TOP_LEVEL_RE.match(candidate)
            if top_match and int(top_match.group('chapter')) == chapter_number:
                return candidate
        return None

    def _belongs_to_parent(self, filename: str, parent_filename: str) -> bool:
        parent_match = self.TOP_LEVEL_RE.match(parent_filename)
        child_match = self.SUBCHAPTER_RE.match(filename)
        if not parent_match or not child_match:
            return False
        return int(parent_match.group('chapter')) == int(child_match.group('chapter'))

    def _next_top_level_number(self) -> int:
        numbers = []
        for filename in self.assembler.get_chapter_filenames():
            match = self.TOP_LEVEL_RE.match(filename)
            if match:
                numbers.append(int(match.group('chapter')))
        return (max(numbers) + 1) if numbers else 1

    def _next_subchapter_number(self, chapter_number: int) -> int:
        numbers = []
        for filename in self.assembler.get_chapter_filenames():
            match = self.SUBCHAPTER_RE.match(filename)
            if match and int(match.group('chapter')) == chapter_number:
                numbers.append(int(match.group('subchapter')))
        return (max(numbers) + 1) if numbers else 1

    def _slugify_title(self, title: str) -> str:
        slug = re.sub(r'[^\w\s-]', '', title, flags=re.UNICODE)
        slug = slug.strip().replace(' ', '_')
        slug = re.sub(r'_+', '_', slug)
        return slug or 'New_Item'

    def _build_scholarly_chapter_content(self, title: str) -> str:
        return (
            f'## {title}\n\n'
            '### Research Question\n\n'
            'State the central claim, scope, and why this section matters.\n\n'
            '### Theoretical Basis\n\n'
            'Define concepts, cite frameworks, and establish the analytical lens.\n\n'
            '### Analysis\n\n'
            'Develop the argument with evidence, examples, or system behavior.\n\n'
            '### Discussion\n\n'
            'Compare alternatives, identify tradeoffs, and address limitations.\n\n'
            '### Conclusion\n\n'
            'Summarize the contribution of this chapter and connect it to the next one.\n'
        )

    def _build_scholarly_subchapter_content(self, title: str, parent_title: str) -> str:
        return (
            f'### {title}\n\n'
            f'This subchapter extends **{parent_title}**.\n\n'
            '#### Claim\n\n'
            'State the precise point being argued.\n\n'
            '#### Evidence\n\n'
            'Add data, examples, diagrams, or observed behavior.\n\n'
            '#### Interpretation\n\n'
            'Explain why the evidence supports the claim.\n\n'
            '#### Interim Finding\n\n'
            'Close the subsection with the result that should carry forward.\n'
        )

    def _get_workspace_config(self):
        config = self.assembler.get_config()
        if not config:
            raise FileNotFoundError('Workspace is missing config.yaml')
        return config

    def _save_workspace_settings(self, updates: dict):
        config = self._get_workspace_config()
        merged = dict(config.settings or {})
        merged.update(updates)
        config.settings = merged
        config.save(self.project_path / 'config.yaml')
        self._set_status('Document settings saved')

    def open_paragraph_settings(self):
        from src.core.docx_helpers import DocxHelpers

        config = self._get_workspace_config()
        settings = DocxHelpers.get_paragraph_settings(config)

        dialog = tk.Toplevel(self)
        dialog.title('Paragraph Settings')
        dialog.transient(self)
        dialog.grab_set()
        dialog.resizable(False, False)

        body = ttk.Frame(dialog, padding=14)
        body.pack(fill='both', expand=True)

        alignment_var = tk.StringVar(value=str(settings.get('alignment', 'justify')).capitalize())
        special_indent_var = tk.StringVar(value=self._special_indent_label(settings.get('special_indent', 'first_line')))
        line_spacing_var = tk.StringVar(value=self._line_spacing_label(settings.get('line_spacing_mode', 'multiple')))

        left_var = tk.StringVar(value=str(settings.get('left_indent_cm', 0.0)))
        right_var = tk.StringVar(value=str(settings.get('right_indent_cm', 0.0)))
        special_by_var = tk.StringVar(value=str(settings.get('special_indent_by_cm', 1.27)))
        before_var = tk.StringVar(value=str(settings.get('space_before_pt', 0.0)))
        after_var = tk.StringVar(value=str(settings.get('space_after_pt', 6.0)))
        line_value_var = tk.StringVar(value=str(settings.get('line_spacing_value', 1.5)))

        self._settings_row(body, 'Alignment', ttk.Combobox(
            body, textvariable=alignment_var, state='readonly', values=['Left', 'Center', 'Right', 'Justify']
        ), 0)
        self._settings_row(body, 'Left (cm)', ttk.Entry(body, textvariable=left_var), 1)
        self._settings_row(body, 'Right (cm)', ttk.Entry(body, textvariable=right_var), 2)
        self._settings_row(body, 'Special', ttk.Combobox(
            body, textvariable=special_indent_var, state='readonly', values=['None', 'First line', 'Hanging']
        ), 3)
        self._settings_row(body, 'By (cm)', ttk.Entry(body, textvariable=special_by_var), 4)
        self._settings_row(body, 'Before (pt)', ttk.Entry(body, textvariable=before_var), 5)
        self._settings_row(body, 'After (pt)', ttk.Entry(body, textvariable=after_var), 6)
        self._settings_row(body, 'Line spacing', ttk.Combobox(
            body, textvariable=line_spacing_var, state='readonly', values=['Single', '1.5 lines', 'Double', 'Exactly']
        ), 7)
        self._settings_row(body, 'At', ttk.Entry(body, textvariable=line_value_var), 8)

        def save_settings():
            try:
                self._save_workspace_settings(
                    {
                        'alignment': alignment_var.get().lower(),
                        'left_indent_cm': float(left_var.get()),
                        'right_indent_cm': float(right_var.get()),
                        'special_indent': self._special_indent_value(special_indent_var.get()),
                        'special_indent_by_cm': float(special_by_var.get()),
                        'space_before_pt': float(before_var.get()),
                        'space_after_pt': float(after_var.get()),
                        'line_spacing_mode': self._line_spacing_value(line_spacing_var.get()),
                        'line_spacing_value': float(line_value_var.get()),
                    }
                )
            except ValueError:
                messagebox.showerror('Paragraph Settings', 'Numeric fields are invalid.', parent=dialog)
                return
            dialog.destroy()

        button_row = ttk.Frame(body)
        button_row.grid(row=9, column=0, columnspan=2, sticky='e', pady=(12, 0))
        ttk.Button(button_row, text='Save', command=save_settings).pack(side='left')
        ttk.Button(button_row, text='Cancel', command=dialog.destroy).pack(side='left', padx=(8, 0))

    def open_list_marker_settings(self):
        selected_filename = self._get_selected_filename()
        if not selected_filename:
            messagebox.showwarning('List Markers', 'Select a chapter first.', parent=self)
            return

        config = self._get_workspace_config()
        markers = ChapterSettings.get_list_markers_by_level(config, selected_filename)

        dialog = tk.Toplevel(self)
        dialog.title('List Markers')
        dialog.transient(self)
        dialog.grab_set()
        dialog.resizable(False, False)

        body = ttk.Frame(dialog, padding=14)
        body.pack(fill='both', expand=True)

        ttk.Label(
            body,
            text=f'Configure bullet markers for {selected_filename}',
            wraplength=420,
            justify='left',
        ).grid(row=0, column=0, columnspan=2, sticky='w', pady=(0, 10))

        marker_vars = []
        for index in range(max(5, len(markers))):
            value = markers[index] if index < len(markers) else markers[-1]
            marker_var = tk.StringVar(value=value)
            marker_vars.append(marker_var)
            self._settings_row(body, f'Level {index + 1}', ttk.Entry(body, textvariable=marker_var), index + 1)

        def save_settings():
            normalized = ChapterSettings.normalize_list_markers([var.get() for var in marker_vars])
            config = self._get_workspace_config()
            settings = dict(config.settings or {})
            chapter_settings = dict(settings.get('chapter_settings', {}) or {})
            file_settings = dict(chapter_settings.get(selected_filename, {}) or {})
            file_settings['list_markers_by_level'] = normalized
            chapter_settings[selected_filename] = file_settings
            settings['chapter_settings'] = chapter_settings
            config.settings = settings
            config.save(self.project_path / 'config.yaml')
            self.refresh_preview()
            self._set_status(f'List markers saved for {selected_filename}')
            dialog.destroy()

        button_row = ttk.Frame(body)
        button_row.grid(row=len(marker_vars) + 1, column=0, columnspan=2, sticky='e', pady=(12, 0))
        ttk.Button(button_row, text='Save', command=save_settings).pack(side='left')
        ttk.Button(button_row, text='Cancel', command=dialog.destroy).pack(side='left', padx=(8, 0))

    def open_page_settings(self):
        from src.core.docx_helpers import DocxHelpers

        config = self._get_workspace_config()
        settings = DocxHelpers.get_page_settings(config)

        dialog = tk.Toplevel(self)
        dialog.title('Page Setup')
        dialog.transient(self)
        dialog.grab_set()
        dialog.resizable(False, False)

        body = ttk.Frame(dialog, padding=14)
        body.pack(fill='both', expand=True)

        top_var = tk.StringVar(value=str(settings.get('margin_top_cm', 2.5)))
        bottom_var = tk.StringVar(value=str(settings.get('margin_bottom_cm', 2.5)))
        left_var = tk.StringVar(value=str(settings.get('margin_left_cm', 3.0)))
        right_var = tk.StringVar(value=str(settings.get('margin_right_cm', 2.0)))
        gutter_var = tk.StringVar(value=str(settings.get('gutter_cm', 0.0)))
        width_var = tk.StringVar(value=str(settings.get('page_width_cm', 21.0)))
        height_var = tk.StringVar(value=str(settings.get('page_height_cm', 29.7)))
        orientation_var = tk.StringVar(value=str(settings.get('orientation', 'portrait')).capitalize())

        self._settings_row(body, 'Top (cm)', ttk.Entry(body, textvariable=top_var), 0)
        self._settings_row(body, 'Bottom (cm)', ttk.Entry(body, textvariable=bottom_var), 1)
        self._settings_row(body, 'Left (cm)', ttk.Entry(body, textvariable=left_var), 2)
        self._settings_row(body, 'Right (cm)', ttk.Entry(body, textvariable=right_var), 3)
        self._settings_row(body, 'Gutter (cm)', ttk.Entry(body, textvariable=gutter_var), 4)
        self._settings_row(body, 'Page Width (cm)', ttk.Entry(body, textvariable=width_var), 5)
        self._settings_row(body, 'Page Height (cm)', ttk.Entry(body, textvariable=height_var), 6)
        self._settings_row(body, 'Orientation', ttk.Combobox(
            body, textvariable=orientation_var, state='readonly', values=['Portrait', 'Landscape']
        ), 7)

        def save_settings():
            try:
                self._save_workspace_settings(
                    {
                        'margin_top_cm': float(top_var.get()),
                        'margin_bottom_cm': float(bottom_var.get()),
                        'margin_left_cm': float(left_var.get()),
                        'margin_right_cm': float(right_var.get()),
                        'gutter_cm': float(gutter_var.get()),
                        'page_width_cm': float(width_var.get()),
                        'page_height_cm': float(height_var.get()),
                        'orientation': orientation_var.get().lower(),
                    }
                )
            except ValueError:
                messagebox.showerror('Page Setup', 'Numeric fields are invalid.', parent=dialog)
                return
            dialog.destroy()

        button_row = ttk.Frame(body)
        button_row.grid(row=8, column=0, columnspan=2, sticky='e', pady=(12, 0))
        ttk.Button(button_row, text='Save', command=save_settings).pack(side='left')
        ttk.Button(button_row, text='Cancel', command=dialog.destroy).pack(side='left', padx=(8, 0))

    def _settings_row(self, parent, label_text: str, widget, row_index: int):
        ttk.Label(parent, text=label_text).grid(row=row_index, column=0, sticky='w', padx=(0, 10), pady=4)
        widget.grid(row=row_index, column=1, sticky='ew', pady=4)
        parent.grid_columnconfigure(1, weight=1)

    def _special_indent_label(self, value: str) -> str:
        mapping = {'none': 'None', 'first_line': 'First line', 'hanging': 'Hanging'}
        return mapping.get(str(value).lower(), 'First line')

    def _special_indent_value(self, label: str) -> str:
        mapping = {'none': 'none', 'first line': 'first_line', 'hanging': 'hanging'}
        return mapping.get(label.strip().lower(), 'first_line')

    def _line_spacing_label(self, value: str) -> str:
        mapping = {'single': 'Single', 'multiple': '1.5 lines', 'double': 'Double', 'exactly': 'Exactly'}
        return mapping.get(str(value).lower(), '1.5 lines')

    def _line_spacing_value(self, label: str) -> str:
        mapping = {'single': 'single', '1.5 lines': 'multiple', 'double': 'double', 'exactly': 'exactly'}
        return mapping.get(label.strip().lower(), 'multiple')

    def move_selected_chapter(self, delta: int):
        selected_filename = self._get_selected_filename()
        if not selected_filename:
            return

        filenames = self.assembler.get_chapter_filenames()
        selected_index = filenames.index(selected_filename)
        new_order = self._move_outline_item(filenames, selected_index, delta)
        if new_order == filenames:
            return

        self.assembler.save_chapter_order(new_order)
        self._load_chapter_list(select_filename=selected_filename)
        self.selected_filename = selected_filename
        self.refresh_preview()
        self._set_status('Updated chapter order')

    def _move_outline_item(self, filenames: list[str], selected_index: int, delta: int) -> list[str]:
        selected_filename = filenames[selected_index]

        if self.TOP_LEVEL_RE.match(selected_filename):
            return self._move_top_level_block(filenames, selected_index, delta)
        if self.SUBCHAPTER_RE.match(selected_filename):
            return self._move_subchapter(filenames, selected_index, delta)

        new_index = selected_index + delta
        if new_index < 0 or new_index >= len(filenames):
            return filenames
        reordered = filenames[:]
        reordered[selected_index], reordered[new_index] = reordered[new_index], reordered[selected_index]
        return reordered

    def _move_top_level_block(self, filenames: list[str], selected_index: int, delta: int) -> list[str]:
        start, end = self._top_level_block_range(filenames, selected_index)
        block = filenames[start:end]
        remaining = filenames[:start] + filenames[end:]

        if delta < 0:
            previous_starts = [idx for idx, name in enumerate(remaining) if self.TOP_LEVEL_RE.match(name) or self.FRONTMATTER_RE.match(name)]
            insert_at = 0
            for idx in previous_starts:
                if idx < start:
                    insert_at = idx
            return remaining[:insert_at] + block + remaining[insert_at:]

        insert_at = len(remaining)
        for idx in range(start, len(remaining)):
            if self.TOP_LEVEL_RE.match(remaining[idx]) or self.FRONTMATTER_RE.match(remaining[idx]):
                next_start, _next_end = self._top_level_block_range(remaining, idx)
                insert_at = next_start + 1
                while insert_at < len(remaining) and self.SUBCHAPTER_RE.match(remaining[insert_at]):
                    insert_at += 1
                break
        return remaining[:insert_at] + block + remaining[insert_at:]

    def _move_subchapter(self, filenames: list[str], selected_index: int, delta: int) -> list[str]:
        selected_filename = filenames[selected_index]
        match = self.SUBCHAPTER_RE.match(selected_filename)
        if not match:
            return filenames

        chapter_number = int(match.group('chapter'))
        sibling_indices = [
            idx
            for idx, name in enumerate(filenames)
            if (sub_match := self.SUBCHAPTER_RE.match(name)) and int(sub_match.group('chapter')) == chapter_number
        ]
        sibling_position = sibling_indices.index(selected_index)
        new_position = sibling_position + delta
        if new_position < 0 or new_position >= len(sibling_indices):
            return filenames

        target_index = sibling_indices[new_position]
        reordered = filenames[:]
        reordered[selected_index], reordered[target_index] = reordered[target_index], reordered[selected_index]
        return reordered

    def _top_level_block_range(self, filenames: list[str], start_index: int) -> tuple[int, int]:
        start = start_index
        end = start + 1
        if not self.TOP_LEVEL_RE.match(filenames[start]):
            return start, end
        while end < len(filenames) and self.SUBCHAPTER_RE.match(filenames[end]):
            end += 1
        return start, end

    def run_advanced_search(self):
        query = self.search_query_var.get().strip()
        self.search_results = []
        self.search_results_listbox.delete(0, tk.END)

        if not query:
            self._set_status('Search query is empty')
            return
        if not (self.search_in_name_var.get() or self.search_in_content_var.get()):
            self._set_status('Select at least one search scope')
            return

        flags = 0 if self.search_case_var.get() else re.IGNORECASE
        pattern_text = re.escape(query)
        if self.search_whole_word_var.get():
            pattern_text = rf'\b{pattern_text}\b'
        pattern = re.compile(pattern_text, flags)

        for filename in self.assembler.get_chapter_filenames():
            display_title = self._humanize_filename(filename)
            if self.search_in_name_var.get() and pattern.search(filename):
                self._append_search_result(filename, None, f'{filename} [filename match]')
            elif self.search_in_name_var.get() and pattern.search(display_title):
                self._append_search_result(filename, None, f'{filename} [title match]')

            if not self.search_in_content_var.get():
                continue

            file_path = self.project_path / 'chapters' / filename
            if not file_path.exists():
                continue

            for line_number, line in enumerate(file_path.read_text(encoding='utf-8').splitlines(), start=1):
                if not pattern.search(line):
                    continue
                excerpt = line.strip() or '[blank line]'
                self._append_search_result(filename, line_number, f'{filename}:{line_number} - {excerpt[:90]}')
                if len(self.search_results) >= 100:
                    break
            if len(self.search_results) >= 100:
                break

        if self.search_results:
            self._set_status(f'Found {len(self.search_results)} search matches')
        else:
            self._set_status('No matches found')

    def _append_search_result(self, filename: str, line_number: int | None, label: str):
        self.search_results.append({'filename': filename, 'line_number': line_number})
        self.search_results_listbox.insert(tk.END, label)

    def clear_search(self):
        self.search_query_var.set('')
        self.search_results = []
        self.search_results_listbox.delete(0, tk.END)
        self._clear_search_highlight()
        self._set_status('Search cleared')

    def _open_selected_search_result(self, _event=None):
        selection = self.search_results_listbox.curselection()
        if not selection:
            return

        result = self.search_results[selection[0]]
        self.selected_filename = result['filename']
        self._load_chapter_list(select_filename=result['filename'])
        if result['line_number']:
            self._highlight_editor_line(result['line_number'])
            self.editor_text.see(f'{result["line_number"]}.0')
        self._set_status(f'Opened search result in {result["filename"]}')

    def _highlight_editor_line(self, line_number: int):
        self._clear_search_highlight()
        start = f'{line_number}.0'
        end = f'{line_number}.end'
        self.editor_text.tag_add('search_hit', start, end)

    def _clear_search_highlight(self):
        self.editor_text.tag_remove('search_hit', '1.0', tk.END)

    def _load_preview_css(self) -> str:
        css_path = Path(__file__).with_name('styles.css')
        return css_path.read_text(encoding='utf-8')

    def _render_preview_html(self, entries) -> str:
        css = self._load_preview_css()
        self._preview_anchors_by_file = {}

        if not entries:
            return (
                '<!DOCTYPE html><html><head><meta charset="utf-8">'
                f'<style>{css}</style></head><body><div class="document-shell">'
                '<section class="empty-state">No chapter content available.</section>'
                '</div></body></html>'
            )

        page_sections = []
        for index, entry in enumerate(entries, start=1):
            anchored_md, anchors = PreviewUtils.inject_block_anchors(entry.content, entry.filename)
            self._preview_anchors_by_file[entry.filename] = anchors
            markers = ChapterSettings.get_list_markers_by_level(self.assembler.get_config(), entry.filename)
            body = PreviewUtils.markdown_to_html_body_with_markers(anchored_md, list_markers_by_level=markers)
            page_sections.append(
                (
                    f'<section class="page" id="{self._chapter_anchor(entry.filename)}" '
                    f'data-page-label="Page {index}">'
                    f'{body}</section>'
                )
            )

        return (
            '<!DOCTYPE html><html><head><meta charset="utf-8">'
            f'<title>{html.escape(self.project_path.name)}</title><style>{css}</style>'
            '</head><body><div class="document-shell">'
            + ''.join(page_sections)
            + '</div></body></html>'
        )

    def _chapter_anchor(self, filename: str) -> str:
        slug = re.sub(r'[^a-zA-Z0-9]+', '-', filename).strip('-').lower()
        return f'chapter-{slug or "item"}'

    def _get_preview_fragment_from_editor(self) -> str | None:
        if not self.current_file:
            return None
        anchors = self._preview_anchors_by_file.get(self.current_file.name, [])
        local_line = self._get_editor_view_line_number()
        return PreviewUtils.find_anchor_for_line(anchors, local_line)

    def _scroll_html_preview_to_anchor(self, anchor_id: str | None):
        if not self._has_html_preview or not anchor_id:
            return

        try:
            element = self.preview_widget.document.getElementById(anchor_id)
            if element is None:
                return
            self._suppress_preview_sync = True
            element.scrollIntoView()
            self.after(150, self._clear_preview_sync_suppression)
        except Exception:
            pass

    def refresh_preview(self):
        if self._preview_after_id is not None:
            self.after_cancel(self._preview_after_id)
            self._preview_after_id = None

        try:
            _final_md, entries = self.assembler.assemble_with_metadata()
            target_fraction = self._forced_preview_fraction
            if target_fraction is None:
                target_fraction = self._get_preview_scroll_fraction_from_editor(entries)
            if self._has_html_preview:
                html_source = self._render_preview_html(entries)
                target_fragment = self._get_preview_fragment_from_editor()
                self.preview_widget.load_html(html_source, fragment=target_fragment)
            else:
                self.preview_widget.config(state='normal')
                self.preview_widget.delete('1.0', 'end')
                for entry in entries:
                    markers = ChapterSettings.get_list_markers_by_level(self.assembler.get_config(), entry.filename)
                    PreviewUtils.render_markdown_to_preview_widget(
                        self.preview_widget,
                        entry.content,
                        list_markers_by_level=markers,
                        append=True,
                    )
                    self.preview_widget.config(state='normal')
                    self.preview_widget.insert('end', '\n')
                self.preview_widget.config(state='disabled')
        except Exception as exc:
            self._set_status(f'Preview error: {exc}')
            return

        if self._has_html_preview:
            self._last_preview_fraction = self._get_preview_yview_fraction()
        else:
            self._apply_preview_scroll_fraction(target_fraction)
        self._forced_preview_fraction = None
        self._set_status('Preview updated')

    def build_docx(self):
        self.save_current_file()

        try:
            md_out_path = self.project_path / 'assembled.md'
            self.assembler.save_assembled_for_export(md_out_path)

            builder = DocxBuilder(self.project_path)
            img_cache_dir = self.project_path / '.diagram_cache'
            builder.build_from_markdown(str(md_out_path), img_cache_dir)

            output_docx = self.project_path / f'{self.project_path.name}.docx'
            builder.save(output_docx)
        except Exception as exc:
            messagebox.showerror('Build DOCX', str(exc), parent=self)
            self._set_status(f'Build failed: {exc}')
            return

        self._set_status(f'Built {output_docx.name}')
        messagebox.showinfo('Build DOCX', f'DOCX saved to:\n{output_docx}', parent=self)

    def _start_file_watch(self):
        self._poll_for_external_changes()

    def _poll_for_external_changes(self):
        try:
            for file_path in self.assembler.get_chapter_paths():
                if not file_path.exists():
                    continue
                current_mtime = file_path.stat().st_mtime
                known_mtime = self._known_mtimes.get(file_path)
                if known_mtime is None:
                    self._known_mtimes[file_path] = current_mtime
                    continue
                if current_mtime <= known_mtime:
                    continue

                self._known_mtimes[file_path] = current_mtime
                if file_path != self.current_file:
                    self.refresh_preview()
                    continue

                if self._is_dirty:
                    self._set_status(f'External change detected for {file_path.name}; local edits kept')
                else:
                    self._read_current_file_into_editor()
                    self.refresh_preview()
                    self._set_status(f'Reloaded {file_path.name} after external update')
        finally:
            self._watch_after_id = self.after(self.WATCH_INTERVAL_MS, self._poll_for_external_changes)

    def _set_status(self, message: str):
        self.status_var.set(message)

    def _refresh_title(self):
        dirty_suffix = ' *' if self._is_dirty else ''
        self.title(f'Visual Builder - {self.project_path.name}{dirty_suffix}')

    def _on_close(self):
        self.save_current_file()
        for after_id in (
            self._preview_after_id,
            self._autosave_after_id,
            self._highlight_after_id,
            self._preview_sync_after_id,
            self._watch_after_id,
        ):
            if after_id is not None:
                try:
                    self.after_cancel(after_id)
                except Exception:
                    pass
        self.destroy()
