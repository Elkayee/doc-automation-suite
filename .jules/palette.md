## 2025-05-08 - Tkinter Listbox Empty State UX

**Learning:** Tkinter listboxes don't have built-in empty state handling, which can cause poor UX
and potential errors if empty areas are clicked. Adding a visual placeholder string (e.g. 'Chua co
du an nao. Hay tao moi!') and styling it gray provides clear feedback to the user, but requires
careful handling in event bindings. **Action:** When inserting placeholder text in a Tkinter
listbox, visually distinguish it (e.g. `listbox.itemconfig(0, foreground='gray')`), and update ALL
relevant event handlers (like double-click or delete actions) to explicitly check the item color
(`listbox.itemcget(idx, 'foreground') == 'gray'`) and return early to prevent invalid actions on the
placeholder text. Also, ensure interactive elements like buttons and listboxes use `cursor='hand2'`
to improve visual feedback on hover.

## 2024-05-24 - Handle empty Listbox states with dedicated Labels

**Learning:** Inserting dummy text strings into a `tk.Listbox` to represent an empty state pollutes
the data model, requires brittle checks (like checking foreground color) in event handlers, and
creates false affordances. **Action:** Always wrap the `tk.Listbox` and a dedicated `ttk.Label` in a
`ttk.Frame`, and use `pack()`/`pack_forget()` to toggle their visibility based on the underlying
data state.
