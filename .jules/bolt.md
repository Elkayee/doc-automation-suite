## 2024-05-24 - Pre-compile regex in class variables
**Learning:** Compiling regular expressions repeatedly inside loops or frequently called validation methods causes unnecessary overhead and slows down text processing.
**Action:** Always pre-compile constant regular expressions at the module or class level (e.g., `PATTERN = re.compile(r'...')`) instead of inside methods or loops to avoid redundant compilation overhead, especially in frequently called paths like document validators.
