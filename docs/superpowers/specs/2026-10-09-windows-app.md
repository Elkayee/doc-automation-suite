# Windows application delivery

The user requested a complete Windows EXE with a polished interface on 2026-10-09. This extends the
approved report-authoring implementation, preserving existing Markdown/YAML workspaces and the
shared export core.

Deliver a portable Windows x64 folder containing DocAutomationSuite.exe, Python runtime
dependencies, templates, TkinterWeb resources, LibreOffice and Pandoc. Provide a ZIP of the complete
folder. Users run the EXE without installing Python or a separate document renderer; the complete
folder must stay together.

Packaged resources are read-only. New projects and logs belong under
LOCALAPPDATA/DocAutomationSuite; existing folders remain openable. Source launches retain the
repository's workspaces directory. DOC_SUITE_DATA_DIR supports an explicit alternative data location
and isolated verification.

Use native Tkinter/ttk with consistent Segoe UI typography, navy/blue actions, light surfaces,
visible keyboard focus, a branded dashboard, clear template selection, and a spacious editor with
separate editing/export actions. Preserve background export, recovery and current document
capabilities. Add an application icon, Windows DPI awareness, meaningful startup errors and a
user-accessible log.

Expose packaged automation through an EXE console companion for existing CLI/API commands, sharing
the same bundled resources and export core. Do not introduce a second export implementation.

Acceptance: run the actual GUI EXE from a different working directory; capture only its own window;
create/open/edit/save a sample project; export real Word/PDF; verify bundled renderers are used and
reports contain expected content. Test resource/data paths and isolated regressions. Produce a
manifest with artifact hashes and dependency/tool versions, usage instructions and local
verification. Update PLAN.md, TASK.md and AGENTS.md at milestones. No publication/merge is
requested.

Build references: [PyInstaller usage](https://pyinstaller.org/en/stable/usage.html) and
[TkinterWeb packaging](https://tkinterweb.readthedocs.io/en/latest/faq.html).
