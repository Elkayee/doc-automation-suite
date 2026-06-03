## 2025-06-03 - Avoid polluting Tkinter Listbox with placeholder data

**Learning:** Inserting dummy placeholder strings (like "No projects available") into a `tk.Listbox`
pollutes the data model, requiring fragile checks (`itemcget('foreground') == 'gray'`) in all event
handlers to ignore them, and creates false affordances. **Action:** Wrap the Listbox and a dedicated
`ttk.Label` in a `ttk.Frame`, and toggle their visibility using `pack()` and `pack_forget()` based
on whether the data is empty.
