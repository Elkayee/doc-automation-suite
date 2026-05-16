## 2024-03-24 - Tkinter Listbox Empty States

**Learning:** Tkinter `tk.Listbox` does not have a native empty state feature. Implementing a
placeholder text by inserting a fake item and styling it (e.g., `foreground='gray'`) requires
explicitly updating ALL relevant event handlers (`<<ListboxSelect>>`, `<Double-1>`, buttons
dependent on selection) to check for the placeholder item (`itemcget(idx, 'foreground') == 'gray'`)
and return early, preventing unintended actions on the placeholder text itself. **Action:** Always
verify dependent event handlers when faking empty states in Tkinter Listbox to ensure the
placeholder isn't treated as a legitimate selection.
