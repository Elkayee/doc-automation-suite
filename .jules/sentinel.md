## 2024-05-18 - Predictable temporary file path vulnerability in soffice socket shim
**Vulnerability:** The application used a predictable, hardcoded temporary file path (`lo_socket_shim.so` and `lo_socket_shim.c`) via `tempfile.gettempdir()` for the LibreOffice socket shim, which exposes it to symlink manipulation and TOCTOU vulnerabilities.
**Learning:** Hardcoded names in a globally writable directory (like `/tmp`) can allow attackers to hijack or intercept files by creating symlinks before the application writes them.
**Prevention:** Use `tempfile.TemporaryDirectory()` at the module level (assigned to a global variable to prevent premature garbage collection) to securely generate a random, unique directory that the application can safely write its files to.
