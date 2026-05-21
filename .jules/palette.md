## 2024-05-21 - Tkinter Listbox Empty States and Cursors

**Learning:** Tkinter Listboxes do not have a built-in "empty state" display, and default buttons
lack a pointer cursor on hover, which reduces affordance. **Action:** Implement empty states by
inserting a placeholder item and styling it with `foreground='gray'`, then updating event handlers
to ignore items with this style. Add `cursor='hand2'` to Listboxes and use
`root.option_add('*TButton*cursor', 'hand2')` to globally apply pointer cursors to ttk.Buttons to
improve discoverability.
