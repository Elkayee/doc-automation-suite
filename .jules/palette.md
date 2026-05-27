## 2024-05-27 - Implement Listbox empty states in Tkinter

**Learning:** Tkinter's `tk.Listbox` does not have a built-in "empty state" property. Without an
empty state, users may feel lost when no data is present. A simple placeholder improves the user
experience by guiding them to create new items.

**Action:** Implement an empty state by inserting a placeholder string when the list is empty,
setting its color to be visually distinct (e.g., `listbox.itemconfig(0, foreground='gray')`). Update
event handlers (`<Double-1>`, delete operations) to check
`listbox.itemcget(idx, 'foreground') == 'gray'`, clear the selection, and return early so the
placeholder is not treated as actionable data.
