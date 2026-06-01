## 2026-06-01 - Pre-compiled Regexes in Hot Loops

**Learning:** Using inline `re.search(r'pattern', text)` inside a heavily executed parsing function
(like word capitalisation) has significant overhead due to regex cache lookups and compilation.
**Action:** Pre-compile regular expressions using `re.compile()` as class attributes when they are
evaluated repeatedly in text processing loops.
