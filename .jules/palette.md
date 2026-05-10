## 2025-05-10 - Improved Empty State for Listboxes

**Learning:** Empty listboxes in Tkinter provide no guidance. Applying a standard UX practice where
we insert a placeholder string ("Chua co du an nao. Hay tao moi.") and visually distinguish it using
`foreground='gray'` improves user feedback. **Action:** When creating empty states in listboxes,
always ensure we update related event handlers (e.g. `Double-1` to open, or explicit action buttons
like Delete) to check if the clicked item is the placeholder
(`itemcget(idx, 'foreground') == 'gray'`) and return early.
