## 2024-05-24 - Handle empty Listbox states with proper UI elements

**Learning:** Inserting placeholder strings into a `tk.Listbox` creates false affordances by making
the empty state selectable and pollutes the data model. **Action:** Wrap the Listbox and a dedicated
`ttk.Label` in a `ttk.Frame`, and use `pack()`/`pack_forget()` to toggle their visibility based on
the data state.

## 2024-05-24 - Enable keyboard navigation for Toplevel dialogs and Listboxes

**Learning:** Tkinter `Toplevel` dialogs and list components do not automatically provide keyboard
navigation support, forcing users to rely on mouse clicks for primary interactions.

**Action:** Always call `.focus_set()` on the primary entry field when opening dialogs, and
explicitly bind `<Return>` events to primary actions (ensuring action functions accept an optional
event parameter).
