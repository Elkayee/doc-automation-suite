## 2024-06-01 - Add Empty State to Project Listbox
**Learning:** Empty listboxes present a poor UX as they leave users unsure if the app is broken or if they just have no items. Adding a dedicated empty state label improves clarity and provides an implicit call-to-action ("Create a new project to begin").
**Action:** Use `pack_forget()` and `pack()` to toggle between a `tk.Listbox` and a `ttk.Label` within a shared `ttk.Frame` container depending on whether the list is empty.
