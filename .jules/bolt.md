## 2024-05-22 - Optimize unbounded full-buffer splitting in keystroke handlers

**Learning:** Unbounded splitting (`text.split('\n')`) on large text buffers inside Tkinter
keystroke event handlers (like return key handlers) causes severe memory allocation overhead and
input lag per keystroke. **Action:** Use bounded splitting (`maxsplit` parameter in `split()`)
combined with O(1) substring checks (`'...' in text`) to limit string parsing to only the required
line boundaries.
