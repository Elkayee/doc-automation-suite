## 2024-05-28 - Tkinter Listbox Empty States

**Learning:** Inserting dummy strings into a Tkinter Listbox as an empty state pollutes the data
model, creates false affordances, and can break unit tests that assert list length. **Action:**
Implement empty states by using a dedicated `ttk.Label` and toggling visibility using
`pack_forget()` and `pack()` depending on the list size.
