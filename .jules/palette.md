## 2024-05-24 - Tkinter Listbox empty state and interactivity

**Learning:** Tkinter `tk.Listbox` does not have a built-in empty state, which can confuse users.
Additionally, ttk Buttons do not show a pointer cursor on hover by default. **Action:** Implement an
empty state by inserting a placeholder string colored gray, and ensure event handlers check
`listbox.itemcget(idx, 'foreground') == 'gray'` to ignore interactions. Apply `cursor='hand2'`
globally via `root.option_add('*TButton*cursor', 'hand2')` for buttons, and pass `cursor='hand2'`
explicitly to Listbox widgets for better visual feedback.
