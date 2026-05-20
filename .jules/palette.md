## 2024-05-20 - Tkinter Listbox Empty States and Global Cursors

**Learning:** In Tkinter `tk.Listbox`, implementing empty states requires manually inserting a
placeholder string and distinguishing it visually (e.g., using `foreground='gray'`). Furthermore,
global application of hover cursors to specific widget types requires using
`root.option_add('*TButton*cursor', 'hand2')`, as styling via `ttk.Style()` is insufficient for
components like `ttk.Button`. **Action:** When working with `tk.Listbox` empty states, insert
placeholder text and set its style, then add checks in event handlers to ignore interactions with
the placeholder (`itemcget(idx, 'foreground') == 'gray'`). Apply hover cursors globally for widget
types using the option database.
