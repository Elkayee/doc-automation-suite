## 2024-05-23 - Optimize string splitting in UI event handlers
**Learning:** In Tkinter applications, using unbounded `.split('\n')` on large text buffers inside keystroke event handlers (like return key handlers checking for fenced blocks) causes severe memory allocation overhead and lags the UI per keystroke.
**Action:** Use bounded splitting (`split('\n', maxsplit)`) combined with O(1) fast-path substring checks (`if '\r' in text` before `replace()`) to skip unnecessary processing. Also `lstrip` is faster than `strip` when just checking prefixes.
