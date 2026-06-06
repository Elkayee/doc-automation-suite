## 2024-05-28 - Bounded Split for Large Documents

**Learning:** Checking the line state of a large text document by fully splitting the entire string
(`.split('\n')`) on every keystroke causes O(N) memory allocations, resulting in noticeable UI lag
for early lines in large files.

**Action:** Use `.split('\n', limit)` to bound the parsing strictly to the required prefix of the
document. This avoids allocating the rest of the string into thousands of smaller strings.

## 2024-06-03 - Optimize Python Whitespace Normalization

**Learning:** Using `str.split()` combined with `' '.join()` is significantly faster (~5.5x) than
`re.sub(r'\s+', ' ', text).strip()` for collapsing whitespace in Python, bypassing regex compilation
and engine overhead. **Action:** Prefer `' '.join(text.split())` over `re.sub` for normalizing
whitespace when exact space/tab/newline distinctions aren't required.

## 2024-06-06 - O(N²) String Slicing in Regex Processing

**Learning:** Repeatedly slicing the entire prefix of a large document (`text[:start]`) inside a
loop (like `re.finditer`) causes O(N) string allocations per iteration, resulting in O(N²) execution
time. In this application, this caused `normalize_report_capitalization` to take over 60 seconds on
large Markdown documents.

**Action:** When validating local text patterns (e.g., matching the end of a prefix with regex using
`$` or `endswith`), bound the slice to a fixed maximum length (e.g.,
`text[max(0, start - 200):start]`) to cap the memory allocation strictly at O(1) per iteration,
effectively dropping the overall time complexity to O(N). Additionally, always pre-compile inline
regular expressions to class-level constants to avoid compilation overhead during tight loops.
