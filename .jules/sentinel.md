## 2025-05-19 - Insecure Predictable Temporary File Usage for LD_PRELOAD Shim

**Vulnerability:** The application compiled and wrote a shared object (`lo_socket_shim.so`) and C
source file (`lo_socket_shim.c`) into hardcoded, predictable temporary file paths
(`Path(tempfile.gettempdir()) / '...'`). This exposes the system to symlink attacks, allowing an
attacker to overwrite arbitrary files when the application is run with higher privileges, or
facilitating arbitrary code execution by replacing the `lo_socket_shim.so` payload loaded via
`LD_PRELOAD`. **Learning:** Hardcoded filenames within global temporary directories (like `/tmp`)
are vulnerable to race conditions (Time-of-Check to Time-of-Use) and symlink manipulation. The
attack surface is amplified because the generated file is directly executed via the `LD_PRELOAD`
environment variable. **Prevention:** Always use securely generated randomized paths from the
`tempfile` module (e.g., `tempfile.TemporaryDirectory()`, `tempfile.mkstemp()`, or
`tempfile.NamedTemporaryFile()`). For module-level temporary paths, storing the instance of
`tempfile.TemporaryDirectory()` in a global variable ensures it isn't prematurely garbage-collected
while the process is running.
