## 2024-05-24 - Handle empty Listbox states with proper UI elements

**Learning:** Inserting placeholder strings into a `tk.Listbox` creates false affordances by making
the empty state selectable and pollutes the data model. **Action:** Wrap the Listbox and a dedicated
`ttk.Label` in a `ttk.Frame`, and use `pack()`/`pack_forget()` to toggle their visibility based on
the data state.

## 2024-05-25 - Tkinter Dialog Keyboard Accessibility

**Learning:** Toplevel dialogs in Tkinter don't automatically focus inputs or support form
submission via the Enter key, degrading keyboard usability. **Action:** Explicitly assign focus to
the primary input using `.focus_set()` and bind `<Return>` to the primary submission action
(ensuring the action function accepts an `event=None` argument).
