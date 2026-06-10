## 2024-05-24 - Handle empty Listbox states with proper UI elements

**Learning:** Inserting placeholder strings into a `tk.Listbox` creates false affordances by making
the empty state selectable and pollutes the data model. **Action:** Wrap the Listbox and a dedicated
`ttk.Label` in a `ttk.Frame`, and use `pack()`/`pack_forget()` to toggle their visibility based on
the data state.

## 2024-05-24 - Enable keyboard navigation in Tkinter UI elements

**Learning:** Tkinter Toplevel dialogs and Listbox components lack automatic keyboard navigation
(like `<Return>` to submit or `<Delete>` to remove). **Action:** Use `focus_set()` to focus the
primary entry upon opening a dialog, and bind standard keys (`<Return>`, `<Delete>`) to the
corresponding actions, ensuring callback signatures accept an optional `event` parameter.
