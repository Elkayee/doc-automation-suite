## 2024-05-24 - Handle empty Listbox states with proper UI elements

**Learning:** Inserting placeholder strings into a `tk.Listbox` creates false affordances by making
the empty state selectable and pollutes the data model. **Action:** Wrap the Listbox and a dedicated
`ttk.Label` in a `ttk.Frame`, and use `pack()`/`pack_forget()` to toggle their visibility based on
the data state.

## 2025-06-16 - Tkinter Dialog Keyboard Accessibility

**Learning:** Toplevel dialogs and Entry components in Tkinter do not automatically support keyboard
navigation, causing poor UX for users who prefer using the keyboard to type and submit forms
quickly. **Action:** Always call `.focus_set()` on the primary `ttk.Entry` field when a dialog opens
to immediately capture keyboard focus. Additionally, bind the `<Return>` event on the dialog
(`dialog.bind('<Return>', action_function)`) to trigger the primary submission action, and ensure
the action function signature includes an optional event parameter
(`def action_function(event=None):`).
