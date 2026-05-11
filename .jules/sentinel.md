## 2026-05-11 - Prevent Path Traversal in Configuration Loading

**Vulnerability:** The application was loading `docx_template`, `required_files`, and
`chapter_order` from `config.yaml` without validating the paths, potentially allowing path traversal
attacks via `../` references to read arbitrary files. **Learning:** File references within
user-supplied configurations (e.g. YAML) must be sanitized. Relying entirely on application logic to
handle invalid or dangerous paths later is unsafe. **Prevention:** Block `..` in all configuration
paths upon load and raise an explicit `ValueError` instead of silently ignoring or fixing them.
Accommodate valid absolute paths if necessary.
