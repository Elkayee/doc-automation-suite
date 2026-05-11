## 2024-05-11 - Tkinter Listbox Empty States

**Learning:** In Tkinter, implementing a listbox empty state requires explicitly inserting
placeholder text and visually distinguishing it (e.g., using
`listbox.itemconfig(0, foreground='gray')`). Since it's actual text in the listbox, ALL relevant
event handlers (double click, delete actions, etc.) must explicitly check for the placeholder's
distinguishing feature (like `listbox.itemcget(idx, 'foreground') == 'gray'`) and return early to
prevent actions on the placeholder text. **Action:** When implementing an empty state in Tkinter
listboxes, always set a distinguishing property (like foreground color) and add early returns in all
event handlers for items matching that property.
