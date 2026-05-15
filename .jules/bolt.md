## 2024-05-15 - Unbounded Line Splits Cause O(N^2) Latency

**Learning:** When scanning for markers (like code fences ` ``` `) or searching text line-by-line using a naive full-string split `text.split('\n')`, it creates severe performance overhead by unnecessarily allocating large arrays for huge text blocks (e.g. 7000+ lines). Unbounded string formatting combined with split limits is especially harmful in deeply nested calls or UI functions that query lines.
**Action:** Guard string operations (`replace`) with fast-path string inclusion checks (`if '\r' in text`) and bound array creation limits during split operations (`text.split('\n', limit)`). Always add top-level checks (`if '```' not in text`) to skip processing entirely when no markers are present.
