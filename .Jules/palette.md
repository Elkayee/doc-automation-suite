## 2026-05-26 - Tkinter Button Cursors

**Learning:** Setting the cursor via `ttk.Style().configure('TButton', cursor='hand2')` does not
work for `ttk.Button`. Instead, it must be applied globally using the Tk option database:
`root.option_add('*TButton*cursor', 'hand2')`. For `tk.Listbox`, pass `cursor='hand2'` explicitly
via widget kwargs. **Action:** Use `option_add` for ttk.Button global cursors and kwargs for other
tk widgets.
