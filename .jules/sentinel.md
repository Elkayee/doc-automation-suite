## 2025-02-14 - Predictable Temporary File Vulnerability

**Vulnerability:** Found hardcoded and predictable temporary file paths
(`/tmp/libreoffice_docx_profile` and paths derived from `tempfile.gettempdir()`) for LibreOffice
profiles and dynamic shared objects (`lo_socket_shim.so`/`.c`). **Learning:** Using predictable
paths in world-writable directories like `/tmp` exposes the application to TOCTOU (Time-of-Check to
Time-of-Use) race conditions, symlink manipulation, and unauthorized file access/overwrite attacks.
**Prevention:** Always use `tempfile.TemporaryDirectory()` or `tempfile.mkstemp()` to securely
generate randomized temporary paths. When required to persist a temporary directory for the duration
of a script without being garbage collected, assign the `TemporaryDirectory` instance to a
module-level global variable.
