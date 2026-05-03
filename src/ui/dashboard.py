import sys
from pathlib import Path
import shutil

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from src.core.template_manager import TemplateManager
from src.ui.visual_builder import VisualBuilderWindow


class DashboardApp:
    def __init__(self, root, base_dir: Path):
        self.root = root
        self.base_dir = base_dir
        self.template_manager = TemplateManager(base_dir / 'templates')
        self.workspaces_dir = base_dir / 'workspaces'
        self.workspaces_dir.mkdir(exist_ok=True)

        self.root.title('Doc Automation Suite - Dashboard')
        self.root.geometry('800x600')
        self.root.configure(bg='#f3efe5')

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

        ttk.Label(main_container, text='Doc Automation Suite', style='Header.TLabel').pack(anchor='center', pady=(0, 5))
        ttk.Label(main_container, text='Chon tac vu de bat dau', style='SubHeader.TLabel').pack(
            anchor='center', pady=(0, 40)
        )

        actions_frame = ttk.Frame(main_container)
        actions_frame.pack(anchor='center')

        ttk.Button(actions_frame, text='+ Tao Du An Moi', style='Action.TButton', command=self.show_create_dialog).grid(
            row=0, column=0, padx=10, pady=10
        )
        ttk.Button(actions_frame, text='Mo Du An', style='Action.TButton', command=self.open_project).grid(
            row=0, column=1, padx=10, pady=10
        )
        ttk.Button(
            actions_frame,
            text='Cong Cu Cu (Legacy)',
            style='Action.TButton',
            command=self.open_legacy_workflow,
        ).grid(row=0, column=2, padx=10, pady=10)

        recent_header_frame = ttk.Frame(main_container)
        recent_header_frame.pack(fill='x', pady=(40, 10))

        ttk.Label(recent_header_frame, text='Du an gan day', font=('Georgia', 12, 'bold'), background='#f3efe5').pack(
            side='left'
        )

        ttk.Button(
            recent_header_frame, text='Xoa Du An', style='Action.TButton', command=self.delete_selected_project
        ).pack(side='right')

        self.projects_list = tk.Listbox(main_container, font=('Consolas', 11), height=10)
        self.projects_list.pack(fill='both', expand=True)
        self.projects_list.bind('<Double-1>', lambda _event: self.open_selected_project())

        self.refresh_projects()

    def refresh_projects(self):
        self.projects_list.delete(0, tk.END)
        for entry in self.workspaces_dir.iterdir():
            if entry.is_dir() and (entry / 'config.yaml').exists():
                self.projects_list.insert(tk.END, entry.name)

    def show_create_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title('Tao Du An Moi')
        dialog.geometry('500x300')
        dialog.configure(bg='#f3efe5')

        ttk.Label(dialog, text='Ten du an:').pack(pady=(20, 5))
        name_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=name_var, width=40).pack()

        ttk.Label(dialog, text='Chon Template:').pack(pady=(20, 5))
        templates = self.template_manager.list_templates()
        template_var = tk.StringVar()

        if templates:
            template_var.set(list(templates.keys())[0])
            ttk.Combobox(
                dialog,
                textvariable=template_var,
                values=list(templates.keys()),
                state='readonly',
                width=38,
            ).pack()
        else:
            ttk.Label(dialog, text='Khong tim thay template nao.').pack()

        def do_create():
            name = name_var.get().strip()
            tmpl = template_var.get()
            if not name:
                messagebox.showerror('Loi', 'Vui long nhap ten du an', parent=dialog)
                return
            if not tmpl:
                messagebox.showerror('Loi', 'Vui long chon template', parent=dialog)
                return

            dest = self.workspaces_dir / name
            if dest.exists():
                messagebox.showerror('Loi', 'Ten du an da ton tai', parent=dialog)
                return

            try:
                self.template_manager.create_project(tmpl, dest)
                messagebox.showinfo('Thanh cong', f'Da tao du an {name}', parent=dialog)
            except Exception as exc:
                messagebox.showerror('Loi', str(exc), parent=dialog)
                return

            dialog.destroy()
            self.refresh_projects()
            self._launch_workspace(dest)

        ttk.Button(dialog, text='Tao Moi', command=do_create).pack(pady=30)

    def delete_selected_project(self):
        if not self.projects_list.curselection():
            messagebox.showwarning('Canh bao', 'Vui long chon mot du an de xoa', parent=self.root)
            return

        idx = self.projects_list.curselection()[0]
        name = self.projects_list.get(idx)

        confirm = messagebox.askyesno(
            'Xac nhan xoa',
            f"Ban co chac chan muon xoa du an '{name}' khong?\nHanh dong nay khong the hoan tac.",
            parent=self.root
        )

        if confirm:
            target_dir = self.workspaces_dir / name
            try:
                shutil.rmtree(target_dir)
                messagebox.showinfo('Thanh cong', f"Da xoa du an '{name}'", parent=self.root)
                self.refresh_projects()
            except Exception as e:
                messagebox.showerror('Loi', f"Khong the xoa du an:\n{str(e)}", parent=self.root)

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

    def open_legacy_workflow(self):
        from src.ui.legacy_workflow import launch_workflow_ui

        launch_workflow_ui()

    def _launch_workspace(self, path: Path):
        VisualBuilderWindow(self.root, path)


if __name__ == '__main__':
    root = tk.Tk()
    app = DashboardApp(root, Path(__file__).resolve().parent.parent.parent)
    root.mainloop()
