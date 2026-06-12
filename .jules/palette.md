## 2024-05-24 - Handle empty Listbox states with proper UI elements

**Learning:** Inserting placeholder strings into a `tk.Listbox` creates false affordances by making
the empty state selectable and pollutes the data model. **Action:** Wrap the Listbox and a dedicated
`ttk.Label` in a `ttk.Frame`, and use `pack()`/`pack_forget()` to toggle their visibility based on
the data state.

## 2025-05-15 - Tkinter Keyboard Accessibility

**Learning:** Tkinter dialogs and lists do not have built-in keyboard navigation support, such as
focusing on entry elements automatically or supporting `<Return>` key actions. **Action:** Always
add keyboard accessibility features by explicitly calling `.focus_set()` on primary inputs in
dialogs, and binding `<Return>` to confirm primary actions. Ensure event handlers bound this way
accept an optional event argument (e.g., `event=None`).
