## 2026-05-04 - Path Traversal Vulnerability in Template Configuration

**Vulnerability:** Path traversal vulnerability allowed reading arbitrary files by specifying paths
like `../../etc/passwd` in `docx_template` and `required_files` inside `config.yaml`. The
`template_id` in `TemplateManager.create_project` was also vulnerable to path traversal.

**Learning:** When reading files specified in YAML configurations or accepting directory names as
input (like `template_id`), user inputs must be validated to prevent traversing outside the intended
directories (`..` or absolute paths).

**Prevention:** Always validate that paths from configurations do not contain `..` and are not
absolute paths before using them in file operations. Ensure that directory IDs do not contain path
separators (`/` or `\`).

## 2024-06-02 - Fix Path Traversal in API

**Vulnerability:** The API endpoints `/workspaces/create` and `/workspaces/compile` allowed
directory traversal by directly concatenating user input (`req.name`, `req.workspace_name`) with the
base directory without verification. **Learning:** `Path.resolve()` combined with
`Path.is_relative_to()` is a clean and robust way to verify that an untrusted sub-path resolves
strictly within an expected base directory in Python. Wait, I should also remember to never commit
dummy exploit files. **Prevention:** Always validate and normalize external path inputs against the
expected base directory boundaries before using them in file operations.

## 2026-06-16 - Path Traversal Vulnerability in API Compile Output Paths

**Vulnerability:** The `/workspaces/compile` endpoint in the API accepted `md_out`, `docx_out`, and
`cache_dir` as optional strings. It directly created absolute paths from these inputs without
validating them against the workspace bounds, enabling arbitrary file write/overwrite capabilities
(path traversal) on the host machine. **Learning:** Even when API inputs represent target output
files or temporary cache directories, they must be treated as untrusted and potentially malicious if
they allow overriding predefined server paths. **Prevention:** Always validate all user-supplied
paths using a secure resolution function (e.g., `_secure_resolve`) that ensures the fully resolved
path remains relative to the intended base directory.
