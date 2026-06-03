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

## 2026-05-05 - Path Traversal Vulnerability in API Workspaces Configuration

**Vulnerability:** Path traversal vulnerability allowed reading or writing arbitrary files by
specifying paths like `../` or `/absolute/path` in `workspace_name`, `docx_out`, `md_out`,
`cache_dir` for `CompileRequest` and `name`, `template` for `CreateRequest` in the API endpoints.
**Learning:** Even when inputs are validated downstream (like `template_id` in `TemplateManager`),
API endpoints themselves often construct new paths or pass parameters directly to internal services,
requiring input validation at the boundary layer. Output paths provided by clients must always be
strictly validated to prevent arbitrary file writes. **Prevention:** Use Pydantic's
`field_validator` in FastAPI request models to explicitly reject path parameters containing path
separators (`/`, `\`), relative traversal segments (`..`), or absolute paths (`is_absolute()`)
before the data reaches application logic.
