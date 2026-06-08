## 2024-05-24 - Handle empty Listbox states with proper UI elements

**Learning:** Inserting placeholder strings into a `tk.Listbox` creates false affordances by making
the empty state selectable and pollutes the data model. **Action:** Wrap the Listbox and a dedicated
`ttk.Label` in a `ttk.Frame`, and use `pack()`/`pack_forget()` to toggle their visibility based on
the data state.

## 2025-06-08 - Keyboard Accessibility in Tkinter Dialogs and Listboxes

**Learning:** In Tkinter applications, `Toplevel` dialogs and list components (`tk.Listbox`) do not
automatically provide complete keyboard navigation support out of the box. Without explicit
bindings, users cannot trigger primary actions using the `<Return>` key or navigate efficiently.
**Action:** Always add explicit keyboard bindings (`<Return>`, `<Delete>`) to interactive components
like `Listbox`. When opening `Toplevel` dialogs with form inputs, immediately call `.focus_set()` on
the primary `Entry` widget so the user can start typing immediately, and bind the `<Return>` key on
the dialog to the primary action. Ensure the action function signature handles the optional event
parameter (`def action(event=None):`) to prevent `TypeError`s when triggered by key bindings.
