## 2024-10-25 - Avoid unbounded split in keystroke UI handlers

**Learning:** Unbounded string splitting (`text.split('\n')`) on large text buffers inside
synchronous Tkinter UI keystroke event handlers (like return key handling) causes severe memory
allocation overhead and blocks the main thread. **Action:** Replace unbounded `.split('\n')` with
iterative `str.find('\n')` (or bounded `maxsplit`) combined with early returns, allowing the loop to
stop exactly when the required line is reached without parsing the entire remainder of the text.
