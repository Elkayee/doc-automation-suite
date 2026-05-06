## 2024-05-17 - Keyboard Accessibility in Tkinter Dialogs

**Learning:** Adding `.focus_set()` to key input fields (like project names) and supporting
`<Return>` and `<Escape>` keybindings for submission/cancellation vastly improves the UX of Tkinter
Toplevel dialogs by enabling smooth, mouse-free interactions. **Action:** When creating Tkinter
dialogs, always ensure primary inputs auto-focus and provide keyboard shortcuts for common actions.
