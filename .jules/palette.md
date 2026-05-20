## 2025-05-20 - Tkinter interactive cursors and empty states

**Learning:** Tkinter native elements lack modern affordances like hover cursors and disabled states
for empty list views. Users may interact with placeholder texts, causing application errors, and
lack visual feedback when buttons are clickable. Note that ttk.Button cursors must be set via the
root option database `option_add('*TButton*cursor', 'hand2')` instead of style configuration.
**Action:** When working with Tkinter interfaces, always configure `cursor='hand2'` for interactive
elements like buttons and listboxes to provide feedback. Implement empty states by inserting a
distinctly styled placeholder (e.g., `foreground='gray'`) and ensure event handlers check
`itemcget(idx, 'foreground') == 'gray'` to abort actions on placeholder text.
