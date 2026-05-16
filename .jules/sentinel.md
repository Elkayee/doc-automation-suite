## 2024-05-24 - Configuration File Path Traversal Vulnerability

**Vulnerability:** `src/core/config.py` was blindly loading configuration files (`config.yaml`)
without validating user-provided file paths, such as `required_files` and `docx_template`, which
exposed the application to path traversal vulnerabilities (e.g., `../secret.md`). **Learning:**
Naive file path handling in configurations read from user environments poses severe security risks,
as untrusted entries may use `..` sequences to bypass directory restrictions. Validating data
structures requires recursive traversal for deeply nested structures (like arrays of strings or
nested dicts in YAML). **Prevention:** Implement a recursive validation function
(`_validate_no_path_traversal`) in the configuration loader that recursively checks properties
against traversal vectors (`..` within `.split('/')` arrays, after normalizing backslashes), and
strictly throws validation errors instead of silently ignoring invalid paths.
