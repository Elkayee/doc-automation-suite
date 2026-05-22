## 2024-05-22 - Tkinter Listbox Empty State

**Learning:** Implementing empty states in Tkinter Listbox requires inserting a placeholder item
with distinct formatting (e.g., foreground color) and modifying interaction handlers to ignore the
placeholder to prevent processing invalid data. **Action:** Insert placeholder with
`itemconfig(0, foreground='gray')` and update click/selection handlers to check
`itemcget(idx, 'foreground') == 'gray'`.
