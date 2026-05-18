## 2024-05-18 - Fast Path and Bounded Splits for Fenced Block Detection

**Learning:** In Tkinter UI applications and general parsing logic, using unbounded
`.replace().split('\n')` on large strings in frequently executed code paths (like keystroke
handlers) introduces severe O(N) allocation overhead per call, even when the search condition is
rare. **Action:** Always prioritize fast-path O(1) checks (e.g.
`if '```' not in text: return False`) and use bounded splits (e.g.
`text.split('\n', safe_line_number)`) to limit computation to the minimally required chunk.
