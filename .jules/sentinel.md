## 2024-05-24 - Path Traversal Vulnerability in Template Configuration

**Vulnerability:** The `config.yaml` parsing (`TemplateConfig.load`) blindly accepted
user-controlled strings for `required_files` and `chapter_order`. These properties are used as
filenames and concatenated with directory paths without proper sanitization, allowing path traversal
attacks via `..`, `/`, and `\`. **Learning:** File references originating from configuration files
must be treated as untrusted inputs, especially when they will be used dynamically for file system
operations. **Prevention:** Always implement strict sanitization logic for filename arrays loaded
from configuration. Drop or sanitize elements containing `..` or path separator characters (`/`,
`\`) before they merge with base directories.
