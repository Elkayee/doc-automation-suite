## 2023-10-27 - Tkinter Listbox Empty States

**Learning:** Inserting dummy strings into `tk.Listbox` to show an empty state pollutes the data
model and creates false affordances. **Action:** Implement empty states by wrapping the `Listbox`
and a dedicated `ttk.Label` in a shared `ttk.Frame`, then toggling their visibility using `pack()`
and `pack_forget()` based on data size. This preserves the layout order and keeps the data model
clean.
