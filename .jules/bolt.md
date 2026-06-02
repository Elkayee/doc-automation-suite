## 2024-05-28 - Bounded Split for Large Documents

**Learning:** Checking the line state of a large text document by fully splitting the entire string
(`.split('\n')`) on every keystroke causes O(N) memory allocations, resulting in noticeable UI lag
for early lines in large files.

**Action:** Use `.split('\n', limit)` to bound the parsing strictly to the required prefix of the
document. This avoids allocating the rest of the string into thousands of smaller strings.
## 2024-05-29 - O(N) Regex String Allocations in Bounded Splits

**Learning:** When attempting to limit memory allocations via bounded string splits (e.g., `.split('\n', limit)`), calling `.replace()` on the source string beforehand completely negates the optimization. `.replace()` evaluates on the entire string first, forcing a massive, O(N) allocation before the bounded split even occurs. For a 10 million line document, this means allocating ~20MB just to check the first 5 lines.

**Action:** Replace `.replace().split(limit)` on unbounded text with a lazily evaluated regular expression iterator (`re.finditer()`). This approach avoids full-string allocations entirely by iterating via indices and can break early, resulting in essentially 0MB memory overhead for prefix operations.
