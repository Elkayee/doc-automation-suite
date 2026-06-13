## 2024-05-24 - Handle empty Listbox states with proper UI elements

**Learning:** Inserting placeholder strings into a `tk.Listbox` creates false affordances by making
the empty state selectable and pollutes the data model. **Action:** Wrap the Listbox and a dedicated
`ttk.Label` in a `ttk.Frame`, and use `pack()`/`pack_forget()` to toggle their visibility based on
the data state.

## 2024-06-13 - Tkinter Keyboard Accessibility

**Learning:** Tkinter components like Toplevel dialogs and Listboxes do not automatically focus
input fields or provide <Return> key submissions. **Action:** Always call `.focus_set()` on primary
entry fields and explicitly bind `<Return>` to action functions (remembering to add `event=None` to
the function signature).
