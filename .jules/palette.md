## 2024-05-23 - Improve Tkinter Listbox empty state and cursor feedback

**Learning:** Tkinter Listboxes don't have built-in empty states or nice hover pointers like web
apps do. Assigning placeholder items and setting them to 'gray', and enabling 'hand2' cursor on
listbox and globally on '*TButton*cursor' significantly improves interaction and accessibility cues.
**Action:** Always provide placeholder text with different foreground colors for empty listboxes and
ignore selection events for those items. Use `option_add` for global cursors on ttk components.
