## 2024-05-24 - Handle empty Listbox states with proper UI elements

**Learning:** Inserting placeholder strings into a `tk.Listbox` creates false affordances by making
the empty state selectable and pollutes the data model. **Action:** Wrap the Listbox and a dedicated
`ttk.Label` in a `ttk.Frame`, and use `pack()`/`pack_forget()` to toggle their visibility based on
the data state.

## 2024-06-09 - Keyboard Navigation in Tkinter Dialogs

**Learning:** Tkinter `Toplevel` dialogs and list components do not automatically focus inputs or
support `<Return>` submission, which creates friction for keyboard navigation. **Action:**
Explicitly call `.focus_set()` on the primary input field upon opening the dialog, and bind the
`<Return>` event to the primary submission actions (ensuring the handler accepts an optional `event`
parameter).
