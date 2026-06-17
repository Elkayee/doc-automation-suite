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

## 2024-06-13 - Safe Zero-Allocation Regex Slicing

**Learning:** Bounding the length of a string slice (`text[max(0, start-200):start]`) prevents
O(N^2) memory leaks but causes destructive context loss if whitespace exceeds the bounds.
Furthermore, Python's `re.search` with `$` and `\Z` anchors ignores the `endpos` parameter, making
bounded regex suffix checks fail. **Action:** Achieve zero-allocation O(1) performance safely by
manually walking backwards over unbounded whitespace arrays to locate the true end of the string,
and only extracting a small trailing context window slice once the exact alphanumeric text boundary
is located.
