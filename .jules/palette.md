## 2024-05-24 - Handle empty Listbox states with proper UI elements

**Learning:** Inserting placeholder strings into a `tk.Listbox` creates false affordances by making
the empty state selectable and pollutes the data model. **Action:** Wrap the Listbox and a dedicated
`ttk.Label` in a `ttk.Frame`, and use `pack()`/`pack_forget()` to toggle their visibility based on
the data state.

## 2024-06-04 - Handle Empty List States

**Learning:** In Tkinter, avoiding empty list states by inserting dummy placeholder strings into a
`tk.Listbox` pollutes the data model and creates false affordances. **Action:** Wrap the Listbox and
a dedicated `ttk.Label` in a `ttk.Frame`, and use `pack()`/`pack_forget()` to toggle their
visibility based on the data state.
