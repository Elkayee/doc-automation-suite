## 2024-05-23 - Handle Empty States in Tkinter Listboxes

**Learning:** Tkinter Listboxes don't have built-in empty states, which leads to poor UX when lists
are empty. **Action:** Use a placeholder string formatted differently (e.g., foreground='gray') and
guard event handlers by checking `itemcget(idx, 'foreground') == 'gray'` to ensure empty states are
not processed.
