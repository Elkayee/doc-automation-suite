## 2025-05-24 - Add Empty States & Cursors to Tkinter Listbox

**Learning:** Tkinter `tk.Listbox` elements can visually indicate empty states by inserting a
placeholder string with `foreground='gray'`. Button cursors can be globally improved using
`root.option_add('*TButton*cursor', 'hand2')`. **Action:** When a `tk.Listbox` is empty, insert a
placeholder and add checks (`itemcget(idx, 'foreground') == 'gray'`) in event handlers to prevent
actions on the placeholder.
