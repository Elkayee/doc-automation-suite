## 2025-01-20 - Tkinter Empty States and Interactive Cursors

**Learning:** In Tkinter UI applications, implementing visual feedback like empty states for
Listboxes and hover cursors for interactive elements significantly improves user experience.
However, `ttk.Style` doesn't support setting cursors for `ttk.Button` directly. **Action:**
Implement `tk.Listbox` empty states by inserting a placeholder string when the list is empty and
setting its color to be visually distinct (e.g., `listbox.itemconfig(0, foreground='gray')`). Update
all associated event handlers to check `listbox.itemcget(idx, 'foreground') == 'gray'` and return
early to prevent the application from treating the placeholder as valid user data. Apply global
cursor styles for `ttk.Button` using the Tk option database:
`root.option_add('*TButton*cursor', 'hand2')`.
