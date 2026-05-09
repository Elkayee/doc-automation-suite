
## 2024-05-09 - Fast-path check and bounded split for large strings
**Learning:** Python's string `.split()` creates unbounded full arrays in memory even when only a subset is accessed. Bounded splitting via the `maxsplit` parameter paired with an initial `in` fast-path check provides a safe optimization with order of magnitude speedup for text-parsing functions.
**Action:** When extracting data up to a specific line index in string buffers, use a guard check (e.g., `if 'marker' not in text: return`) and `maxsplit` bounded `.split()` rather than unbounded or manual replacement techniques.
