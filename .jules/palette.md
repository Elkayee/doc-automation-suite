## 2024-05-24 - Handle empty Listbox states with proper UI elements

**Learning:** Inserting placeholder strings into a `tk.Listbox` creates false affordances by making
the empty state selectable and pollutes the data model. **Action:** Wrap the Listbox and a dedicated
`ttk.Label` in a `ttk.Frame`, and use `pack()`/`pack_forget()` to toggle their visibility based on
the data state.

## 2026-06-04 - Improve Tkinter dialog keyboard accessibility
**Learning:** By default, Tkinter dialogs and lists lack keyboard support for primary actions. Users expect Enter to submit forms and open selected items.
**Action:** Bind `<Return>` to primary actions and set initial focus on the first input field (`.focus_set()`) to improve keyboard navigation.
