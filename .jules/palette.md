## 2024-05-28 - Tkinter Listbox Empty States

**Learning:** Standard Tkinter Listbox widgets lack built-in empty states, leaving users without
guidance when lists are empty. **Action:** Implement empty states by inserting a distinct
placeholder string (e.g., foreground='gray') and adding early returns in event handlers to ignore
selections of the placeholder item.
