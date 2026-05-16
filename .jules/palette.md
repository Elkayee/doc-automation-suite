## 2024-05-16 - Add empty state pattern to Tkinter Listbox

**Learning:** Tkinter Listboxes lack native empty state support. Adding a placeholder string is
visually effective, but creates a subtle accessibility and functional bug if users can select the
placeholder text. We must explicitly intercept selection events (e.g., `<Double-1>` or dedicated
buttons) and verify the item state (e.g., by checking for `itemcget(idx, 'foreground') == 'gray'`)
to discard the event and avoid downstream logic errors or exceptions. **Action:** Always complement
Listbox placeholder strings with visually distinct styling (`foreground='gray'`) and defensively
wrap ALL interaction handlers bound to that Listbox to ignore selections with that styling.
