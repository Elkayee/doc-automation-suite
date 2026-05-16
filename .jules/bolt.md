## 2025-03-01 - Avoid unbounded string replacements and splits

**Learning:** Performance Anti-pattern: When parsing text up to a specific line, unbounded
`text.replace(...).split('\n')` allocates a full array for the entire string. Avoid manual iterative
`str.find('\n')` loops as they are slower in Python; instead, use a fast-path substring check
(`if marker not in text`) combined with bounded splitting using `maxsplit` (e.g.,
`text.split('\n', safe_line_number)`). **Action:** When a method needs to inspect text only up to a
certain line, use `maxsplit` on `.split()` and fast-path substring `in` checks to avoid unnecessary
allocation of memory.
