import sys
from pathlib import Path
import tkinter as tk

def main():
    # Install dependencies if needed
    try:
        import yaml
        import docx
    except ImportError as e:
        missing_module = str(e).split("'")[1] if "'" in str(e) else "a required module"
        print(f"Missing {missing_module}. Please run: pip install -r requirements.txt")
        sys.exit(1)
        
    # Start Dashboard
    from src.ui.dashboard import DashboardApp
    
    root = tk.Tk()
    app = DashboardApp(root, Path(__file__).resolve().parent)
    root.mainloop()

if __name__ == "__main__":
    main()
