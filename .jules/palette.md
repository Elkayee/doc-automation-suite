## 2024-05-25 - Empty states in Tkinter Listbox
**Learning:** Tkinter doesn't have built-in empty states for Listbox widgets, which can leave users confused when a list is completely empty. Users might think the application is broken.
**Action:** Implement empty states by inserting a placeholder string, setting its color to gray (`listbox.itemconfig(0, foreground='gray')`), and updating event handlers to ignore selections where the item foreground is gray.
