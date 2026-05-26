## 2024-05-23 - Tkinter Listbox Empty State

**Learning:** Tkinter `Listbox` doesn't have a native empty state property. Using a dummy item with
`foreground='gray'` provides a visible empty state, but requires event handlers to explicitly ignore
items with that color to prevent treating them as valid data. **Action:** Insert a placeholder and
`itemconfig(0, foreground='gray')` when a list is empty. Update selection events (`<Double-1>`,
delete actions) to ignore these placeholder items.
