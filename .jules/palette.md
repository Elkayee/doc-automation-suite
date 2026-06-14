## 2024-05-24 - Handle empty Listbox states with proper UI elements

**Learning:** Inserting placeholder strings into a `tk.Listbox` creates false affordances by making
the empty state selectable and pollutes the data model. **Action:** Wrap the Listbox and a dedicated
`ttk.Label` in a `ttk.Frame`, and use `pack()`/`pack_forget()` to toggle their visibility based on
the data state.

## 2026-06-14 - Keyboard Accessibility in Tkinter Dialogs

**Learning:** Tkinter `Toplevel` dialogs and forms do not automatically receive keyboard focus or
map the `<Return>` key to default actions, which creates friction for keyboard navigation.
**Action:** When creating a dialog, explicitly capture the primary input field into a variable and
call `.focus_set()` on it so the user can type immediately. Additionally, update the primary action
function (e.g., `do_create(event=None)`) to accept an event and bind `<Return>` on the dialog to
that function (`dialog.bind('<Return>', do_create)`).
