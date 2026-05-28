## 2024-05-28 - Implement Empty States for Listboxes

**Learning:** When dealing with standard Tkinter `Listbox` widgets, inserting dummy strings to
represent an empty state pollutes the data model and creates false affordances. It is much better UX
and accessibility practice to use a dedicated label and toggle visibility.

**Action:** Implement empty states using a dedicated `ttk.Label` and toggle visibility between the
label and the listbox using `pack_forget()` and `pack()` depending on the data size.
