## 2024-05-28 - Bounded Split for Large Documents

**Learning:** Checking the line state of a large text document by fully splitting the entire string
(`.split('\n')`) on every keystroke causes O(N) memory allocations, resulting in noticeable UI lag
for early lines in large files.

**Action:** Use `.split('\n', limit)` to bound the parsing strictly to the required prefix of the
document. This avoids allocating the rest of the string into thousands of smaller strings.

## 2024-06-03 - [Optimize whitespace normalization]
**Learning:** Using `re.sub(r'\s+', ' ', text).strip()` to normalize whitespace is significantly slower (~5.6x) than using built-in string methods like `' '.join(text.split())`. This is because `.split()` inherently handles contiguous whitespace and strips leading/trailing spaces without the regex engine overhead.
**Action:** Prefer `' '.join(text.split())` over regex substitution when the goal is simply to collapse all whitespace into single spaces and strip surrounding whitespace.
