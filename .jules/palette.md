## 2025-02-23 - Keyboard Accessibility in Tkinter UIs

**Learning:** Tkinter `Toplevel` dialogs and `Listbox` components lack built-in keyboard navigation
affordances (e.g., auto-focus, submission via Return key). **Action:** Explicitly call
`.focus_set()` on primary inputs upon dialog open, and bind the `<Return>` event to primary action
methods (remembering to accept `event=None` in the callback) to ensure a seamless, mouse-free user
experience.
