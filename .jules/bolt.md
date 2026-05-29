## 2026-05-29 - Optimize line parsing with bounded split

**Learning:** When parsing large text strings to find specific lines, full-string memory allocation
(e.g., `.replace().split('\n')`) can be a significant performance bottleneck. While `io.StringIO`
offers lazy iteration, bounded splits `.split('\n', limit)` are a safer way to reduce memory
allocation without breaking bug-for-bug trailing newline compatibility, compared to manual search
loops. **Action:** When a method only needs to process lines up to a specific index `N`, use
`text.split('\n', N)` to limit array allocation while preserving exact splitting semantics.
