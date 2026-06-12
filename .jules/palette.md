## 2024-05-24 - Handle empty Listbox states with proper UI elements

**Learning:** Inserting placeholder strings into a `tk.Listbox` creates false affordances by making
the empty state selectable and pollutes the data model. **Action:** Wrap the Listbox and a dedicated
`ttk.Label` in a `ttk.Frame`, and use `pack()`/`pack_forget()` to toggle their visibility based on
the data state.

## 2024-06-12 - Tkinter Toplevel keyboard accessibility

**Learning:** `Toplevel` dialogs in Tkinter do not automatically focus input fields or bind the
`<Return>` key to default actions, which breaks keyboard accessibility and forces mouse usage.
**Action:** When creating `Toplevel` dialogs, explicitly call `.focus_set()` on the primary entry
widget and bind `<Return>` to the primary action function (ensuring the action function accepts an
optional `event=None` argument).
