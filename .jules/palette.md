## 2024-05-24 - Handle empty Listbox states with proper UI elements

**Learning:** Inserting placeholder strings into a `tk.Listbox` creates false affordances by making
the empty state selectable and pollutes the data model. **Action:** Wrap the Listbox and a dedicated
`ttk.Label` in a `ttk.Frame`, and use `pack()`/`pack_forget()` to toggle their visibility based on
the data state.

## 2024-06-09 - Keyboard Navigation in Tkinter Modals and Lists

**Learning:** `Toplevel` dialogs and list components in Tkinter do not automatically provide
keyboard navigation support (such as auto-focusing inputs or submitting actions via the `<Return>`
key). **Action:** Explicitly call `.focus_set()` on primary entry fields when opening dialogs, and
bind `<Return>` events to primary actions, ensuring the action function accepts an optional event
parameter.
