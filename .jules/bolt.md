## 2024-05-20 - Pre-compile regular expressions at the class/module level
**Learning:** Compiling regular expressions repeatedly inside loops or frequently called validation functions creates significant overhead and slows down validation significantly, especially in CPU-bound tasks like document parsing.
**Action:** Always pre-compile constant regular expressions at the module or class level (e.g., `PATTERN = re.compile(...)`) so they are compiled exactly once.
