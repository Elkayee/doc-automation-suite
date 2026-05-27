## 2024-05-27 - Bounded Splits for Line Parsing

**Learning:** In large string parsing, `split('\n')` on the entire document can cause massive,
unnecessary memory allocation and block the main thread. **Action:** When searching for a property
of a specific line number, use `split('\n', line_number)` to limit splits and process only the
necessary chunks. Remember to use `break` when iterating the resulting chunks.
