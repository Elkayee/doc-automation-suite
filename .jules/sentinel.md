## 2025-05-20 - [Fix predictable temporary file paths]

**Vulnerability:** Application generates a predictably named temporary file in the global temp
directory `Path(tempfile.gettempdir()) / 'lo_socket_shim.so'` or
`Path(tempfile.gettempdir()) / 'lo_socket_shim.c'`. **Learning:** These types of hardcoded paths are
highly vulnerable to Symlink manipulation and race conditions where an attacker could pre-create the
file to gain code execution or leak data. **Prevention:** Use securely generated randomized paths
provided by functions like `tempfile.TemporaryDirectory()`. When generating them at the module
level, ensure the generated object's reference is kept in a global variable so that the directory
isn't prematurely garbage collected.
