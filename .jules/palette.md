## 2026-05-25 - Improve Empty States & Hover Interaction for Listboxes

**Learning:** Empty `tk.Listbox` elements give no user feedback, which can be confusing (e.g. is the
app broken or is there just no data?). When inserting placeholder items (like "No items found") to
improve UX, it is critical to also update their selection handlers to ignore these placeholder rows
(e.g. by checking `itemcget(idx, 'foreground') == 'gray'`) so they don't trigger errors when a user
inevitably tries to click them. Setting `cursor='hand2'` via option_add works for themed widgets
(`ttk.Button`), but native ones like `tk.Listbox` require explicitly passing `cursor='hand2'` to the
constructor to improve affordance.

**Action:** Whenever introducing empty states for `Listbox` components in Tkinter, use a visual
indicator (like gray text) and ensure all event handlers (like `<Double-1>` or `<<ListboxSelect>>`)
correctly intercept and ignore clicks on that index. Use `option_add('*TButton*cursor', 'hand2')`
for global hover cursors on themed buttons.
