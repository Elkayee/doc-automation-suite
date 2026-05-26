## 2026-05-26 - Avoid O(N) scanning loops when iterating lines

**Learning:** When trying to avoid full-string array allocation (e.g. from `.replace().split()`),
replacing it with a manual `while` loop using `.find('\n')` and `.find('\r')` introduces a
catastrophic algorithmic regression: `str.find()` performs an $O(N)$ scan to the end of the document
on _every_ line if the target character isn't present, turning a millisecond operation into
$O(L \times N)$ execution. **Action:** To iteratively and lazily parse lines from a large string
without full memory allocation, always rely on Python's optimized `io.StringIO(text)`. It handles
universal newlines efficiently under the hood via C extensions, preventing both array allocation
bloat and quadratic scanning times.
