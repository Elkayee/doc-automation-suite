## 2024-05-24 - Handle empty Listbox states with dedicated Labels

**Learning:** In Tkinter, inserting dummy placeholder strings (like "Chua co du an nao") into a
`tk.Listbox` pollutes the data model and creates false affordances, allowing users to select the
empty state message. **Action:** Wrap the Listbox and a dedicated `ttk.Label` inside a parent
`ttk.Frame`, and use `pack()`/`pack_forget()` to toggle their visibility based on the data state.
This keeps the data model clean and provides a clearer, non-interactive visual indicator for empty
states.
