## 2024-05-10 - Tkinter Interactive Cursor & Empty State Handling

**Learning:** Tkinter `Listbox` widgets do not support native empty states out of the box.
Additionally, Tkinter interactive widgets (like buttons and listboxes) do not show the expected
`hand2` cursor by default, leading to poor visual feedback. When implementing an empty state by
inserting a placeholder text into a `Listbox`, it's critical to ensure all event handlers (like
click/double-click) explicitly check for the placeholder item's formatting (e.g.,
`itemcget(idx, 'foreground') == 'gray'`) and return early. Otherwise, users might trigger actions
(like deleting or opening a project) on the placeholder itself, causing confusing errors.
**Action:** Always configure `cursor='hand2'` for interactive Tkinter elements (either globally via
`ttk.Style` or individually). When adding text-based empty states to a `Listbox`, differentiate them
visually (e.g., using a gray color) and always guard downstream event handlers against acting on the
placeholder text.
