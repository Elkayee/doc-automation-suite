import os
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from src.core.template_manager import TemplateManager
from src.core.assembler import DocumentAssembler
from src.core.docx_builder import DocxBuilder

class DashboardApp:
    def __init__(self, root, base_dir: Path):
        self.root = root
        self.base_dir = base_dir
        self.template_manager = TemplateManager(base_dir / 'templates')
        self.workspaces_dir = base_dir / 'workspaces'
        self.workspaces_dir.mkdir(exist_ok=True)

        self.root.title("Doc Automation Suite - Dashboard")
        self.root.geometry("800x600")
        self.root.configure(bg="#f3efe5")

        self._setup_styles()
        self._build_ui()

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background='#f3efe5')
        style.configure('Header.TLabel', background='#f3efe5', foreground='#1f3f5b', font=('Georgia', 24, 'bold'))
        style.configure('SubHeader.TLabel', background='#f3efe5', foreground='#2b241b', font=('Georgia', 14))
        style.configure('Action.TButton', font=('Georgia', 12, 'bold'), padding=10)

    def _build_ui(self):
        main_container = ttk.Frame(self.root, padding=30)
        main_container.pack(fill='both', expand=True)

        # Header
        ttk.Label(main_container, text="Doc Automation Suite", style='Header.TLabel').pack(anchor='center', pady=(0, 5))
        ttk.Label(main_container, text="Chọn tác vụ để bắt đầu", style='SubHeader.TLabel').pack(anchor='center', pady=(0, 40))

        # Actions Grid
        actions_frame = ttk.Frame(main_container)
        actions_frame.pack(anchor='center')

        ttk.Button(actions_frame, text="+ Tạo Dự Án Mới", style='Action.TButton', command=self.show_create_dialog).grid(row=0, column=0, padx=10, pady=10)
        ttk.Button(actions_frame, text="Mở Dự Án", style='Action.TButton', command=self.open_project).grid(row=0, column=1, padx=10, pady=10)

        # Recent Projects
        ttk.Label(main_container, text="Dự án gần đây", font=('Georgia', 12, 'bold'), background='#f3efe5').pack(anchor='w', pady=(40, 10))

        self.projects_list = tk.Listbox(main_container, font=('Consolas', 11), height=10)
        self.projects_list.pack(fill='both', expand=True)
        self.projects_list.bind('<Double-1>', lambda e: self.open_selected_project())

        self.refresh_projects()

    def refresh_projects(self):
        self.projects_list.delete(0, tk.END)
        for entry in self.workspaces_dir.iterdir():
            if entry.is_dir() and (entry / 'config.yaml').exists():
                self.projects_list.insert(tk.END, entry.name)

    def show_create_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Tạo Dự Án Mới")
        dialog.geometry("500x300")
        dialog.configure(bg="#f3efe5")

        ttk.Label(dialog, text="Tên dự án:").pack(pady=(20, 5))
        name_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=name_var, width=40).pack()

        ttk.Label(dialog, text="Chọn Template:").pack(pady=(20, 5))
        templates = self.template_manager.list_templates()
        template_var = tk.StringVar()

        if templates:
            template_var.set(list(templates.keys())[0])
            combo = ttk.Combobox(dialog, textvariable=template_var, values=list(templates.keys()), state="readonly", width=38)
            combo.pack()
        else:
            ttk.Label(dialog, text="Không tìm thấy template nào!").pack()

        def do_create():
            name = name_var.get().strip()
            tmpl = template_var.get()
            if not name:
                messagebox.showerror("Lỗi", "Vui lòng nhập tên dự án")
                return
            if not tmpl:
                messagebox.showerror("Lỗi", "Vui lòng chọn template")
                return

            dest = self.workspaces_dir / name
            if dest.exists():
                messagebox.showerror("Lỗi", "Tên dự án đã tồn tại")
                return

            try:
                self.template_manager.create_project(tmpl, dest)
                messagebox.showinfo("Thành công", f"Đã tạo dự án {name}!")
                dialog.destroy()
                self.refresh_projects()
                self._launch_workspace(dest)
            except Exception as e:
                messagebox.showerror("Lỗi", str(e))

        ttk.Button(dialog, text="Tạo Mới", command=do_create).pack(pady=30)

    def open_project(self):
        path = filedialog.askdirectory(initialdir=str(self.workspaces_dir))
        if path:
            self._launch_workspace(Path(path))

    def open_selected_project(self):
        if not self.projects_list.curselection():
            return
        idx = self.projects_list.curselection()[0]
        name = self.projects_list.get(idx)
        self._launch_workspace(self.workspaces_dir / name)

    def _launch_workspace(self, path: Path):
        # Open directory in OS explorer
        try:
            if os.name == 'nt': # Windows
                os.startfile(path)
            elif os.name == 'posix': # macOS/Linux
                import subprocess
                import sys
                opener = 'open' if sys.platform == 'darwin' else 'xdg-open'
                subprocess.call([opener, str(path)])
        except Exception as e:
            print(f"Lỗi mở thư mục: {e}")

        # Show a minimal workspace editor window
        editor = tk.Toplevel(self.root)
        editor.title(f"Workspace: {path.name}")
        editor.geometry("400x200")
        editor.configure(bg="#f3efe5")
        
        ttk.Label(editor, text=f"Đang làm việc tại:\n{path.name}", 
                 style='SubHeader.TLabel', justify='center').pack(pady=20)
                 
        def do_build():
            try:
                assembler = DocumentAssembler(path)
                md_content, _ = assembler.assemble_markdown()
                
                builder = DocxBuilder(path)
                img_cache_dir = path / '.img_cache'
                builder.build_from_markdown(md_content, img_cache_dir)
                
                output_docx = path / 'output' / 'final_document.docx'
                builder.save(output_docx)
                
                messagebox.showinfo("Thành công", f"Đã build file docx tại:\n{output_docx}")
            except Exception as e:
                messagebox.showerror("Lỗi Build", f"Có lỗi xảy ra:\n{str(e)}")
                
        ttk.Button(editor, text="Build DOCX", style='Action.TButton', command=do_build).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = DashboardApp(root, Path(__file__).resolve().parent.parent.parent)
    root.mainloop()
