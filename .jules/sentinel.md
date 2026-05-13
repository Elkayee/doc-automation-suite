## 2025-05-03 - Config Path Traversal Prevention
**Vulnerability:** Path traversal in `TemplateConfig` paths (`docx_template`, `required_files`, `chapter_order`). Allowed loading configuration files that could instruct the system to read or process sensitive files outside the intended project directory by using `..` in relative paths.
**Learning:** Configurations driven by user-provided yaml files can be exploited to read restricted files. Path properties should always be sanitized on initialization to block relative back-references.
**Prevention:** Implement validation on path-related properties inside `__post_init__` to explicitly reject any paths containing `..` in their parts, preventing directories escape.
