## 2024-05-24 - Tkinter Cursor and Empty States UX

**Learning:** In Tkinter, setting the cursor via `ttk.Style().configure` does not work for
`ttk.Button`. Empty listboxes without placeholder text can be confusing. **Action:** Apply
`cursor='hand2'` globally using `root.option_add('*TButton*cursor', 'hand2')` and directly on
`tk.Listbox`. Use placeholder text with distinct styling (e.g. gray foreground) and early returns in
event handlers to implement explicit empty states for listboxes.
