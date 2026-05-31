## 2024-05-31 - Empty state for Tkinter Listbox

**Learning:** In Tkinter, `tk.Listbox` doesn't have a built-in way to show an empty state. Inserting
dummy text pollutes the data model. **Action:** Use a dedicated `ttk.Label` for the empty state and
toggle visibility between the label and the listbox using `pack_forget()` and `pack()` depending on
the data size. Wrap both in a dedicated `ttk.Frame` to preserve layout order.
