## 2024-05-24 - Handle empty Listbox states with proper UI elements

**Learning:** Inserting placeholder strings into a `tk.Listbox` creates false affordances by making
the empty state selectable and pollutes the data model. **Action:** Wrap the Listbox and a dedicated
`ttk.Label` in a `ttk.Frame`, and use `pack()`/`pack_forget()` to toggle their visibility based on
the data state.

## 2024-06-11 - Tkinter Toplevel and Listbox Keyboard Navigation

**Learning:** Toplevel dialogs and listbox components in Tkinter do not natively provide keyboard
navigation expectations (such as focusing the primary entry or accepting the Enter key for
submission/selection). Without explicit focus management and event binding, keyboard-only users
cannot efficiently navigate. **Action:** Always call `.focus_set()` on the primary entry widget when
opening a `Toplevel` dialog, and explicitly bind the `<Return>` event to the primary action. Ensure
the bound action method accepts an optional `event=None` parameter.
