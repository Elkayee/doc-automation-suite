## 2024-05-24 - Handle empty Listbox states with proper UI elements

**Learning:** Inserting placeholder strings into a `tk.Listbox` creates false affordances by making
the empty state selectable and pollutes the data model. **Action:** Wrap the Listbox and a dedicated
`ttk.Label` in a `ttk.Frame`, and use `pack()`/`pack_forget()` to toggle their visibility based on
the data state.

## 2024-05-24 - Improve Tkinter dialog keyboard accessibility

**Learning:** Tkinter `Toplevel` dialogs do not automatically focus inputs or support submitting via
the Enter key, degrading keyboard accessibility. **Action:** Always call `.focus_set()` on primary
inputs and bind `<Return>` to the submit action (ensuring the action function accepts an optional
`event` parameter).
