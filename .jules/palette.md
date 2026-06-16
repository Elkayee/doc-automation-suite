## 2024-05-24 - Handle empty Listbox states with proper UI elements

**Learning:** Inserting placeholder strings into a `tk.Listbox` creates false affordances by making
the empty state selectable and pollutes the data model. **Action:** Wrap the Listbox and a dedicated
`ttk.Label` in a `ttk.Frame`, and use `pack()`/`pack_forget()` to toggle their visibility based on
the data state.

## 2026-06-16 - Add keyboard navigation support to Tkinter dialogs

**Learning:** Tkinter `Toplevel` dialogs do not automatically focus their input fields or submit
forms via the `<Return>` key. **Action:** Explicitly call `.focus_set()` on the primary entry widget
and bind `<Return>` to the primary action function (ensuring it accepts an `event` parameter).
