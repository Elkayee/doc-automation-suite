## 2024-05-28 - Tkinter Empty States

**Learning:** Empty states in Tkinter are best implemented by toggling visibility
(`pack_forget()`/`pack()`) of a dedicated `ttk.Label` rather than inserting dummy strings into a
`Listbox`, which pollutes the data model and creates false affordances. **Action:** Always implement
empty states by conditionally packing a dedicated label when the data model is empty.
