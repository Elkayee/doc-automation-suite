## 2025-05-18 - Pre-compile Regex Patterns
**Learning:** Compiling regex dynamically within a frequently executed method significantly degrades performance.
**Action:** Move regular expression compilation (`re.compile`) from within methods to the module or class level to avoid redundant recompilation overhead, particularly for patterns that are used often or within large text processing functions.