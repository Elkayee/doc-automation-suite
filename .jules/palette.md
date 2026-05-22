## 2024-05-23 - Visual Feedback and Empty States in Tkinter Desktop UIs

**Learning:** In desktop environments like Tkinter, default buttons (`ttk.Button`) and interactive
lists (`tk.Listbox`) lack visual hover states (like the hand cursor common on the web), making it
harder for users to identify clickable elements. Additionally, empty lists without placeholders can
confuse users about whether the app is broken or just devoid of data. **Action:** Always apply
`cursor='hand2'` globally to `*TButton*` via `root.option_add` and directly to `tk.Listbox`
instances. For empty list states, insert a styled placeholder item (e.g., `foreground='gray'`) and
add guard clauses in event handlers to ignore selections of this placeholder.
