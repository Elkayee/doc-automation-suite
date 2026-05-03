# Delete Project Feature Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Allow users to permanently delete projects from the Dashboard's Recent Projects list.

**Architecture:** We will modify the Tkinter UI in `src/ui/dashboard.py` to add a delete button next to the "Recent Projects" heading. The button will trigger a confirmation dialog, and if confirmed, use `shutil.rmtree` to delete the project folder from the disk.

**Tech Stack:** Python, Tkinter (ttk, messagebox), `shutil`, `pathlib`.

---

### Task 1: Add the Delete Project UI and Logic

**Files:**
- Modify: `src/ui/dashboard.py`

- [ ] **Step 1: Add the necessary imports**

At the top of `src/ui/dashboard.py`, ensure `shutil` is imported.

```python
import shutil
```

- [ ] **Step 2: Update the UI to include the Delete button**

In `src/ui/dashboard.py`, inside the `_build_ui` method, replace the single "Du an gan day" label (around line 61) with a frame containing the label and the new button.

Replace:
```python
        ttk.Label(main_container, text='Du an gan day', font=('Georgia', 12, 'bold'), background='#f3efe5').pack(
            anchor='w', pady=(40, 10)
        )
```

With:
```python
        recent_header_frame = ttk.Frame(main_container)
        recent_header_frame.pack(fill='x', pady=(40, 10))
        
        ttk.Label(recent_header_frame, text='Du an gan day', font=('Georgia', 12, 'bold'), background='#f3efe5').pack(side='left')
        
        ttk.Button(recent_header_frame, text='Xoa Du An', style='Action.TButton', command=self.delete_selected_project).pack(side='right')
```

- [ ] **Step 3: Implement the `delete_selected_project` logic**

Add the `delete_selected_project` method to the `DashboardApp` class in `src/ui/dashboard.py` (e.g., right after `show_create_dialog`).

```python
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
```

- [ ] **Step 4: Run the application manually to test**

Since this is a UI-heavy change involving file system operations, a manual smoke test is the most reliable verification. 
Run: `python make.py run` (or `python src/ui/dashboard.py`).
Expected: 
1. The "Xoa Du An" button appears on the right side, across from "Du an gan day".
2. Clicking it without a selection shows a warning.
3. Selecting a project and clicking it shows the confirmation dialog.
4. Clicking 'Yes' deletes the folder and removes it from the list.

- [ ] **Step 5: Commit**

```bash
git add src/ui/dashboard.py
git commit -m "feat(ui): add delete project button and logic to dashboard"
```