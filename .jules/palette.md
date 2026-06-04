## 2024-05-24 - Handle empty Listbox states with proper UI elements

**Learning:** Inserting placeholder strings into a `tk.Listbox` creates false affordances by making
the empty state selectable and pollutes the data model. **Action:** Wrap the Listbox and a dedicated
`ttk.Label` in a `ttk.Frame`, and use `pack()`/`pack_forget()` to toggle their visibility based on
the data state.

## 2024-05-23 - Add Keyboard Navigation to Dashboard Forms

**Learning:** Users expect to be able to navigate lists and submit dialog forms (like "Create
Project") using the Enter key. In Tkinter, setting initial focus with `focus_set()` on entry fields
and binding `<Return>` to submit actions drastically improves the micro-UX and keyboard
accessibility without needing visual changes. **Action:** Always bind `<Return>` to standard
submit/open actions and set initial focus on the first input field in dialogs.
