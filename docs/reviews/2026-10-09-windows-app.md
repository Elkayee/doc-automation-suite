# Windows portable application review

Scope: docs/superpowers/specs/2026-10-09-windows-app.md. Control routing: Hard; direct Codex
implementation. Standards and Spec reviewers independently examined the Windows additions to the
authorized report upgrade.

Resolved findings: conversion tools now accept the dashboard parent and open a child window without
a nested mainloop or blocking startup notice; native styles remain consistent. The release manifest
includes actual renderer version lines, dependency/build versions and file/vendor hashes. Pandoc's
version output is limited to its first line to avoid recording a machine-specific data directory.
CLI output is UTF-8, including redirected output and Vietnamese workspace paths.

## Local evidence

- 108 isolated tests pass; Ruff and uv lock check pass. The existing Starlette TestClient
  deprecation warning remains. Remote CI has not run.
- Actual GUI EXE starts from an unrelated Unicode directory, with PATH limited to Windows and an
  empty external renderer profile. Its own window was captured; writable logs and normal close exit
  0 were checked. Evidence: artifacts/windows-acceptance/frozen-startup.json and dashboard.png.
- Packaged CLI creates a Vietnamese project and produces a final academic DOCX/PDF with 4 pages,
  updated fields, embedded images, citations and editable OMML. Packaged API starts, reports
  capabilities and creates an office project outside the bundle. Both renderer paths resolve inside
  the distribution. Evidence: artifacts/windows-acceptance/packaged-verification.json and
  packaged-academic.pdf.
- Current native source GUI exercises metadata/table forms, save and the actual Word/PDF toolbar
  using the bundled renderers. 374 heartbeat callbacks prove the event loop runs during export;
  rendered content includes the form/table input. Evidence:
  artifacts/windows-acceptance/native-authoring.json and native-authoring.png.
- Initial frozen GUI candidate also created a project and opened the editor. Full
  create/edit/save/export interaction on the final frozen EXE is NOT_EVALUATED: Windows focus
  automation prevented input and the failed sequence was stopped after two attempts. Source GUI and
  frozen CLI/API evidence are separate; they do not certify that unexecuted sequence.

Control found no remaining concrete implementation blocker. Deliver the locally built portable
candidate with the above verification limit recorded. Templates remain generic; no
institution-specific formatting approval or publication is claimed.

Final GUI SHA-256: 4f939f435727eac3e5a928f0e959ea6661b11d04bc56603110c80bcb68d26174. Final CLI
SHA-256: 496c6effb4c030043dd3c7899c24514db6d22f8f650799dccbff748002689f85. ZIP contents/hash
validation is recorded in TASK.md after archive completion.
