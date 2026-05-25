## 2024-05-25 - Tkinter Empty States & Visual Feedback

**Learning:** Tkinter listboxes lack native empty state placeholders. Standard web UX features like
a pointer cursor on hover are also missing from `ttk.Button` by default. Setting the cursor on
`ttk.Button` via `ttk.Style` is ineffective; it requires
`root.option_add('*TButton*cursor', 'hand2')`. **Action:** Implement empty states in `tk.Listbox` by
inserting a placeholder item with `foreground='gray'`, and add guards in event handlers (like
`curselection()`) to ignore this placeholder. Use the global option database to ensure buttons
display the correct hover cursor.
