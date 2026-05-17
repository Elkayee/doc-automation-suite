## 2024-05-18 - Prevent Predictable Temporary File Attacks
**Vulnerability:** A predictable hardcoded temporary directory (`/tmp/libreoffice_docx_profile`) was used for the LibreOffice profile, making the application vulnerable to predictable temporary file attacks such as TOCTOU (Time-Of-Check to Time-Of-Use) and symlink manipulation.
**Learning:** Hardcoded temporary paths expose applications to security risks on shared systems where attackers can pre-create symlinks or modify the temporary directory before the application uses it.
**Prevention:** Use Python's `tempfile.TemporaryDirectory()` to securely and dynamically generate randomized temporary directories. Assign the instance to a module-level variable to prevent premature garbage collection.
