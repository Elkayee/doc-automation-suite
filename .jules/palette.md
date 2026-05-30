## 2024-05-30 - Added Empty State to Projects List

**Learning:** In Tkinter, empty states for a `tk.Listbox` should not be implemented by inserting
dummy strings into the listbox itself, as this creates false interactive affordances and pollutes
the data model. **Action:** Always wrap the listbox in a `ttk.Frame` alongside a dedicated
`ttk.Label` for the empty state, toggling their visibility using `pack()` and `pack_forget()` based
on data presence.
