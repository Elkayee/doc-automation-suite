## 2024-05-24 - Config File Path Traversal

**Vulnerability:** Path traversal possible through config files (`docx_template`, `required_files`,
`chapter_order`). **Learning:** Parsing configurations with file references using `pathlib` combined
with absolute paths or `..` can lead to arbitrary file access and discard the base directory.
**Prevention:** Sanitize file paths explicitly by blocking parent directory references (`..`) and
absolute paths using `os.path.isabs` and platform-specific checks across platforms. Apply this
selectively only to fields intended to be file paths.
