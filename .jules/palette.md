## 2025-02-06 - Tkinter Interactive Element Hover Cursors

**Learning:** Tkinter `ttk.Button` and `tk.Listbox` elements do not inherently display a pointer
cursor (hand) when hovered, which differs from modern web or standard UI frameworks. This lack of
visual feedback degrades the UX as interactive elements are less discoverable. **Action:** Always
explicitly configure `cursor='hand2'` on Tkinter interactive components (e.g.
`ttk.Style().configure('TButton', cursor='hand2')` and `tk.Listbox(..., cursor='hand2')`) to provide
proper visual feedback that the element is clickable.
