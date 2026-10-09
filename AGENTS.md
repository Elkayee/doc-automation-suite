# Project instructions

## Product and scope

This desktop tool authors Vietnamese academic and office reports. Preserve the Python/Tkinter app
and Markdown/YAML workspaces unless a redesign is approved. Read PLAN.md and TASK.md before
implementation; update both at each milestone with completed work, executed checks, and remaining
limitations.

For report upgrades, read the approved contract in
docs/superpowers/specs/2026-10-09-report-authoring-upgrade.md. The supporting research is
docs/research/2026-10-09-document-authoring-upgrade.md.

The Windows delivery contract is docs/superpowers/specs/2026-10-09-windows-app.md. Keep packaged
resources read-only and user projects/logs outside the installation. Bundle renderer programs with
their libraries/licenses and the plain UNO helper. Verify the actual EXE from another working
directory, using isolated sample data. Capture only the application's own window. Release checks
must identify the EXE hash and bundled tools; a source-only smoke is insufficient for Windows
delivery. Keep tool version fields limited to version lines, excluding local user paths. Record
frozen startup, frozen CLI/API export and source GUI evidence separately; an unavailable desktop
input check remains NOT_EVALUATED.

## Data and exports

- Use src/core/export.py for GUI, CLI, API and batch export orchestration. Standalone legacy
  Markdown without config.yaml retains its basic draft conversion path; legacy workspaces with
  config use the shared core.
- Preserve required chapters, missing metadata and missing spreadsheet values. A final export
  rejects missing content/assets; a draft reports its warnings.
- Write files atomically. Preserve the previous export on failure and recovery drafts on
  external-edit conflicts. Test failure paths on temporary projects.
- Templates are generic editable starting points. Institution-specific/legal compliance requires a
  supplied authoritative template.
- Validate DOCX structure and rendered PDF artifacts. File existence and process exit code alone do
  not prove field, pagination or content correctness.
- Keep batch workspace/output/cache inside its declared base. Protect every job's source paths and
  the live export lock; give each artifact a unique path.
- Renderer processes use dedicated temporary profiles. Leave user Office windows and source
  workspaces intact. Keep UI work on the Tk main thread.

## Delivery and checks

- Follow the user's global task-routing assessment and Control review. Reassess old decisions with
  the installed four-tier policy: Easy/Medium- use AGY Flash, Medium+ uses AGY Sonnet; explicit
  quota has one Luna/max fallback. Hard work is handled directly by Codex; no Dely Run or AGY
  dispatch. Review remains Codex Control's responsibility. Task preflight carries both the
  assessment file and spec file; hashes must match.
- Keep mutations scoped to the approved work. Preserve unrelated dirty files.
- Use focused regression tests that reject a present-but-wrong implementation, then run the full
  suite in an isolated copy because legacy tests use fixed temporary folders. Inspect a real GUI and
  rendered report for UI/export work.
- Run Ruff and the repository's Markdown/JSON formatter on owned changes. Match existing style; keep
  dependencies in pyproject.toml and uv.lock aligned.
- Record local verification separately from remote CI. Publication and merge require the user's
  authority for those actions.
- Treat PDF text/image presence as semantic validation; inspect real pages for layout and
  institution-specific formatting requirements.

@C:\Users\Home33\.codex\RTK.md
