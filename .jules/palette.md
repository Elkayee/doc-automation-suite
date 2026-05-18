## 2026-05-15 - Visually distinct empty state for Tkinter Listbox

**Learning:** Tkinter Listboxes don't have built-in empty states. Inserting placeholder text can
lead to bugs if users try to interact with it. **Action:** When a Listbox is empty, insert a
placeholder string, set its color to gray (`listbox.itemconfig(0, foreground='gray')`), and
explicitly check for this color (`if listbox.itemcget(idx, 'foreground') == 'gray': return`) in all
relevant event handlers to prevent invalid actions.
