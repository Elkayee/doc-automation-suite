## 2024-05-24 - Unbounded string splitting in editor keystroke handlers

**Learning:** In Tkinter UI workflows, text area keystroke handlers often evaluate application logic
(like code fence boundary checks via `is_line_inside_fenced_block`) on the entire text buffer for
every keystroke. Applying `.split('\n')` creates severe memory allocation overhead proportional to
the total document size, even when parsing only up to the cursor position. **Action:** When
validating formatting or checking markers up to a specific line index, always use bounded splitting
(e.g. `text.split('\n', safe_line_number)`). Combine this with an O(1) substring fast-path check
(`if marker not in text`) to skip parsing entirely whenever possible.
