## 2025-05-31 - Empty States in Tkinter Listboxes
**Learning:** Implementing empty states by inserting dummy strings into a Listbox pollutes the data model and creates false affordances.
**Action:** Implement empty states by wrapping the Listbox and a dedicated ttk.Label in a ttk.Frame, and use pack_forget()/pack() to toggle visibility based on data size. This preserves the layout order without polluting the underlying Listbox data.
