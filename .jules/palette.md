## 2025-02-28 - Implement Tkinter Listbox Empty States and Cursors

**Learning:** Tkinter listboxes lack a native empty state. Inserting placeholder text requires
carefully styling it (e.g., gray text) and updating all event handlers (double-click, delete, open)
to explicitly check the item's color and ignore actions on the placeholder. Additionally, ttk.Button
cursors must be set globally via `option_add`. **Action:** When using tk.Listbox, insert placeholder
text when size is 0, style it distinctively, and check `listbox.itemcget(idx, 'foreground')` in all
handlers to prevent invalid state errors. Set cursor='hand2' for better interactivity.
