import sys
from pathlib import Path
import tkinter as tk

def main():
    # Install dependencies if needed (check pyyaml)
    try:
        import yaml
    except ImportError:
        print("Missing pyyaml. Please run: pip install -r requirements.txt")
        sys.exit(1)
        
    # Start Dashboard
    from src.ui.dashboard import DashboardApp
    
    root = tk.Tk()
    app = DashboardApp(root, Path(__file__).resolve().parent)
    root.mainloop()

if __name__ == "__main__":
    main()
