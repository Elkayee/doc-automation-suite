## 2024-05-17 - [Tkinter Listbox Empty States & Cursors]

**Learning:** Native Tkinter Listbox lacks built-in empty states, causing confusion when lists are
empty. **Action:** Implement empty states by inserting a visually distinct placeholder string (e.g.,
foreground='gray') when `listbox.size() == 0`, and update all selection event handlers to explicitly
ignore items with that color. For Tkinter widgets like `tk.Listbox`, explicitly pass
`cursor='hand2'` via kwargs.
