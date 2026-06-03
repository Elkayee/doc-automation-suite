## 2024-06-03 - Avoid Data Model Pollution in UI Components

**Learning:** Storing dummy textual placeholders like "No items found" inside data models (like
`tk.Listbox`) creates false affordances, requires fragile color-based workarounds to disable clicks,
and pollutes the underlying data representation. **Action:** When handling empty states, wrap the
main component and a dedicated placeholder label in a container frame. Toggle their visibility
(e.g., using `pack()` and `pack_forget()` in Tkinter) rather than inserting fake entries into the
list.
