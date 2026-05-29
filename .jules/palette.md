## 2024-05-29 - Empty States in Tkinter Data Views

**Learning:** Tkinter `tk.Listbox` widgets do not have a built-in "empty text" placeholder property
like modern web or mobile frameworks. Inserting dummy items (e.g. "No projects") pollutes the data
model and can trigger unintended selection events if the user interacts with the list. **Action:**
Always implement empty states for data views in Tkinter by creating a dedicated `ttk.Label` with
italicized or gray text, and toggle the visibility between the `Listbox` and the `Label` using
`pack_forget()` and `pack()` based on the actual data length during the refresh/render cycle.
