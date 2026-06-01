## 2024-06-01 - Tkinter Empty States

**Learning:** Inserting dummy strings into Tkinter Listboxes for empty states pollutes the data
model and creates false affordances. **Action:** Implement empty states using a dedicated
`ttk.Label` wrapped in a `ttk.Frame` alongside the Listbox, toggling visibility with `pack()` and
`pack_forget()`.
