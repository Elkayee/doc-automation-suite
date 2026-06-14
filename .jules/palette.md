## 2024-05-24 - Handle empty Listbox states with proper UI elements

**Learning:** Inserting placeholder strings into a `tk.Listbox` creates false affordances by making
the empty state selectable and pollutes the data model. **Action:** Wrap the Listbox and a dedicated
`ttk.Label` in a `ttk.Frame`, and use `pack()`/`pack_forget()` to toggle their visibility based on
the data state.

## 2024-06-14 - Keyboard Accessibility in Tkinter Dialogs

**Learning:** Tkinter `Toplevel` dialogs do not automatically focus input fields or support
submitting forms via the `<Return>` key, which creates a frustrating mouse-dependent experience.
**Action:** When creating new Tkinter dialogs with forms, explicitly call `.focus_set()` on the
primary input field, modify the submit action signature to accept an optional event
(`def action(event=None):`), and bind the `<Return>` event on the dialog to that action.
