## 2024-06-01 - Empty State Labels vs. Listbox Data Pollution
**Learning:** In Tkinter, do not implement `tk.Listbox` empty states by inserting dummy strings, as this pollutes the data model and creates false affordances.
**Action:** Implement empty states by using a dedicated `ttk.Label` and toggling visibility between the label and the listbox using `pack_forget()` and `pack()` depending on the data size. To prevent `pack()` from appending them to the end of a shared parent container and destroying the layout order, wrap the listbox and the empty state label within a dedicated `ttk.Frame`.
