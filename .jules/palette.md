## 2024-05-09 - Handling Empty States in Tkinter Listboxes

**Learning:** Tkinter `tk.Listbox` widgets do not have a built-in "empty state" property. Leaving a
listbox blank provides a poor UX, but inserting a placeholder string creates a problem where user
actions (like double-click or delete selection events) might attempt to process the placeholder text
as actual data, leading to errors. **Action:** When implementing listbox empty states, always insert
the placeholder string explicitly when `size() == 0`, style it distinctively using
`itemconfig(0, foreground='gray')`, and critically, update ALL associated event handlers to check
`itemcget(idx, 'foreground') == 'gray'` and return early to safely ignore user interaction on the
placeholder item.
