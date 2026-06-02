## 2024-05-28 - Bounded Split for Large Documents

**Learning:** Checking the line state of a large text document by fully splitting the entire string
(`.split('\n')`) on every keystroke causes O(N) memory allocations, resulting in noticeable UI lag
for early lines in large files.

**Action:** Use `.split('\n', limit)` to bound the parsing strictly to the required prefix of the
document. This avoids allocating the rest of the string into thousands of smaller strings.

## 2024-05-28 - Lazy Regex Parsing and Functional Equivalence

**Learning:** When refactoring bounded text operations (e.g., `text.split('\n', limit)`) into lazily
evaluated iterators (e.g., `re.finditer`), explicitly verify that early-exit conditions (such as
checking target line numbers) are correctly preserved across all inner loop branches, including
`continue` paths, to prevent unintended functional changes (e.g., flipping a boolean flag but
returning before standard evaluation). **Action:** Always write a localized regression test that
compares the exact output of the old vs. new implementation for all expected branches before
integrating lazy evaluations.
