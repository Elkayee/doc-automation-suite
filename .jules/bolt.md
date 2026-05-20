## 2026-05-20 - [Pre-compile Constant Regular Expressions]

**Learning:** Compiling regex patterns (e.g., UUID validation, template tag parsing) inside methods
like `validate_uuid_ids` or `_remove_template_tags_from_text_nodes` introduces redundant compilation
overhead, especially in frequently called paths like document validators processing multiple
files/nodes. **Action:** Pre-compile constant regular expressions at the module level (e.g.,
`PATTERN = re.compile(...)`) to avoid redundant compilation overhead and minimize regex cache
lookups.
