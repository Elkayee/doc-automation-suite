## 2024-05-24 - Handle empty Listbox states with proper UI elements

**Learning:** Inserting placeholder strings into a `tk.Listbox` creates false affordances by making
the empty state selectable and pollutes the data model. **Action:** Wrap the Listbox and a dedicated
`ttk.Label` in a `ttk.Frame`, and use `pack()`/`pack_forget()` to toggle their visibility based on
the data state.

## 2024-05-18 - Improve Tkinter Dashboard Keyboard Accessibility

**Learning:** Tkinter components like `Toplevel` dialogs and `Listbox` components do not have
inherent keyboard navigation like autofocusing inputs or mapping the `<Return>` key to default
actions, which significantly degrades the desktop UX for keyboard-first users. **Action:** When
adding Toplevel dialogs with inputs, explicitly call `.focus_set()` on the primary entry widget.
Additionally, map `<Return>` and `<Escape>` key events to the default submit and close actions to
make the flow smooth.
