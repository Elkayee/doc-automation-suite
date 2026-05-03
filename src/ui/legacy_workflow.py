"""
make.py — Tool duy nhat: Ghep chapters -> MD -> convert DOCX
Usage: uv run python make.py
"""

import argparse
import os
import sys
from pathlib import Path

from src.core.assembler import DocumentAssembler
from src.core.docx_builder import DocxBuilder
from src.core.markdown_utils import MarkdownUtils
from src.ui.preview_utils import PreviewUtils
import src.core.docx_helpers
from src.core.media_downloader import MediaDownloader
import split_chapters
from convert_docx_to_md import convert_docx_to_markdown

sys.stdout.reconfigure(encoding='utf-8')

# ── CONFIG ───────────────────────────────────────────────────────────────────
BASE = Path(__file__).resolve().parent
CH_DIR = str(BASE / 'chapters')
MD_OUT = str(BASE / 'Bao_Cao_Tieu_Luan_NMCNPM.md')
DOCX_OUT = str(BASE / 'Bao_Cao_Tieu_Luan_NMCNPM.docx')
IMG_CACHE = str(BASE / 'diagram_cache')
os.makedirs(IMG_CACHE, exist_ok=True)

# Danh sách chapter chính thức dùng để build báo cáo.
# Các file Ch*.md khác trong thư mục chapters được giữ lại để tham chiếu,
# nhưng không được ghép vào báo cáo để tránh trùng/lặp chương.
BUILD_CHAPTER_FILES = [
    'F00_header.md',
    'F01_toc.md',
    'Ch01_LỜI_MỞ_ĐẦU.md',
    'Ch02_MỞ_ĐẦU_KẾ_HOẠCH_QUẢN_LÝ_DỰ_ÁN_PHẦN_MỀM_.md',
    'Ch03_CHƯƠNG_1_TỔNG_QUAN_HỆ_THỐNG_VÀ_PHÂN_CÔN.md',
    'Ch04_CHƯƠNG_2_THIẾT_KẾ_KIẾN_TRÚC_VÀ_CƠ_SỞ_DỮ.md',
    'Ch05_CHƯƠNG_3_NGHIÊN_CỨU_CHUYÊN_SÂU_—_USE_CA.md',
    'Ch06_CHƯƠNG_4_NGHIÊN_CỨU_CHUYÊN_SÂU_—_USE_CA.md',
    'Ch07_CHƯƠNG_5_NGHIÊN_CỨU_CHUYÊN_SÂU_—_USE_CA.md',
    'Ch08_CHƯƠNG_6_NGHIÊN_CỨU_CHUYÊN_SÂU_—_USE_CA.md',
    'Ch09_CHƯƠNG_7_NGHIÊN_CỨU_CHUYÊN_SÂU_—_USE_CA.md',
    'Ch10_CHƯƠNG_8_NGHIÊN_CỨU_CHUYÊN_SÂU_—_USE_CA.md',
    'Ch11_CHƯƠNG_9_NGHIÊN_CỨU_CHUYÊN_SÂU_—_USE_CA.md',
    'Ch12_KẾT_LUẬN.md',
    'Ch13_TÀI_LIỆU_THAM_KHẢO.md',
]

# ── MÀUSẮC ───────────────────────────────────────────────────────────────────
from docx.shared import RGBColor
COLOR_H1 = RGBColor(0x1A, 0x3A, 0x5C)
COLOR_H2 = RGBColor(0x1F, 0x61, 0x9E)
COLOR_H3 = RGBColor(0x2E, 0x86, 0xAB)
COLOR_H4 = RGBColor(0x44, 0x9D, 0xD1)


# ════════════════════════════════════════════════════════════════════════════
# BƯỚC 1: GỘP CHAPTERS → MD
# ════════════════════════════════════════════════════════════════════════════
def chapter_sort_key(file_path):
    name = os.path.basename(file_path)
    lower_name = name.lower()

    if lower_name == 'f00_header.md':
        return (0, 0, '')
    if lower_name == 'f01_toc.md':
        return (0, 1, '')

    match = re.match(r'^Ch(\d+)(.*)\.md$', name, re.IGNORECASE)
    if not match:
        return (99, 99, lower_name)

    return (1, int(match.group(1)), match.group(2).lower())


def collect_chapter_files(chapter_dir):
    chapter_dir_path = Path(chapter_dir)
    chapter_dir_path.mkdir(parents=True, exist_ok=True)
    chapter_files = []

    for filename in BUILD_CHAPTER_FILES:
        file_path = chapter_dir_path / filename
        if not file_path.exists():
            file_path.write_text(f'# {filename.replace(".md", "")}\n\nNoi dung mau...\n', encoding='utf-8')
            print(f'  [INFO] Da tao file mau: {filename}')
        chapter_files.append(str(file_path))

    return chapter_files


def clear_image_cache(img_cache):
    cache_path = Path(img_cache)
    if not cache_path.exists():
        cache_path.mkdir(parents=True, exist_ok=True)
        return

    for entry in cache_path.iterdir():
        if entry.is_file():
            entry.unlink()
        elif entry.is_dir():
            shutil.rmtree(entry)


def ensure_output_docx_closed(docx_out):
    output_path = Path(docx_out)
    if not output_path.exists():
        return

    probe_path = output_path.with_name(output_path.stem + '.__lockcheck__' + output_path.suffix)
    try:
        os.replace(output_path, probe_path)
        os.replace(probe_path, output_path)
    except PermissionError as exc:
        if probe_path.exists():
            try:
                os.replace(probe_path, output_path)
            except OSError:
                pass
        raise RuntimeError(
            f'File output dang mo: {output_path.name}. Hay dong file Word cu truoc khi build lai.'
        ) from exc


from src.core.assembler import DocumentAssembler

def assemble_markdown(chapter_dir, output_path):
    assembler = DocumentAssembler(Path(chapter_dir).parent)
    final, processed_files = assembler.save_assembled(Path(output_path))

    for file_path in processed_files:
        with open(file_path, encoding='utf-8') as handle:
            content = handle.read().strip()
        print(f'  [OK] {os.path.basename(file_path)}  ({len(content.splitlines())} dong)')

    return final, processed_files


def step_assemble():
    print('=' * 55)
    print('BƯỚC 1: Ghép chapters → MD')
    print('=' * 55)

    final, chapter_files = assemble_markdown(CH_DIR, MD_OUT)

    kb = len(final.encode('utf-8')) // 1024
    print(f'\n  => {MD_OUT}')
    print(f'     {len(final.splitlines())} dong | {kb} KB | {len(chapter_files)} chapters\n')


# ════════════════════════════════════════════════════════════════════════════
# BƯỚC 2: CONVERT MD → DOCX
# ════════════════════════════════════════════════════════════════════════════


# ── Diagram render ───────────────────────────────────────────────────────────
# Removed image dimension logic, plantuml render, latex render, all replaced by MediaDownloader

# ── DOCX helpers ─────────────────────────────────────────────────────────────
# Removed duplicate docx helpers, now using src.core.docx_helpers

# ── Parser MD → DOCX ─────────────────────────────────────────────────────────
# Removed duplicate parsing logic, now using src.core.docx_builder

def step_convert(md_out=MD_OUT, docx_out=DOCX_OUT, img_cache=IMG_CACHE):
    print('=' * 55)
    print('BƯỚC 2: Convert MD → DOCX')
    print('=' * 55)
    print(f'  Input : {md_out}')
    print(f'  Output: {docx_out}')
    print()

    builder = DocxBuilder(BASE) # BASE is the original workspace
    builder.build_from_markdown(str(md_out), Path(img_cache))

    out = docx_out
    try:
        builder.save(Path(out))
    except Exception as exc:
        raise RuntimeError(
            f'Khong the ghi file {Path(docx_out).name}. Hay dong file Word cu truoc khi build lai.'
        ) from exc

    size = os.path.getsize(out) // 1024
    print(f'\n[DONE] {out}  ({size} KB)')
    print('  => Mo file Word va dong lai neu can dung ten goc.')
    return out


def run_build_pipeline(chapters_dir=CH_DIR, md_out=MD_OUT, docx_out=DOCX_OUT, img_cache=IMG_CACHE):
    os.makedirs(img_cache, exist_ok=True)
    print('  [INFO] Dang xoa cache anh cu de lay du lieu render/API moi...')
    clear_image_cache(img_cache)
    print('=' * 55)
    print('BƯỚC 1: Ghép chapters → MD')
    print('=' * 55)
    final, chapter_files = assemble_markdown(chapters_dir, md_out)
    kb = len(final.encode('utf-8')) // 1024
    print(f'\n  => {md_out}')
    print(f'     {len(final.splitlines())} dong | {kb} KB | {len(chapter_files)} chapters\n')
    saved_path = step_convert(md_out=md_out, docx_out=docx_out, img_cache=img_cache)
    return Path(saved_path)


def launch_workflow_ui():
    import tkinter as tk
    from tkinter import filedialog, messagebox, ttk

    root = tk.Tk()
    root.title('NMCNPM Workflow')
    root.geometry('1400x720')  # Rộng hơn để chứa live preview panel
    root.configure(bg='#f3efe5')

    style = ttk.Style()
    style.theme_use('clam')
    style.configure('TFrame', background='#f3efe5')
    style.configure('TLabel', background='#f3efe5', foreground='#2b241b', font=('Georgia', 11))
    style.configure('Header.TLabel', background='#f3efe5', foreground='#1f3f5b', font=('Georgia', 18, 'bold'))
    style.configure('TButton', font=('Georgia', 10, 'bold'))
    style.configure('TNotebook', background='#f3efe5', borderwidth=0)
    style.configure('TNotebook.Tab', font=('Georgia', 10, 'bold'))

    container = ttk.Frame(root, padding=18)
    container.pack(fill='both', expand=True)

    ttk.Label(container, text='NMCNPM Report Workflow', style='Header.TLabel').pack(anchor='w')
    ttk.Label(
        container,
        text='Thiết lập đường dẫn và chạy các bước build, split, convert ngay trong một UI cục bộ.',
    ).pack(anchor='w', pady=(4, 14))

    notebook = ttk.Notebook(container)
    notebook.pack(fill='both', expand=True)

    log_box = tk.Text(container, height=10, bg='#fffdf8', fg='#2b241b', font=('Consolas', 10))
    log_box.pack(fill='x', pady=(14, 0))

    def log(message):
        log_box.insert('end', message + '\n')
        log_box.see('end')
        root.update_idletasks()

    def add_path_row(parent, label, variable, browse_kind, filetypes=None):
        row = ttk.Frame(parent)
        row.pack(fill='x', pady=6)
        ttk.Label(row, text=label, width=18).pack(side='left')
        entry = ttk.Entry(row, textvariable=variable)
        entry.pack(side='left', fill='x', expand=True, padx=(0, 8))

        def choose():
            if browse_kind == 'dir':
                value = filedialog.askdirectory(initialdir=str(BASE))
            elif browse_kind == 'save':
                value = filedialog.asksaveasfilename(initialdir=str(BASE), filetypes=filetypes)
            else:
                value = filedialog.askopenfilename(initialdir=str(BASE), filetypes=filetypes)
            if value:
                variable.set(value)

        ttk.Button(row, text='Browse', command=choose).pack(side='left')
        return entry

    editor_tab = ttk.Frame(notebook, padding=14)
    build_tab = ttk.Frame(notebook, padding=14)
    split_tab = ttk.Frame(notebook, padding=14)
    convert_tab = ttk.Frame(notebook, padding=14)
    notebook.add(editor_tab, text='Editor')
    notebook.add(build_tab, text='Build DOCX')
    notebook.add(split_tab, text='Split Chapters')
    notebook.add(convert_tab, text='DOCX → MD')

    # ── Kiểm tra tkinterweb ──────────────────────────────────────────────────
    _htmlframe_error = None
    try:
        from tkinterweb import HtmlFrame as _HtmlFrame

        _has_htmlframe = True
    except Exception as exc:
        _has_htmlframe = False
        _htmlframe_error = str(exc)

    # --- EDITOR TAB ---
    # Bố cục: [Listbox file | Editor text | Preview panel]
    editor_paned = ttk.PanedWindow(editor_tab, orient=tk.HORIZONTAL)
    editor_paned.pack(fill='both', expand=True)

    # Cột 1: Danh sách file
    file_list_frame = ttk.Frame(editor_paned)
    editor_paned.add(file_list_frame, weight=1)

    # Cột 2: Editor text
    editor_frame = ttk.Frame(editor_paned)
    editor_paned.add(editor_frame, weight=3)

    # Cột 3: Live preview
    preview_frame = ttk.Frame(editor_paned)
    editor_paned.add(preview_frame, weight=3)

    # -- Listbox --
    file_listbox = tk.Listbox(file_list_frame, font=('Consolas', 10))
    file_listbox.pack(side='left', fill='both', expand=True)
    scrollbar = ttk.Scrollbar(file_list_frame, orient='vertical', command=file_listbox.yview)
    scrollbar.pack(side='right', fill='y')
    file_listbox.config(yscrollcommand=scrollbar.set)

    # -- Editor --
    editor_text = tk.Text(editor_frame, font=('Consolas', 11), wrap='word', undo=True)
    editor_text.pack(fill='both', expand=True, pady=(0, 5))

    btn_frame = ttk.Frame(editor_frame)
    btn_frame.pack(fill='x')

    # -- Live preview widget --
    ttk.Label(preview_frame, text='Live Preview', font=('Georgia', 10, 'bold')).pack(anchor='w', padx=6, pady=(0, 4))
    if _has_htmlframe:
        # Dùng HtmlFrame (tkinterweb) — render HTML thực sự
        live_preview = _HtmlFrame(preview_frame, messages_enabled=False)
        live_preview.pack(fill='both', expand=True)

        def _update_preview_widget(html_content):
            live_preview.load_html(html_content)
    else:
        # Fallback: tk.Text hiển thị nội dung thô (chỉ dùng khi tkinterweb chưa cài)
        preview_text = tk.Text(
            preview_frame, font=('Consolas', 10), wrap='word', bg='#fffdf8', fg='#2b241b', state='disabled'
        )
        preview_text.pack(fill='both', expand=True)
        PreviewUtils.configure_preview_text_tags(preview_text)
        ttk.Label(
            preview_frame,
            text=(
                'Đang dùng fallback preview trong ứng dụng.\n'
                'Muốn render HTML đầy đủ: cài `tkinterweb` vào đúng Python đang chạy UI.\n'
                f'Python hiện tại: {sys.executable}\n'
                + (f'Lý do không tải được HtmlFrame: {_htmlframe_error}' if _htmlframe_error else '')
            ),
            foreground='#888',
            font=('Consolas', 9),
        ).pack(anchor='w', padx=6)

        def _update_preview_widget(html_content):
            # Fallback: render markdown có style ngay trong Text widget
            PreviewUtils.render_markdown_to_preview_widget(preview_text, editor_text.get(1.0, tk.END))

    # -- Debounce timer cho live preview --
    _preview_after_id = [None]  # dùng list để có thể thay đổi trong closure

    def _build_preview_html():
        """Tạo HTML đầy đủ từ nội dung editor hiện tại."""
        content = editor_text.get(1.0, tk.END)
        filepath = current_file.get()
        body = PreviewUtils.markdown_to_html_body(content)
        fname = os.path.basename(filepath) if filepath else 'Preview'
        css = """
body { font-family: 'Segoe UI', Arial, sans-serif; padding: 20px 32px;
       line-height: 1.7; color: #222; max-width: 860px; margin: auto; }
h1 { color: #1A3A5C; font-size: 1.7em; border-bottom: 2px solid #1F619E; padding-bottom: 5px; }
h2 { color: #1F619E; font-size: 1.35em; }
h3 { color: #2E86AB; font-size: 1.15em; }
h4 { color: #449DD1; }
pre { background:#f4f4f4; padding:10px; border-radius:5px; overflow-x:auto;
      font-family: Consolas, monospace; font-size: 0.9em; }
code { background:#f0f0f0; padding:2px 4px; border-radius:3px; font-size:0.9em; }
table { border-collapse: collapse; width: 100%; margin: 12px 0; }
th { background-color: #1F619E; color: white; padding: 7px 10px; text-align: left; }
td { border: 1px solid #d0d0d0; padding: 6px 10px; }
tr:nth-child(even) td { background: #EBF4FB; }
blockquote { border-left: 4px solid #449DD1; margin-left:0; padding-left:14px; color:#555; }
img { max-width: 100%; height: auto; display: block; margin: 8px auto; }
.diagram { text-align: center; }
"""
        return f"""<!DOCTYPE html>
<html lang="vi">
<head><meta charset="utf-8"><title>{fname}</title><style>{css}</style></head>
<body>{body}</body>
</html>"""

    def _do_live_preview():
        """Được gọi sau debounce — render và cập nhật preview."""
        try:
            html_content = _build_preview_html()
            _update_preview_widget(html_content)
        except Exception:
            pass  # Không để lỗi render crash UI
        _preview_after_id[0] = None

    def _on_editor_change(event=None):
        """Debounce 800ms: chỉ render sau khi ngừng gõ."""
        if _preview_after_id[0] is not None:
            root.after_cancel(_preview_after_id[0])
        _preview_after_id[0] = root.after(800, _do_live_preview)

    # Gắn sự kiện gõ phím vào editor
    editor_text.bind('<KeyRelease>', _on_editor_change)

    current_file = tk.StringVar()

    def load_files():
        file_listbox.delete(0, tk.END)
        for f in collect_chapter_files(CH_DIR):
            file_listbox.insert(tk.END, os.path.basename(f))

    def on_file_select(event):
        if not file_listbox.curselection():
            return
        idx = file_listbox.curselection()[0]
        filename = file_listbox.get(idx)
        filepath = os.path.join(CH_DIR, filename)
        current_file.set(filepath)
        try:
            with open(filepath, encoding='utf-8') as f:
                editor_text.delete(1.0, tk.END)
                editor_text.insert(tk.END, f.read())
            # Render ngay khi mở file mới
            _do_live_preview()
        except Exception as e:
            log(f'Lỗi đọc file: {e}')

    file_listbox.bind('<<ListboxSelect>>', on_file_select)

    def save_file():
        filepath = current_file.get()
        if filepath:
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(editor_text.get(1.0, tk.END).rstrip('\n') + '\n')
                log(f'Đã lưu: {os.path.basename(filepath)}')
            except Exception as e:
                log(f'Lỗi lưu file: {e}')

    def preview_file():
        filepath = current_file.get()
        if not filepath:
            messagebox.showwarning('Cảnh báo', 'Vui lòng chọn file để preview!')
            return
        import tempfile
        import webbrowser

        content = editor_text.get(1.0, tk.END)
        body = PreviewUtils.markdown_to_html_body(content)
        css = """
body { font-family: 'Segoe UI', Arial, sans-serif; padding: 28px 48px;
       line-height: 1.7; color: #222; max-width: 860px; margin: auto; }
h1 { color: #1A3A5C; font-size: 1.8em; border-bottom: 2px solid #1F619E; padding-bottom: 6px; }
h2 { color: #1F619E; font-size: 1.4em; }
h3 { color: #2E86AB; font-size: 1.2em; }
h4 { color: #449DD1; }
pre { background:#f4f4f4; padding:12px; border-radius:6px; overflow-x:auto;
      font-family: Consolas, monospace; font-size: 0.92em; }
code { background:#f0f0f0; padding:2px 5px; border-radius:3px; font-size:0.92em; }
table { border-collapse: collapse; width: 100%; margin: 14px 0; }
th { background-color: #1F619E; color: white; padding: 8px 12px; text-align: left; }
td { border: 1px solid #d0d0d0; padding: 7px 12px; }
tr:nth-child(even) td { background: #EBF4FB; }
blockquote { border-left: 4px solid #449DD1; margin-left:0; padding-left:16px; color:#555; }
img { max-width: 100%; }
.diagram { text-align: center; }
.diagram img { max-width: 100%; height: auto; }
"""
        html_content = f"""<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="utf-8">
  <title>Preview — {os.path.basename(filepath)}</title>
  <style>{css}</style>
</head>
<body>
{body}
</body>
</html>"""
        fd, temp_path = tempfile.mkstemp(suffix='.html')
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            f.write(html_content)
        webbrowser.open('file:///' + temp_path.replace('\\', '/'))
        log(f'Preview: {os.path.basename(filepath)}')

    def docx_to_chapters():
        docx_path = filedialog.askopenfilename(initialdir=str(BASE), filetypes=[('Word', '*.docx')])
        if not docx_path:
            return
        log('Đang tách DOCX -> Markdown...')
        try:
            tmp_md = str(BASE / 'temp_split.md')
            convert_docx_to_markdown(docx_path, tmp_md, str(BASE / 'extracted_media' / 'temp_split'))
            split_chapters.write_chapter_files(tmp_md, CH_DIR)
            if os.path.exists(tmp_md):
                os.remove(tmp_md)
            log('Tách thành công!')
            load_files()
            messagebox.showinfo('Thành công', 'Đã tách DOCX thành các chapters.')
        except Exception as e:
            log(f'Lỗi: {e}')

    ttk.Button(btn_frame, text='Lưu (Save)', command=save_file).pack(side='left', padx=5)
    ttk.Button(btn_frame, text='Mở Preview (Browser)', command=preview_file).pack(side='left', padx=5)
    ttk.Button(btn_frame, text='Tải lại danh sách', command=load_files).pack(side='left', padx=5)
    ttk.Button(btn_frame, text='Tách DOCX -> Chapters', command=docx_to_chapters).pack(side='right', padx=5)

    load_files()

    build_chapters = tk.StringVar(value=CH_DIR)
    build_md = tk.StringVar(value=MD_OUT)
    build_docx = tk.StringVar(value=DOCX_OUT)
    build_cache = tk.StringVar(value=IMG_CACHE)

    add_path_row(build_tab, 'Chapters dir', build_chapters, 'dir')
    add_path_row(build_tab, 'Output MD', build_md, 'save', [('Markdown', '*.md')])
    add_path_row(build_tab, 'Output DOCX', build_docx, 'save', [('Word Document', '*.docx')])
    add_path_row(build_tab, 'Diagram cache', build_cache, 'dir')

    build_res_frame = ttk.Frame(build_tab)
    build_res_frame.pack(anchor='w', pady=(10, 0))

    def do_build():
        res = run_ui_action(
            root,
            log,
            lambda: run_build_pipeline(
                chapters_dir=build_chapters.get(),
                md_out=build_md.get(),
                docx_out=build_docx.get(),
                img_cache=build_cache.get(),
            ),
            'Build hoàn tất.',
        )
        if res:
            btn_open_file.pack(side='left', padx=5)
            btn_open_folder.pack(side='left', padx=5)

    ttk.Button(build_tab, text='Run Build Pipeline', command=do_build).pack(anchor='w', pady=(14, 0))

    btn_open_file = ttk.Button(build_res_frame, text='Mở file Word', command=lambda: os.startfile(build_docx.get()))
    btn_open_folder = ttk.Button(
        build_res_frame,
        text='Mở thư mục chứa',
        command=lambda: os.startfile(os.path.dirname(os.path.abspath(build_docx.get()))),
    )

    split_source = tk.StringVar(value=MD_OUT)
    split_output = tk.StringVar(value=str(BASE / 'chapters'))
    add_path_row(split_tab, 'Source MD', split_source, 'open', [('Markdown', '*.md')])
    add_path_row(split_tab, 'Output dir', split_output, 'dir')
    ttk.Button(
        split_tab,
        text='Split Markdown',
        command=lambda: run_ui_action(
            root,
            log,
            lambda: split_chapters.write_chapter_files(split_source.get(), split_output.get()),
            'Tách chapter hoàn tất.',
        ),
    ).pack(anchor='w', pady=(14, 0))

    convert_input = tk.StringVar(value=DOCX_OUT)
    convert_output = tk.StringVar(value=str(BASE / 'Bao_Cao_Tieu_Luan_NMCNPM_from_docx.md'))
    convert_media = tk.StringVar(value=str(BASE / 'extracted_media' / 'Bao_Cao_Tieu_Luan_NMCNPM'))
    add_path_row(convert_tab, 'Input DOCX', convert_input, 'open', [('Word Document', '*.docx')])
    add_path_row(convert_tab, 'Output MD', convert_output, 'save', [('Markdown', '*.md')])
    add_path_row(convert_tab, 'Media dir', convert_media, 'dir')
    ttk.Button(
        convert_tab,
        text='Convert DOCX to Markdown',
        command=lambda: run_ui_action(
            root,
            log,
            lambda: convert_docx_to_markdown(convert_input.get(), convert_output.get(), convert_media.get()),
            'Convert DOCX → Markdown hoàn tất.',
        ),
    ).pack(anchor='w', pady=(14, 0))

    messagebox.showinfo(
        'NMCNPM Workflow',
        'UI đã sẵn sàng. Bạn có thể thiết lập đường dẫn file/folder và chạy từng bước ngay tại đây.',
    )
    root.mainloop()


def run_ui_action(root, log, action, success_message):
    try:
        log('---')
        result = action()
        log(f'OK: {result}')
        from tkinter import messagebox

        messagebox.showinfo('NMCNPM Workflow', success_message)
        return result
    except Exception as exc:
        log(f'ERROR: {exc}')
        from tkinter import messagebox

        messagebox.showerror('NMCNPM Workflow', str(exc))


def parse_args():
    parser = argparse.ArgumentParser(description='NMCNPM report workflow')
    parser.add_argument('--ui', action='store_true', help='Launch local workflow UI')
    parser.add_argument('--chapters-dir', default=CH_DIR)
    parser.add_argument('--md-out', default=MD_OUT)
    parser.add_argument('--docx-out', default=DOCX_OUT)
    parser.add_argument('--img-cache', default=IMG_CACHE)
    return parser.parse_args()


# ════════════════════════════════════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════════════════════════════════════
if __name__ == '__main__':
    args = parse_args()
    if args.ui:
        launch_workflow_ui()
    else:
        run_build_pipeline(
            chapters_dir=args.chapters_dir,
            md_out=args.md_out,
            docx_out=args.docx_out,
            img_cache=args.img_cache,
        )
