## 2024-05-24 - Interactive Cursors and Empty States in Tkinter

**Learning:** By default, Tkinter buttons and listboxes do not change cursors on hover, and
listboxes lack a native empty state feature. This creates poor visual feedback for users.
**Action:** Always assign `cursor='hand2'` to interactive elements (globally for ttk.Button via
`option_add`, locally for `tk.Listbox`). For listboxes, insert a placeholder string when size is 0,
visually differentiate it (e.g., `foreground='gray'`), and explicitly ignore it in event handlers by
checking `itemcget(idx, 'foreground') == 'gray'`.
