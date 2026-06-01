## 2024-06-01 - Empty State for Project List
**Learning:** Tkinter Listboxes without data create false affordances. A dedicated `ttk.Label` within a `ttk.Frame` is required to display an empty state properly.
**Action:** Implement empty states by using a dedicated label and toggling visibility between the label and listbox with `pack_forget()` and `pack()` depending on data availability.
