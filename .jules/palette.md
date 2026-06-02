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

## 2024-06-02 - Listbox Empty State UX Improvement

**Learning:** Inserting dummy text into a Tkinter `Listbox` to act as an empty state pollutes the
data model, leads to bad click behavior, and creates false affordances. **Action:** Use a dedicated
`ttk.Label` for the empty state and toggle its visibility against the `Listbox` using
`pack()`/`pack_forget()`. Wrap them in a container frame so toggling doesn't break the parent
layout.
