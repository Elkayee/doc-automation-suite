## 2024-05-16 - Add visual feedback for buttons in desktop app
**Learning:** Tkinter buttons (`ttk.Button` and `tk.Listbox`) do not have hover states that change the cursor to a pointer by default, making them feel unresponsive compared to web apps.
**Action:** Always add `cursor='hand2'` when initializing interactive elements in Tkinter apps to provide immediate visual feedback.
