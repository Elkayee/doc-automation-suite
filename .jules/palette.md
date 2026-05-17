## 2024-05-17 - Implement Listbox Empty States in Tkinter

**Learning:** Tkinter `tk.Listbox` lacks native empty states and `ttk.Button` requires explicit global configuration for cursor changes.
**Action:** Implemented the empty state by conditionally inserting a placeholder string (`'Chua co du an nao...'`) and styling it using `listbox.itemconfig(0, foreground='gray')`. Guarded all related callbacks (`open_selected_project`, `delete_selected_project`) to explicitly ignore clicks when `listbox.itemcget(idx, 'foreground') == 'gray'`. Assigned `cursor='hand2'` directly to the `tk.Listbox` constructor, and for `ttk.Button`, configured it globally with `root.option_add('*TButton*cursor', 'hand2')` to improve visual feedback on hover.
