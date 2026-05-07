## 2024-05-07 - Tkinter Listbox Empty States

**Learning:** In Tkinter, `Listbox` lacks native support for unselectable placeholder items or empty
states. Using an empty state improves UX by guiding users on what to do (e.g., "Chua co du an nao.
Click '+ Tao Du An Moi' de bat dau."), but it creates an interaction challenge because users can
still select the placeholder. **Action:** When implementing an empty state in a Tkinter `Listbox`,
insert the placeholder text, style it uniquely (e.g., `listbox.itemconfig(0, foreground='gray')`),
and update ALL relevant event handlers (like double-click, open, or delete buttons) to explicitly
check `listbox.itemcget(idx, 'foreground') == 'gray'` and return early to prevent invalid actions on
the placeholder text.
