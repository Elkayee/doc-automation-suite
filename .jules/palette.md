## 2024-05-19 - Tkinter Listbox Empty State
**Learning:** Tkinter listboxes do not natively support "empty states". Users can be confused when a listbox is completely blank.
**Action:** When `listbox.size() == 0`, insert a helpful placeholder string (e.g., "No items found") and visually distinguish it by setting its foreground color to gray (`listbox.itemconfig(0, foreground="gray")`). Crucially, explicitly guard event handlers (like delete or open) to return early if `listbox.itemcget(idx, "foreground") == "gray"` to prevent performing actions on the placeholder text.
