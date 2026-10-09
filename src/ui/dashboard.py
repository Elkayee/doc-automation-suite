import os
import shutil
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from src.core.project_paths import workspace_path
from src.core.renderers import renderer_status
from src.core.runtime import VERSION, data_root
from src.core.template_manager import TemplateManager
from src.ui.theme import BACKGROUND, INK, MUTED, apply_theme
from src.ui.visual_builder import VisualBuilderWindow


class DashboardApp:
    def __init__(self, root, base_dir: Path):
        self.root = root
        self.base_dir = base_dir
        self.template_manager = TemplateManager(base_dir / 'templates')
        self.workspaces_dir = data_root(base_dir) / 'workspaces'
        self.workspaces_dir.mkdir(parents=True, exist_ok=True)
        self.root.title('Doc Automation Suite — Văn bản và báo cáo')
        self.root.geometry('1100x720')
        self.root.minsize(960, 640)
        self.root.configure(bg=BACKGROUND)
        apply_theme(root)
        icon = base_dir / 'assets' / 'app.png'
        if icon.is_file():
            self.icon = tk.PhotoImage(file=icon)
            root.iconphoto(True, self.icon)
        self._build_ui()
        self.root.protocol('WM_DELETE_WINDOW', self._on_close)
        self.root.bind('<Control-n>', lambda _event: self.show_create_dialog())
        self.root.bind('<Control-o>', lambda _event: self.open_project())

    def _on_close(self):
        builders = [child for child in self.root.winfo_children() if isinstance(child, VisualBuilderWindow)]
        for builder in builders:
            builder._on_close()
            if builder.winfo_exists():
                return
        self.root.destroy()

    def _build_ui(self):
        sidebar = tk.Frame(self.root, bg=INK, width=218)
        sidebar.pack(side='left', fill='y')
        sidebar.pack_propagate(False)
        tk.Label(sidebar, text='DOC SUITE', font=('Segoe UI', 19, 'bold'), fg='white', bg=INK).pack(
            anchor='w', padx=24, pady=(32, 3)
        )
        tk.Label(sidebar, text='Không gian soạn tài liệu', fg='#bdcce3', bg=INK, font=('Segoe UI', 10)).pack(
            anchor='w', padx=24, pady=(0, 34)
        )
        for label, action in [
            ('Tạo báo cáo mới', self.show_create_dialog),
            ('Mở dự án', self.open_project),
            ('Thư mục tài liệu', self.open_workspaces),
            ('Công cụ chuyển đổi', self.open_legacy_workflow),
        ]:
            ttk.Button(sidebar, text=label, command=action, style='Nav.TButton').pack(fill='x', padx=12, pady=3)
        ttk.Button(sidebar, text='Thông tin ứng dụng', command=self.show_about, style='Nav.TButton').pack(
            side='bottom', fill='x', padx=12, pady=16
        )
        tk.Label(sidebar, text=f'Phiên bản {VERSION}  ·  Windows', fg='#bdcce3', bg=INK, anchor='w').pack(
            side='bottom', fill='x', padx=24, pady=8
        )
        main = ttk.Frame(self.root, padding=(30, 26))
        main.pack(side='left', fill='both', expand=True)
        header = ttk.Frame(main)
        header.pack(fill='x')
        ttk.Label(header, text='Tài liệu của bạn', style='Title.TLabel').pack(side='left')
        ttk.Button(header, text='+ Tạo báo cáo', command=self.show_create_dialog, style='Primary.TButton').pack(
            side='right', pady=4
        )
        ttk.Label(main, text='Từ đề cương đến bản Word/PDF hoàn chỉnh.', style='Muted.TLabel').pack(
            anchor='w', pady=(8, 26)
        )
        ttk.Label(main, text='BẮT ĐẦU TỪ MẪU', style='Section.TLabel').pack(anchor='w', pady=(0, 12))
        cards = ttk.Frame(main)
        cards.pack(fill='x')
        templates = [
            ('bao_cao_bai_tap_lon', 'Bài tập lớn', 'Bìa, chương, mục lục\nvà tài liệu tham khảo.'),
            ('bao_cao_cong_so', 'Báo cáo công sở', 'Kết quả, bảng số liệu\nvà kiến nghị thực hiện.'),
            ('bien_ban', 'Biên bản', 'Thông tin cuộc họp\nvà nội dung thống nhất.'),
        ]
        for column, (key, title, description) in enumerate(templates):
            cards.columnconfigure(column, weight=1, uniform='cards')
            card = ttk.Frame(cards, style='Card.TFrame', padding=18)
            card.grid(row=0, column=column, sticky='nsew', padx=(0, 10 if column < 2 else 0))
            ttk.Label(card, text=title, style='Card.TLabel', font=('Segoe UI', 12, 'bold')).pack(anchor='w')
            ttk.Label(card, text=description, style='Card.TLabel', foreground=MUTED).pack(anchor='w', pady=(10, 18))
            ttk.Button(card, text='Dùng mẫu', command=lambda template=key: self.show_create_dialog(template)).pack(
                anchor='w'
            )
        row = ttk.Frame(main)
        row.pack(fill='x', pady=(28, 12))
        ttk.Label(row, text='DỰ ÁN HIỆN CÓ', style='Section.TLabel').pack(side='left')
        ttk.Button(row, text='Mở', command=self.open_selected_project).pack(side='right')
        ttk.Button(row, text='Xóa', command=self.delete_selected_project).pack(side='right', padx=8)
        self.list_container = ttk.Frame(main, style='Card.TFrame')
        self.list_container.pack(fill='both', expand=True)
        self.projects_list = tk.Listbox(
            self.list_container,
            font=('Segoe UI', 11),
            height=8,
            bg='white',
            fg=INK,
            selectbackground='#e1eaff',
            selectforeground=INK,
            highlightcolor='#2457d6',
            highlightthickness=1,
            relief='flat',
            borderwidth=0,
            activestyle='dotbox',
        )
        self.projects_list.bind('<Double-1>', lambda _event: self.open_selected_project())
        self.projects_list.bind('<Return>', lambda _event: self.open_selected_project())
        self.empty_label = ttk.Label(
            self.list_container, text='Chưa có dự án. Chọn một mẫu để bắt đầu.', style='Card.TLabel', foreground=MUTED
        )
        self.refresh_projects()
        status = ttk.Frame(main)
        status.pack(fill='x', pady=(16, 0))
        tools = renderer_status()
        ready = all(tools.get(name) for name in ('libreoffice', 'pandoc'))
        ttk.Label(
            status,
            text='Word & PDF sẵn sàng' if ready else 'Kiểm tra bộ xuất trong Thông tin ứng dụng',
            foreground='#22613e' if ready else '#81561b',
        ).pack(side='left')
        ttk.Label(status, text='Ctrl+N: tạo mới   ·   Ctrl+O: mở dự án', style='Muted.TLabel').pack(side='right')

    def refresh_projects(self):
        self.projects_list.delete(0, tk.END)
        for entry in sorted(self.workspaces_dir.iterdir(), key=lambda path: path.name.casefold()):
            if entry.is_dir() and (entry / 'config.yaml').exists():
                self.projects_list.insert(tk.END, entry.name)
        if self.projects_list.size():
            self.empty_label.pack_forget()
            self.projects_list.pack(fill='both', expand=True, padx=12, pady=12)
        else:
            self.projects_list.pack_forget()
            self.empty_label.pack(expand=True, pady=28)

    def show_create_dialog(self, template_key='bao_cao_bai_tap_lon'):
        dialog = tk.Toplevel(self.root)
        dialog.title('Tạo báo cáo mới')
        dialog.geometry('540x380')
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.configure(bg=BACKGROUND)
        content = ttk.Frame(dialog, padding=28)
        content.pack(fill='both', expand=True)
        ttk.Label(content, text='Bắt đầu báo cáo', font=('Segoe UI', 18, 'bold')).pack(anchor='w', pady=(0, 18))
        ttk.Label(content, text='Tên dự án').pack(anchor='w', pady=(0, 6))
        name_var = tk.StringVar()
        name_entry = ttk.Entry(content, textvariable=name_var)
        name_entry.pack(fill='x')
        ttk.Label(content, text='Mẫu tài liệu').pack(anchor='w', pady=(18, 6))
        templates = self.template_manager.list_templates()
        labels = {config.name: key for key, config in templates.items()}
        template_var = tk.StringVar(
            value=next((label for label, key in labels.items() if key == template_key), next(iter(labels), ''))
        )
        ttk.Combobox(content, textvariable=template_var, values=list(labels), state='readonly').pack(fill='x')
        ttk.Label(
            content, text='Thông tin bìa và nội dung được chỉnh trong trình soạn.', style='Muted.TLabel', wraplength=460
        ).pack(anchor='w', pady=14)

        def do_create():
            name, template = name_var.get().strip(), labels.get(template_var.get())
            if not name or not template:
                messagebox.showerror('Thiếu thông tin', 'Nhập tên dự án và chọn mẫu tài liệu.', parent=dialog)
                return
            try:
                dest = workspace_path(self.workspaces_dir, name)
                if dest.exists():
                    raise ValueError('Tên dự án đã tồn tại. Hãy chọn tên khác.')
                self.template_manager.create_project(template, dest)
            except Exception as exc:
                messagebox.showerror('Không tạo được dự án', str(exc), parent=dialog)
                return
            dialog.destroy()
            self.refresh_projects()
            self._launch_workspace(dest)

        ttk.Button(content, text='Tạo và soạn báo cáo', command=do_create, style='Primary.TButton').pack(
            anchor='e', pady=(8, 0)
        )
        dialog.bind('<Return>', lambda _event: do_create())
        dialog.bind('<Escape>', lambda _event: dialog.destroy())
        dialog.grab_set()
        name_entry.focus_set()

    def delete_selected_project(self):
        if not self.projects_list.curselection():
            return
        name = self.projects_list.get(self.projects_list.curselection()[0])
        if messagebox.askyesno(
            'Xóa dự án', f"Xóa dự án '{name}' và toàn bộ nội dung? Hành động này không thể hoàn tác.", parent=self.root
        ):
            try:
                target = workspace_path(self.workspaces_dir, name)
                if target.is_symlink() or target.resolve().parent != self.workspaces_dir.resolve():
                    raise ValueError('Đường dẫn dự án không hợp lệ.')
                shutil.rmtree(target)
                self.refresh_projects()
            except Exception as exc:
                messagebox.showerror('Không xóa được dự án', str(exc), parent=self.root)

    def open_project(self):
        path = filedialog.askdirectory(
            parent=self.root, initialdir=str(self.workspaces_dir), title='Chọn thư mục dự án'
        )
        if path:
            self._launch_workspace(Path(path))

    def open_selected_project(self):
        if self.projects_list.curselection():
            self._launch_workspace(self.workspaces_dir / self.projects_list.get(self.projects_list.curselection()[0]))

    def open_workspaces(self):
        if os.name == 'nt':
            os.startfile(self.workspaces_dir)
        else:
            messagebox.showinfo('Thư mục tài liệu', str(self.workspaces_dir), parent=self.root)

    def show_about(self):
        tools = renderer_status()
        status = '\n'.join(f'{name}: {path or "chưa tìm thấy"}' for name, path in tools.items())
        messagebox.showinfo(
            'Doc Automation Suite',
            f'Phiên bản {VERSION}\n\nSoạn báo cáo và xuất Word/PDF.\nDự án: {self.workspaces_dir}\nNhật ký: {data_root(self.base_dir) / "logs"}\n\n{status}',
            parent=self.root,
        )

    def open_legacy_workflow(self):
        from src.ui.legacy_workflow import launch_workflow_ui

        launch_workflow_ui(self.root)

    def _launch_workspace(self, project_path):
        try:
            window = VisualBuilderWindow(self.root, project_path)
            window.lift()
        except Exception as exc:
            messagebox.showerror('Không mở được dự án', str(exc), parent=self.root)
