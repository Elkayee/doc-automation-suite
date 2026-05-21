## 2024-05-21 - Secure Temporary Directory for LibreOffice Profile

**Vulnerability:** Predictable hardcoded temporary path (`/tmp/libreoffice_docx_profile`) used for
the LibreOffice profile directory, which could lead to symlink manipulation or TOCTOU race
conditions. **Learning:** Hardcoded predictable paths in shared temporary directories like `/tmp`
expose the application to local file manipulation attacks. **Prevention:** Use
`tempfile.TemporaryDirectory()` to securely generate randomized temporary paths and ensure they
persist for the required duration by storing the directory instance in a module-level variable.
