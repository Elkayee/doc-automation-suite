## 2024-05-24 - Handle empty Listbox states with proper UI elements

**Learning:** Inserting placeholder strings into a `tk.Listbox` creates false affordances by making
the empty state selectable and pollutes the data model. **Action:** Wrap the Listbox and a dedicated
`ttk.Label` in a `ttk.Frame`, and use `pack()`/`pack_forget()` to toggle their visibility based on
the data state.

## 2024-06-10 - Keyboard accessibility in Tkinter dialogs and lists

**Learning:** Tkinter `Toplevel` dialogs and list components do not automatically provide keyboard
navigation support out of the box (like auto-focusing inputs or `<Return>` bindings for primary
actions). **Action:** Explicitly call `.focus_set()` on primary entry fields when opening dialogs,
and bind `<Return>` events (ensuring the action function accepts an optional event parameter) to
improve keyboard accessibility.
