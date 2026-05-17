## 2024-05-24 - Bounded splitting and Fast Path String optimization

**Learning:** In text processing applications with Tkinter keystroke handlers, unbounded
`.split('\n')` on large strings causes massive memory overhead and computational cost. Additionally,
allocating the full string arrays with `splitlines()` can also be bypassed using
`str.split('\n', limit)` to allocate only up to the needed line length while using an early fast
path substring check (`if 'marker' not in text: return False`) to bypass parsing for the vast
majority of operations. **Action:** When repeatedly scanning large documents for line-specific
markers (like code fences), use bounded splitting (`text.split('\n', maxsplit)`) combined with an
`in` fast path string check and avoid full string copies (e.g. `text.replace()`) unless explicitly
required by the string characters being present.
