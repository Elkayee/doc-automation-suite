## 2024-05-21 - Predictable Temporary File Paths

**Vulnerability:** Predictable, hardcoded temporary file paths (e.g., `/tmp/libreoffice_profile` or
`/tmp/lo_socket_shim.so`) were used for application profiles and sockets, exposing the application
to temporary file attacks like symlink manipulation. **Learning:** Hardcoded paths in `/tmp` are
globally writable, making them predictable and vulnerable to hijacking. **Prevention:** Use
`tempfile.TemporaryDirectory()` and assign the instance to a module-level global variable to
generate randomized paths securely and prevent premature garbage collection.
