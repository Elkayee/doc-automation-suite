# Visual Doc Builder Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create a three-pane IDE-like workspace with direct Markdown editing and real-time Word-style A4 pagination.

**Architecture:** A Tkinter Toplevel window containing three panes: Navigator (file list), Editor (text), and Visualizer (embedded browser). Uses `tkinterweb` for high-fidelity rendering and CSS Paged Media for pagination.

**Tech Stack:** Python (Tkinter), `tkinterweb` (for Chromium/Edge/Webkit embedding), CSS (Paged Media).

---

### Task 1: Environment Setup & Dependency Check

**Files:**
- Modify: `requirements.txt`

- [ ] **Step 1: Add tkinterweb to requirements**
Add `tkinterweb` to `requirements.txt`.

- [ ] **Step 2: Install dependencies**
Run: `pip install tkinterweb`

- [ ] **Step 3: Verify installation**
Run: `python -c "from tkinterweb import HtmlFrame; print('OK')"`
Expected: `OK`

- [ ] **Step 4: Commit**
```bash
git add requirements.txt
git commit -m "chore: add tkinterweb dependency"
```

### Task 2: Basic Three-Pane Layout

**Files:**
- Create: `src/ui/visual_builder/window.py`

- [ ] **Step 1: Write skeleton for VisualBuilderWindow**
Implement a Tkinter window using `ttk.PanedWindow`.

```python
import tkinter as tk
from tkinter import ttk

class VisualBuilderWindow(tk.Toplevel):
    def __init__(self, master, project_path):
        super().__init__(master)
        self.title(f"Visual Builder - {project_path.name}")
        self.geometry("1200x800")
        
        self.paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.paned.pack(fill='both', expand=True)
        
        self.nav_frame = ttk.Frame(self.paned, width=200)
        self.edit_frame = ttk.Frame(self.paned, width=400)
        self.view_frame = ttk.Frame(self.paned, width=600)
        
        self.paned.add(self.nav_frame, weight=1)
        self.paned.add(self.edit_frame, weight=2)
        self.paned.add(self.view_frame, weight=3)

if __name__ == "__main__":
    root = tk.Tk()
    VisualBuilderWindow(root, type('Obj', (object,), {'name': 'Test'})).mainloop()
```

- [ ] **Step 2: Run and verify layout**
Run the script to see three empty panes.

- [ ] **Step 3: Commit**
```bash
git add src/ui/visual_builder/window.py
git commit -m "feat: initial three-pane layout for visual builder"
```

### Task 3: Navigator (Sidebar) Implementation

**Files:**
- Create: `src/ui/visual_builder/navigator.py`

- [ ] **Step 1: Implement file list with refresh logic**
Use a `tk.Listbox` to show files in the `chapters/` directory.

- [ ] **Step 2: Add chapter selection callback**
Expose a callback that notifies the main window when a file is selected.

- [ ] **Step 3: Commit**
```bash
git add src/ui/visual_builder/navigator.py
git commit -m "feat: add navigator component for visual builder"
```

### Task 4: Editor with Syntax Highlighting

**Files:**
- Create: `src/ui/visual_builder/editor.py`

- [ ] **Step 1: Implement Text widget with basic Markdown highlighting**
Add tags for headers (`#`), bold (`**`), etc.

- [ ] **Step 2: Add auto-save logic**
Save to the `.md` file after a short delay (debounce) when typing stops.

- [ ] **Step 3: Commit**
```bash
git add src/ui/visual_builder/editor.py
git commit -m "feat: add markdown editor with auto-save"
```

### Task 5: Visualizer with CSS Pagination

**Files:**
- Create: `src/ui/visual_builder/visualizer.py`
- Create: `src/ui/visual_builder/styles.css`

- [ ] **Step 1: Define A4 CSS styles**
In `styles.css`, add `@page` and `.page` container rules for A4 sizing.

- [ ] **Step 2: Implement HtmlFrame wrapper**
Use `tkinterweb.HtmlFrame` to render HTML generated from Markdown.

- [ ] **Step 3: Integrate Assembler**
Use `src.core.assembler.DocumentAssembler` to get the full content for the preview.

- [ ] **Step 4: Commit**
```bash
git add src/ui/visual_builder/visualizer.py src/ui/visual_builder/styles.css
git commit -m "feat: add visualizer with CSS paged media"
```

### Task 6: Final Integration & Dashboard Link

**Files:**
- Modify: `src/ui/dashboard.py`
- Modify: `src/ui/visual_builder/window.py`

- [ ] **Step 1: Wire up components in window.py**
Connect Navigator selection -> Editor load -> Visualizer update.

- [ ] **Step 2: Add "Visual Builder" button to Dashboard**
Replace the old minimal workspace build window with a button that launches the `VisualBuilderWindow`.

- [ ] **Step 3: Final Test**
Create a new project, edit a chapter, and verify it updates in the paginated visualizer.

- [ ] **Step 4: Commit**
```bash
git add src/ui/dashboard.py src/ui/visual_builder/window.py
git commit -m "feat: integrate visual builder into main dashboard"
```
