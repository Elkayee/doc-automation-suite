## 2024-05-24 - Tkinter Listbox Empty State

**Learning:** Tkinter `Listbox` components do not have a built-in `empty_text` property like some
modern UI frameworks. This can lead to a confusing UX when lists (like recent projects) are empty.
**Action:** Use `listbox.size() == 0` to check for empty states during refresh, insert a placeholder
string (e.g., `--- Chua co du an nao ---`), and style it using
`listbox.itemconfig(0, foreground='gray')` to visually distinguish it from selectable items. Ensure
click/delete handlers return early if the selected item matches the placeholder string.
