## 2025-05-31 - Add empty state for Dashboard projects list

**Learning:** Empty listboxes without visual feedback create uncertainty. Users might wonder if data
is still loading or if they need to perform an action. In Tkinter, empty states shouldn't be dummy
listbox items as it creates false interactive affordances. **Action:** Use a dedicated `ttk.Label`
wrapped in a `ttk.Frame` along with the listbox, toggling their visibility with `pack()` and
`pack_forget()` based on data presence to provide clear guidance when lists are empty.
