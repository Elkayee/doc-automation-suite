## 2024-05-29 - Empty States in Tkinter Listboxes

**Learning:** Hardcoding dummy strings into Tkinter `tk.Listbox` for empty states creates false
affordances and pollutes the data model.

**Action:** Implement empty states by toggling visibility (`pack`/`pack_forget`) between the listbox
and a dedicated `ttk.Label` wrapped in a `ttk.Frame` to preserve layout order.
