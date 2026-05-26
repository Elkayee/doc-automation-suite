## 2026-05-26 - Tkinter Listbox Empty States
**Learning:** Tkinter `tk.Listbox` lacks native empty state support. If empty states are simulated using placeholder strings (e.g., changing text color to gray), users can still select the placeholder text.
**Action:** When implementing placeholder strings in `tk.Listbox`, explicitly bind to `<<ListboxSelect>>` to check `listbox.itemcget(idx, 'foreground') == 'gray'` and call `listbox.selection_clear(idx)` to clear selection, preventing users from treating the placeholder as actionable data.
