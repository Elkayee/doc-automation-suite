## 2024-05-25 - Prevent Memory Overhead with Iterative Substring Parsing

**Learning:** Using unbounded `.split('\n')` or full-string `.replace()` on large text buffers (like
markdown documents in keystroke event handlers) scans and allocates massive strings/arrays, causing
severe memory overhead and O(N) performance penalties. **Action:** When parsing up to a specific
line limit in large text, use a fast-path substring check (e.g., `if '\`\`\`' not in
text`) and an iterative boundary search (using `str.find('\n', start)`) to prevent unnecessary
allocations and early-return as soon as the target line is evaluated.
