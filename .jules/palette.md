## 2024-05-24 - Listbox Empty States in Tkinter

**Learning:** In Tkinter, since `tk.Listbox` does not natively support an "empty state" overlay like
modern web frameworks, adding a placeholder item (e.g., "(No projects yet)") is a common fallback.
However, doing so makes the placeholder selectable and triggerable. **Action:** When implementing an
empty state via a placeholder string in `tk.Listbox`, visually distinguish it (e.g., using
`listbox.itemconfig(0, foreground='gray')`) and update **ALL** relevant event handlers (e.g.,
double-click, delete, edit) to explicitly check `listbox.itemcget(idx, 'foreground') == 'gray'` and
return early to prevent invalid actions on the placeholder text.
