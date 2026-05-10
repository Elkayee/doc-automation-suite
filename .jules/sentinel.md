## 2024-05-10 - Config File Path Traversal Protection
**Vulnerability:** Configuration files (`config.yaml`) defining `required_files` and `docx_template` lacked path sanitization, potentially allowing path traversal attacks via `..`.
**Learning:** Even internal configuration objects can be attack vectors if they process user-provided paths without validation, especially in document processing pipelines where configurations are loaded dynamically.
**Prevention:** Always implement an `is_safe_path` check for user-defined file paths in configurations, explicitly blocking parent directory references (`..`), and gracefully handling or validating valid absolute paths as per the application's design, rather than silently rejecting them.
