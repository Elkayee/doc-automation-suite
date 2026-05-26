## 2024-05-26 - Implement Tkinter Listbox empty states

**Learning:** `tk.Listbox` does not natively support an empty state placeholder. Users might get
confused when no data is present because it just looks like a blank, broken widget. **Action:**
Implement `tk.Listbox` empty states by inserting a placeholder string and setting its color to be
visually distinct (e.g., `listbox.itemconfig(0, foreground='gray')`). Update all associated event
handlers to check `listbox.itemcget(idx, 'foreground') == 'gray'`, clear the selection (e.g.,
`listbox.selection_clear(idx)`), and return early to prevent treating the placeholder as valid data.
