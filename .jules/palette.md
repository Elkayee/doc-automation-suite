## 2024-05-12 - Add tk.Listbox Empty State Pattern

**Learning:** Tkinter `tk.Listbox` lacks a built-in empty state. Simply inserting a placeholder text
and setting its foreground color to gray creates the visual cue, but ALL event handlers bound to
selection/actions must explicitly check the foreground color
(`listbox.itemcget(idx, 'foreground') == 'gray'`) and return early to prevent the placeholder from
being treated as actual user data. Additionally, assigning `cursor='hand2'` explicitly to
interactive widgets like `tk.Listbox` and `ttk.Button` provides much-needed visual hover feedback
missing in native Tkinter. **Action:** Always insert a placeholder item with gray text when
populating an empty Tkinter `Listbox`. Guard all corresponding event handlers to skip over this
placeholder text by checking its color. Also apply `cursor='hand2'` via ttk styles or explicitly to
improve interactive UI cues.
