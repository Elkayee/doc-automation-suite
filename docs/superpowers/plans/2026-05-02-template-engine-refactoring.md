# Doc Automation Suite - Template Engine Refactoring Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Refactor the monolithic `make.py` script into a modular Document Automation Suite with a flexible Template Engine to support various document types (reports, exams, etc.).

**Architecture:** 
1. Core engine logic will be split into smaller modules (`markdown_parser.py`, `docx_builder.py`, `ui.py`).
2. A new `templates/` structure will define different project types via `config.yaml`, base `.docx` templates, and boilerplate `.md` files.
3. A `ProjectManager` class will handle workspace creation from templates.
4. The UI will be updated to be a Dashboard allowing users to create new projects from templates and open existing ones.

**Tech Stack:** Python 3.10+, `python-docx`, `tkinter` (for UI), `pyyaml` (for config).

---

### Task 1: Setup New Directory Structure and Dependencies

**Files:**
- Modify: `requirements.txt`
- Create: `src/core/__init__.py`
- Create: `src/core/config.py`

- [ ] **Step 1: Add pyyaml to dependencies**

Modify `requirements.txt` to add pyyaml:
```text
pyyaml>=6.0
```

- [ ] **Step 2: Create core directory and config module**

Create `src/core/__init__.py` (empty file).

Create `src/core/config.py`:
```python
import yaml
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class TemplateConfig:
    name: str
    description: str
    type: str  # e.g., "report", "exam"
    required_files: List[str]
    docx_template: str
    settings: Dict[str, Any] = field(default_factory=dict)
    
    @classmethod
    def load(cls, config_path: Path) -> 'TemplateConfig':
        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")
            
        with open(config_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            
        return cls(
            name=data.get('name', 'Unknown Template'),
            description=data.get('description', ''),
            type=data.get('type', 'report'),
            required_files=data.get('required_files', []),
            docx_template=data.get('docx_template', 'template.docx'),
            settings=data.get('settings', {})
        )
```

- [ ] **Step 3: Commit**

```bash
git add requirements.txt src/core/
git commit -m "chore: setup core package and template config model"
```

### Task 2: Create Template Manager

**Files:**
- Create: `src/core/template_manager.py`

- [ ] **Step 1: Write TemplateManager implementation**

Create `src/core/template_manager.py`:
```python
import os
import shutil
from pathlib import Path
from typing import List, Dict
from src.core.config import TemplateConfig

class TemplateManager:
    def __init__(self, templates_dir: Path):
        self.templates_dir = templates_dir
        self.templates_dir.mkdir(parents=True, exist_ok=True)
        
    def list_templates(self) -> Dict[str, TemplateConfig]:
        """Returns a dict mapping template ID (folder name) to its config."""
        templates = {}
        for entry in self.templates_dir.iterdir():
            if entry.is_dir():
                config_path = entry / 'config.yaml'
                if config_path.exists():
                    try:
                        templates[entry.name] = TemplateConfig.load(config_path)
                    except Exception as e:
                        print(f"Error loading template {entry.name}: {e}")
        return templates

    def create_project(self, template_id: str, dest_dir: Path) -> bool:
        """Creates a new project in dest_dir based on the template_id."""
        template_path = self.templates_dir / template_id
        if not template_path.exists() or not (template_path / 'config.yaml').exists():
            raise ValueError(f"Invalid template ID: {template_id}")
            
        # Create destination directory
        dest_dir.mkdir(parents=True, exist_ok=True)
        
        # 1. Create config copy
        config = TemplateConfig.load(template_path / 'config.yaml')
        shutil.copy(template_path / 'config.yaml', dest_dir / 'config.yaml')
        
        # 2. Copy docx template if it exists
        docx_src = template_path / config.docx_template
        if docx_src.exists():
            shutil.copy(docx_src, dest_dir / config.docx_template)
            
        # 3. Create chapters directory and copy boilerplate
        chapters_dir = dest_dir / 'chapters'
        chapters_dir.mkdir(exist_ok=True)
        
        boilerplate_dir = template_path / 'boilerplate'
        
        for filename in config.required_files:
            dest_file = chapters_dir / filename
            src_file = boilerplate_dir / filename if boilerplate_dir.exists() else None
            
            if src_file and src_file.exists():
                shutil.copy(src_file, dest_file)
            else:
                # Create empty file if no boilerplate exists
                title = filename.replace('.md', '').replace('_', ' ')
                dest_file.write_text(f"# {title}\n\n[Nhập nội dung vào đây]\n", encoding='utf-8')
                
        return True
```

- [ ] **Step 2: Commit**

```bash
git add src/core/template_manager.py
git commit -m "feat: add template manager for project scaffolding"
```

### Task 3: Create Sample Templates

**Files:**
- Create: `templates/tieu_luan_nd30/config.yaml`
- Create: `templates/tieu_luan_nd30/boilerplate/F00_header.md`
- Create: `templates/bai_kiem_tra/config.yaml`

- [ ] **Step 1: Create base template for reports**

```bash
mkdir -p templates/tieu_luan_nd30/boilerplate
```

Create `templates/tieu_luan_nd30/config.yaml`:
```yaml
name: "Tiểu Luận (Chuẩn Nghị định 30)"
description: "Mẫu báo cáo tiểu luận chuẩn font Times New Roman, dãn dòng 1.5, thụt lề 1.27cm."
type: "report"
docx_template: "template.docx"
required_files:
  - "F00_header.md"
  - "F01_toc.md"
  - "Ch01_LOI_MO_DAU.md"
  - "Ch02_NOI_DUNG.md"
  - "Ch03_KET_LUAN.md"
  - "Ch04_TAI_LIEU_THAM_KHAO.md"
settings:
  font_name: "Times New Roman"
  font_size: 13
  line_spacing: 1.5
  first_line_indent: 1.27
```

Create `templates/tieu_luan_nd30/boilerplate/F00_header.md`:
```markdown
---
title: "Báo cáo Tiểu luận Môn học"
author: "Nguyễn Văn A"
class: "CTK43"
date: "2026-05-02"
---

# Lời Cảm Ơn

Chúng em xin chân thành cảm ơn...
```

- [ ] **Step 2: Create base template for exams**

```bash
mkdir -p templates/bai_kiem_tra/boilerplate
```

Create `templates/bai_kiem_tra/config.yaml`:
```yaml
name: "Đề Thi Trắc Nghiệm"
description: "Mẫu đề kiểm tra trắc nghiệm, hỗ trợ sinh tự động đề và đáp án, trộn đề."
type: "exam"
docx_template: "template.docx"
required_files:
  - "00_Thong_Tin.md"
  - "01_Cau_Hoi.md"
settings:
  font_name: "Times New Roman"
  font_size: 11
  columns: 2
```

- [ ] **Step 3: Commit**

```bash
git add templates/
git commit -m "feat: add initial template definitions for reports and exams"
```

### Task 4: Refactor Markdown Assembling Logic

**Files:**
- Create: `src/core/assembler.py`

- [ ] **Step 1: Extract assemble_markdown from make.py**

Create `src/core/assembler.py`:
```python
import os
from pathlib import Path
from typing import Tuple, List

class DocumentAssembler:
    def __init__(self, workspace_dir: Path):
        self.workspace_dir = workspace_dir
        
    def get_config(self):
        from src.core.config import TemplateConfig
        config_path = self.workspace_dir / 'config.yaml'
        if config_path.exists():
            return TemplateConfig.load(config_path)
        return None
        
    def assemble_markdown(self) -> Tuple[str, List[str]]:
        """Reads required files from workspace/chapters and joins them."""
        config = self.get_config()
        if not config:
            raise FileNotFoundError("Workspace is missing config.yaml")
            
        chapters_dir = self.workspace_dir / 'chapters'
        if not chapters_dir.exists():
            raise FileNotFoundError(f"Chapters directory missing in {self.workspace_dir}")
            
        parts = []
        processed_files = []
        
        for filename in config.required_files:
            file_path = chapters_dir / filename
            if file_path.exists():
                with open(file_path, encoding='utf-8') as f:
                    parts.append(f.read().strip())
                processed_files.append(str(file_path))
            else:
                print(f"  [WARN] Missing required file: {filename}")
                
        final_md = '\n\n'.join(parts)
        return final_md, processed_files
        
    def save_assembled(self, output_path: Path) -> Tuple[str, List[str]]:
        final_md, processed_files = self.assemble_markdown()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(final_md)
        return final_md, processed_files
```

- [ ] **Step 2: Commit**

```bash
git add src/core/assembler.py
git commit -m "refactor: extract markdown assembly logic to separate module"
```

### Task 5: Refactor DOCX Building Logic

**Files:**
- Create: `src/core/docx_builder.py`

- [ ] **Step 1: Extract DOCX creation logic from make.py**

Create `src/core/docx_builder.py`:
*(Note: To keep tasks bite-sized, we will create a simplified wrapper class that will eventually encapsulate the large parsing logic from make.py. Full parsing logic migration is large and should be handled incrementally. We'll start with the structural wrapper.)*

```python
from pathlib import Path
from docx import Document
import os

class DocxBuilder:
    def __init__(self, workspace_dir: Path):
        self.workspace_dir = workspace_dir
        self.config = self._get_config()
        self.doc = self._init_document()
        
    def _get_config(self):
        from src.core.config import TemplateConfig
        config_path = self.workspace_dir / 'config.yaml'
        if config_path.exists():
            return TemplateConfig.load(config_path)
        return None
        
    def _init_document(self):
        """Loads template.docx if it exists, otherwise creates a blank Document."""
        if self.config and self.config.docx_template:
            template_path = self.workspace_dir / self.config.docx_template
            if template_path.exists():
                return Document(str(template_path))
        return Document()
        
    def build_from_markdown(self, md_content: str, img_cache_dir: Path):
        """
        Applies markdown parsing and writes to self.doc.
        (This will integrate the parse_and_write logic from make.py)
        """
        # For now, we stub this out to be integrated in the next pass.
        # It should read md_content line by line and add to self.doc
        p = self.doc.add_paragraph("DOCX generation triggered. (Parser logic will be migrated here)")
        
    def save(self, output_path: Path):
        output_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            self.doc.save(str(output_path))
        except PermissionError as exc:
            raise RuntimeError(
                f"Khong the ghi file {output_path.name}. Hay dong file Word cu truoc khi build lai."
            ) from exc
```

- [ ] **Step 2: Commit**

```bash
git add src/core/docx_builder.py
git commit -m "refactor: extract DOCX builder structural wrapper"
```

### Task 6: Build the New Dashboard UI (Part 1)

**Files:**
- Create: `src/ui/dashboard.py`

- [ ] **Step 1: Create Dashboard UI basic layout**

Create `src/ui/dashboard.py`:
```python
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from src.core.template_manager import TemplateManager

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
                # TODO: Launch Workspace Editor here
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
        # Stub for launching the actual editor
        messagebox.showinfo("Workspace", f"Sẽ mở workspace: {path.name}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DashboardApp(root, Path(__file__).resolve().parent.parent.parent)
    root.mainloop()
```

- [ ] **Step 2: Commit**

```bash
git add src/ui/dashboard.py
git commit -m "feat: create new dashboard UI for project management"
```

### Task 7: Integrate and Run

**Files:**
- Modify: `make.py` (or create a new entrypoint `main.py`)

- [ ] **Step 1: Create new entrypoint**

Create `main.py` in the root directory:
```python
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
```

- [ ] **Step 2: Commit**

```bash
git add main.py
git commit -m "feat: add main entrypoint for the new Dashboard UI"
```
