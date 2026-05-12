## 2025-03-05 - Secure Temporary Directory Creation

**Vulnerability:** Predictable temporary directory paths (e.g., `/tmp/libreoffice_docx_profile`)
were hardcoded for LibreOffice user profiles. This allowed potential pre-creation attacks, enabling
malicious actors to gain access to files created in the temp directory, elevate privileges, or
perform denial-of-service by locking the directory path. **Learning:** Hardcoded paths in
world-writable directories (`/tmp/`) create insecure and predictable attack surfaces.
**Prevention:** Use standard library functions like `tempfile.mkdtemp` to securely and dynamically
create randomized temporary directories, and use `atexit` hooks to manage process-lifetime cleanup.
