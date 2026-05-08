## $(date +%Y-%m-%d) - Optimize unbounded line splitting with maxsplit

**Learning:** When parsing text up to a specific line number, doing a full string replace and
unbounded split `text.replace('\r\n', '\n').split('\n')` forces Python to traverse and allocate an
array for the entire string. This scales poorly $O(N)$ with large text files. Trying to implement a
custom bounds loop with `find('\n')` is also surprisingly slower due to pure-Python overhead vs C
implementations.

**Action:** Add an upfront fast path substring check (`if '```' not in text: return False`), and use
the native `maxsplit` parameter (`text.split('\n', max_lines)`) instead of custom looping. This
bounds the split, saving memory and processing overhead while keeping the parsing code clean.
