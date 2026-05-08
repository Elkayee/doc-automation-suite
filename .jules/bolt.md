## 2025-05-08 - Optimized `is_line_inside_fenced_block`

**Learning:** `text.replace('\r\n', '\n').replace('\r', '\n').split('\n')` creates severe memory
allocations for large text files, and using `text.splitlines()` introduces edge cases with trailing
empty strings. A simple fast path `if marker not in text: return` combined with preserving the
original behavior offers the best mix of safety and speed. **Action:** Always consider an upfront
fast-path inclusion check (e.g., `in`) before parsing or splitting lines, and be cautious when
replacing native operations with `splitlines()` as it handles trailing newlines and unusual
whitespace characters differently than standard split logic. Add inline comments explaining
performance enhancements.
