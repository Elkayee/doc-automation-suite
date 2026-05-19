## 2025-02-12 - Pre-compile Regular Expressions

**Learning:** In frequently called methods like document validators, compiling regular expressions
inside the method (e.g., `re.compile()`) adds redundant compilation overhead and regex cache
lookups. **Action:** Pre-compile constant regular expressions at the module or class level to avoid
this overhead, especially in hot paths.
