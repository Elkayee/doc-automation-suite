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

## 2025-06-06 - Path Traversal in File Output Endpoints

**Vulnerability:** The `/workspaces/compile` endpoint in `src/api.py` allowed path traversal via
`md_out`, `docx_out`, and `cache_dir` parameters. While `workspace_name` was validated using
`_secure_resolve`, the output paths were directly cast to `Path()` and used to write files, allowing
attackers to overwrite arbitrary files on the system (e.g. `../../../../tmp/pwned.md`).
**Learning:** Security controls like `_secure_resolve` must be applied symmetrically to all file
path inputs. Only protecting the input workspace directory while leaving the output destination
paths unprotected bypasses the defense-in-depth strategy. **Prevention:** Always validate all path
inputs provided by the user using a secure resolution function before utilizing them in file system
operations. Output paths should either be strictly relative to a safe base directory or forbidden
from being passed explicitly if not necessary.
