## 2024-05-24 - Tkinter Listbox Empty States

**Learning:** Empty `tk.Listbox` widgets offer no visual feedback and can appear broken to users.
Implementing a visible empty state improves clarity and UX.

**Action:** Insert a placeholder string (e.g., "(Chua co du an nao)") into the listbox and set its
color to gray (`listbox.itemconfig(0, foreground='gray')`). Update event handlers to ignore
selections where `itemcget(idx, 'foreground') == 'gray'` to prevent errors.
