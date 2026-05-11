## 2025-02-24 - [Path Traversal in Configuration Loading]

**Vulnerability:** The application was loading `docx_template`, `required_files`, and
`chapter_order` strings directly from `config.yaml` without validating for relative path indicators
(`..`). This allowed potential path traversal attacks to access or write outside the intended
workspace directories. **Learning:** File paths supplied via user-controlled configuration files
(like YAML templates) must be treated as untrusted input. Blindly parsing and relying on relative
path resolutions using `Path()` can lead to directory traversal. **Prevention:** Implement explicit
structural checks (e.g., `'..' in Path(val).parts`) during configuration hydration to reject unsafe
paths. Fail explicitly with a `ValueError` instead of silently cleaning or ignoring the payload.
