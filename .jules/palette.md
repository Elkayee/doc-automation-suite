## 2024-05-24 - Tkinter Hover Cursors and Listbox Empty States

**Learning:** Setting the cursor property on `ttk.Style().configure('TButton')` doesn't work for
hover states in Tkinter; it must be applied globally via the option database
(`root.option_add('*TButton*cursor', 'hand2')`). Additionally, `tk.Listbox` lacks native empty state
support, so placeholder strings must be inserted with distinct colors (like `gray`), and event
handlers must explicitly block interactions on these gray placeholder items. **Action:** Always
apply hand cursors globally in Tkinter apps, and implement manual listbox empty states by verifying
`itemcget(idx, 'foreground') == 'gray'` in click/delete handlers.
