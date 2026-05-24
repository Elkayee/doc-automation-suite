## 2024-05-24 - Fix Path Traversal in Config Loader

**Vulnerability:** The configuration parsing (`TemplateConfig.load`) blindly accepts any string for
`required_files` and `docx_template`, which could lead to path traversal vulnerabilities if absolute
paths or parent references (`..`) are provided, especially when these configurations are combined
with a base directory in Python's `pathlib`. **Learning:** `pathlib` combined with an absolute path
silently discards the base directory (e.g. `base_dir / '/etc/passwd'` results in `'/etc/passwd'`),
which creates severe arbitrary file access vulnerabilities in Python. This must be guarded
explicitly across platforms. **Prevention:** Implement path sanitization validation at the
configuration loading level to selectively block absolute paths and `..` combinations for fields
expected to be file paths (`required_files` and `docx_template`).
