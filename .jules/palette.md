## 2024-05-17 - Accessible Empty States in Tkinter Listboxes

**Learning:** Tkinter listboxes don't have a native empty state feature. Using an inserted string
with `foreground='gray'` works visually, but event handlers (like double-click or selection) need to
explicitly check `listbox.itemcget(idx, 'foreground') == 'gray'` and return early to prevent the
placeholder from being processed as a valid item. **Action:** Always implement empty states for
listboxes when `listbox.size() == 0`, distinguish them visually with a gray foreground, and guard
all related event handlers with an explicit check on the item's foreground color to avoid invalid
actions.
