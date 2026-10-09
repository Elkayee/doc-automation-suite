import ctypes
import logging
import tkinter as tk
from tkinter import messagebox

from src.core.runtime import data_root, resource_root


def main():
    if hasattr(ctypes, 'windll'):
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    logs = data_root() / 'logs'
    logs.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(filename=logs / 'application.log', encoding='utf-8', level=logging.INFO)
    root = tk.Tk()
    root.withdraw()

    def report_error(exc_type, exc_value, traceback):
        logging.error('Application error', exc_info=(exc_type, exc_value, traceback))
        messagebox.showerror('Không thực hiện được', f'{exc_value}\n\nNhật ký: {logs / "application.log"}', parent=root)

    root.report_callback_exception = report_error
    try:
        from src.ui.dashboard import DashboardApp

        DashboardApp(root, resource_root())
    except Exception as exc:
        logging.exception('Startup failed')
        messagebox.showerror('Không mở được ứng dụng', f'{exc}\n\nNhật ký: {logs / "application.log"}', parent=root)
        root.destroy()
        return
    root.deiconify()
    root.mainloop()


if __name__ == '__main__':
    main()
