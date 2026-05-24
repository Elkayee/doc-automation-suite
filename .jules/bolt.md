## 2024-05-24 - Bounded splitting for line-based searches

**Learning:** Using unbounded `.split('\n')` on large buffers (especially in keystroke handlers like
return key events) causes massive CPU and memory allocation overhead. Bounded limits like
`.split('\n', limit)` drastically speed this up.

**Action:** Avoid `.replace('\r\n', '\n').replace('\r', '\n').split('\n')` and instead use
`.split('\n', limit)` where you only need parsing up to `limit`. Python's `.split()` supports an
efficient `maxsplit` argument that skips copying the remainder of the string into elements.
