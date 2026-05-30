## 2024-05-30 - Empty States in Tkinter Listbox

**Learning:** In Tkinter, `tk.Listbox` does not have built-in support for empty states. Inserting
dummy strings into the listbox pollutes the data model and creates false affordances. **Action:**
Implement empty states using a dedicated `ttk.Label` and toggle visibility between the label and the
listbox using `pack_forget()` and `pack()` depending on the data size. To prevent layout ordering
issues when using `pack()`, wrap both the listbox and the empty state label within a dedicated
`ttk.Frame`.
