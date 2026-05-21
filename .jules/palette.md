## 2024-05-21 - Tkinter Empty States and Interactive Cursors
**Learning:** Tkinter lacks native empty states for Listboxes and default hover cursors for ttk.Buttons. Users can easily feel lost when lists are empty, and lack of visual feedback on buttons reduces perceived interactivity.
**Action:** Always inject a distinct (e.g., grayed out) placeholder item in empty Listboxes (and update event handlers to ignore it) and globally apply `cursor='hand2'` to buttons via `root.option_add`.
