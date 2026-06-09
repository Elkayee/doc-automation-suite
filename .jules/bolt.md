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

## 2024-06-10 - File Streaming vs. String regex iterators

**Learning:** Replacing `str.splitlines()` on an entire file contents string with a regex iterator
like `re.finditer` is a severe anti-optimization due to regex overhead. For memory-efficient, lazy
line iteration of large files, stream the file directly (e.g.,
`with open(filepath) as f: for line in f:`) instead of reading the whole text into memory.

**Action:** Prefer `with open() as f: for line in f:` when reading lines lazily from a file, rather
than loading the text and iterating with regex.
