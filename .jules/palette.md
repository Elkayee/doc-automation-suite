## 2024-05-29 - Empty States for Tkinter Listboxes

**Learning:** Implementing empty states by inserting dummy strings into a `tk.Listbox` pollutes the
data model and creates false affordances. **Action:** Implement empty states using a dedicated
`ttk.Label` and toggle visibility via `pack_forget()` and `pack()`. Wrap the listbox and label
within a dedicated `ttk.Frame` to prevent `pack()` from altering the layout order in shared
containers.
