## 2024-05-24 - Handle empty Listbox states with proper UI elements

**Learning:** Inserting placeholder strings into a `tk.Listbox` creates false affordances by making
the empty state selectable and pollutes the data model. **Action:** Wrap the Listbox and a dedicated
`ttk.Label` in a `ttk.Frame`, and use `pack()`/`pack_forget()` to toggle their visibility based on
the data state.

## 2024-05-18 - Disable project deletion button when no project is selected

**Learning:** Destructive actions (like "Xoa Du An") should visually indicate when they are not
applicable by using a disabled state. Previously, the button was always clickable, but would show a
warning dialog if clicked without a selection. **Action:** Add disabled state to the button
initially and bind listbox select event to toggle disabled state based on selection.
