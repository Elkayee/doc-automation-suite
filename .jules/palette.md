## 2024-05-15 - Implement Listbox Empty States
**Learning:** In Tkinter, empty Listboxes provide poor UX by appearing completely blank. Adding a disabled placeholder item improves feedback but requires manual event interception to prevent invalid selections.
**Action:** Implement empty states by inserting placeholder text (`listbox.insert(0, "Empty")`), graying it out (`listbox.itemconfig(0, foreground='gray')`), and explicitly checking `listbox.itemcget(idx, 'foreground') == 'gray'` in ALL selection event handlers to return early.
