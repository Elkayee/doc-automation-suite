## 2024-05-24 - Added empty state to Tkinter Listbox

**Learning:** Empty states provide helpful guidance when no data is present, improving UX. In
Tkinter Listboxes, we can implement this by inserting a placeholder string and setting its color to
'gray' (e.g., `listbox.itemconfig(0, foreground='gray')`), then explicitly blocking interactions
with gray items in event handlers. **Action:** Apply this pattern to any empty listbox in the app to
improve onboarding and clarify empty states, and add `cursor='hand2'` to interactive widgets for
better visual feedback.
