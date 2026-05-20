## 2024-05-24 - [Optimize fenced block check with bounded split]

**Learning:** When parsing text up to a specific line, unbounded `text.replace(...).split('\n')`
allocates a full array for the entire string, which causes significant memory and execution overhead
for large documents. Fast-path substring checks (`if marker not in text: return False`) eliminate
O(N) allocation entirely when the marker is absent. **Action:** Always wrap `str.replace` and
`str.split` operations on large texts in fast-path checks when possible. Use `maxsplit` to limit
splitting allocations and parse safely when iterating linearly.
