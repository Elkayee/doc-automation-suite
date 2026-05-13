## 2024-05-15 - [Predictable Temporary File Vulnerabilities]
**Vulnerability:** Found hardcoded temporary file paths (`/tmp/libreoffice_docx_profile`, `/tmp/lo_socket_shim.c`) which are prone to symlink manipulation and Time-of-Check Time-of-Use (TOCTOU) attacks in multi-user environments.
**Learning:** Hardcoding standard temporary paths creates a window for local attackers to pre-create files/directories as symlinks, potentially leading to arbitrary file overwrite or privilege escalation when the application interacts with those files.
**Prevention:** Always use secure, random path generation mechanisms like `tempfile.TemporaryDirectory` or `tempfile.NamedTemporaryFile` instead of statically predicting file locations in world-writable directories.
