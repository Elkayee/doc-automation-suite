## 2024-05-21 - Tkinter empty states and cursors
**Learning:** Tkinter Listboxes lack native empty states. Inserting a placeholder and changing its foreground color provides visual feedback, but requires explicit guards in all event handlers to ignore items with that color. ttk.Button requires setting the cursor via `root.option_add` rather than widget properties.
**Action:** Always implement empty states for Listboxes using placeholder text and color coding, and guard event handlers against acting on the placeholder.
