## 2024-05-24 - Tkinter Listbox Empty State Pattern

**Learning:** In Tkinter, `tk.Listbox` doesn't have a native "empty state" or placeholder property.
When lists are empty, it leaves a confusing blank white space. **Action:** Implement empty states by
inserting a placeholder string (e.g., `(No projects)`) when `listbox.size() == 0`, visually
distinguishing it with `listbox.itemconfig(0, foreground='gray')`. Crucially, update ALL relevant
event handlers (e.g., double-click, delete buttons) to explicitly check
`if listbox.itemcget(idx, 'foreground') == 'gray'` and return early to prevent the application from
treating the placeholder text as valid user data.

## 2024-05-24 - Tkinter Cursor Hover State

**Learning:** Tkinter `ttk.Button` elements do not show a pointer/hand cursor on hover by default,
which violates common web/desktop UX expectations for clickable elements. Setting `cursor='hand2'`
via `ttk.Style().configure` does not work for `ttk.Button`. **Action:** Apply the hand cursor
globally to all `ttk.Button` instances using the Tk option database:
`root.option_add('*TButton*cursor', 'hand2')`. For `tk.Listbox`, pass `cursor='hand2'` explicitly
via widget kwargs during initialization.
