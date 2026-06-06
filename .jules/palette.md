## 2024-05-24 - Handle empty Listbox states with proper UI elements

**Learning:** Inserting placeholder strings into a `tk.Listbox` creates false affordances by making
the empty state selectable and pollutes the data model. **Action:** Wrap the Listbox and a dedicated
`ttk.Label` in a `ttk.Frame`, and use `pack()`/`pack_forget()` to toggle their visibility based on
the data state.

## 2025-02-18 - Tkinter Keyboard Accessibility

**Learning:** Tkinter dialogs and lists lack default keyboard navigation like "Return" to submit or
open items, and entry fields are not auto-focused by default, forcing mouse usage. **Action:**
Always add `.focus_set()` to primary entry fields and bind `<Return>` events to critical actions
(submitting dialogs, opening list items) to ensure screen-reader/keyboard-only accessibility.
