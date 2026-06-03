## 2024-05-28 - Bounded Split for Large Documents

**Learning:** Checking the line state of a large text document by fully splitting the entire string
(`.split('\n')`) on every keystroke causes O(N) memory allocations, resulting in noticeable UI lag
for early lines in large files.

**Action:** Use `.split('\n', limit)` to bound the parsing strictly to the required prefix of the
document. This avoids allocating the rest of the string into thousands of smaller strings.
## 2024-05-28 - Regex Overhead in Whitespace Normalization
**Learning:** Using `re.sub(r'\s+', ' ', text).strip()` to normalize multiple whitespace characters into single spaces carries noticeable regex engine overhead when executed heavily in loops.
**Action:** Replace it with the built-in string operation `' '.join(text.split())`, which achieves the exact same result (stripping ends and collapsing internal whitespace) much faster as it bypasses regular expressions entirely.
