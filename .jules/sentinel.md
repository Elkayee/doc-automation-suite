## 2026-05-08 - [Path Traversal in Configuration Parsing]

**Vulnerability:** The configuration parsing in `TemplateConfig.load` blindly accepted user-provided
file references (`required_files`, `docx_template`, `chapter_order`) without validation. This
allowed an attacker to specify arbitrary files on the file system by using path traversal sequences
like `..`, `/` or `\`. **Learning:** File references from configuration files (like `config.yaml`)
should be rigorously sanitized against path traversal by explicitly blocking parent directory
references (`..`) and path separators (`/`, `\`) before combining them with base directories.
**Prevention:** Implement an `is_safe_path` function that checks for and blocks traversal sequences
and separators. Drop invalid entries or use a safe default instead.
