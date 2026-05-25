## 2025-05-25 - Prevent O(N) allocation bottleneck in UI events

**Learning:** Using unbounded string operations (like `replace` and `split` on the whole text)
inside UI event handlers (e.g. keypress handlers) creates severe input latency for large documents.
Replacing full-document scans with bounded iterative search (e.g. `str.find('\n', start)`) prevents
O(N) memory allocation and processing overhead per keystroke. **Action:** When analyzing string
contents up to a specific index or line, avoid full-document string replacements or splits. Use
iterative substring searching combined with boundary limits.
