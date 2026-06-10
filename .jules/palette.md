## 2024-05-24 - Handle empty Listbox states with proper UI elements

**Learning:** Inserting placeholder strings into a `tk.Listbox` creates false affordances by making
the empty state selectable and pollutes the data model. **Action:** Wrap the Listbox and a dedicated
`ttk.Label` in a `ttk.Frame`, and use `pack()`/`pack_forget()` to toggle their visibility based on
the data state.

## 2024-06-10 - Add keyboard navigation support for Tkinter components

**Learning:** `Toplevel` dialogs and Tkinter list components lack automatic keyboard navigation.
**Action:** Use `.focus_set()` on primary entry fields, and bind `<Return>` to primary action
functions (making sure they accept an optional `event=None` argument).
