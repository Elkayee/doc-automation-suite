## 2024-05-24 - Handle empty Listbox states with proper UI elements

**Learning:** Inserting placeholder strings into a `tk.Listbox` creates false affordances by making
the empty state selectable and pollutes the data model. **Action:** Wrap the Listbox and a dedicated
`ttk.Label` in a `ttk.Frame`, and use `pack()`/`pack_forget()` to toggle their visibility based on
the data state.

## 2024-06-14 - Keyboard Accessibility in Tkinter Dialogs

**Learning:** By default, Tkinter Toplevel dialogs and listbox items do not offer intuitive keyboard
accessibility out-of-the-box. Users cannot press Enter to trigger the default primary action, and
inputs are not automatically focused. **Action:** When creating new dialogs, always call
`.focus_set()` on the primary input field. Furthermore, bind the `<Return>` event to the primary
action function, ensuring the function signature includes `event=None` so it can handle both button
clicks and keybinds.
