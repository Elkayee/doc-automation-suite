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

## 2024-10-24 - Optimize Python Line Counting

**Learning:** Counting lines of large strings by evaluating `len(text.splitlines())` causes O(N)
memory allocation and overhead from splitting the string into a list. Using
`text.count(' ') + (1 if text and not text.endswith(' ') else 0)` is significantly faster (10x+ on
large texts) and has zero additional memory overhead.

**Action:** Use `.count(' ')` combined with the edge case check for fast, memory-efficient line
counting.
