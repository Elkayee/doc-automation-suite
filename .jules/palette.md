## 2024-05-24 - Handle empty Listbox states with proper UI elements

**Learning:** Inserting placeholder strings into a `tk.Listbox` creates false affordances by making
the empty state selectable and pollutes the data model. **Action:** Wrap the Listbox and a dedicated
`ttk.Label` in a `ttk.Frame`, and use `pack()`/`pack_forget()` to toggle their visibility based on
the data state.

## 2024-05-18 - Tkinter Keyboard Accessibility

**Learning:** Tkinter Toplevel dialogs and Listboxes lack automatic keyboard navigation
out-of-the-box, which breaks a11y for keyboard-only users navigating menus. **Action:** Always
manually call `.focus_set()` on primary inputs in dialogs and bind `<Return>` events to primary
actions or selections. Remember to include `event=None` in the handler signatures.
