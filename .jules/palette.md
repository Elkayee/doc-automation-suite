## 2026-05-10 - Tkinter Listbox Empty State UX

**Learning:** In Tkinter `Listbox` components, a placeholder empty state must be simulated by
inserting literal text when `size() == 0` and visually differentiating it with a color like
`foreground='gray'`. Since this text becomes selectable, it's critical to update _all_ event
handlers (like double-click and custom delete actions) to check
`itemcget(idx, 'foreground') == 'gray'` and return early. Otherwise, users can trigger actions on
the placeholder text. **Action:** Always pair a simulated empty state in a `Listbox` with defensive
`itemcget` color checks in associated event handlers to prevent invalid actions. Apply
`cursor='hand2'` to interactive widgets (like `Listbox` and buttons) to improve feedback on hover.
