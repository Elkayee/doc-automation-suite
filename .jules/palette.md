## 2024-05-18 - Missing empty states for Listbox

**Learning:** In Tkinter, displaying an empty Listbox without a clear "No items" message creates a
confusing experience. Users might think the list is still loading or broken, missing the fact that
it's intentionally empty. **Action:** Always provide an empty state label when a list is empty.
Instead of inserting fake items into the Listbox which pollutes the data model, use a separate
`ttk.Label` and swap visibility using `pack()` and `pack_forget()`. Wrap both in a dedicated
`ttk.Frame` to preserve layout ordering when packing and unpacking.
