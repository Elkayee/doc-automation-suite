# Visual Doc Builder Design

## Overview

Create a three-pane editing workspace for `doc-automation-suite` that lets users edit chapter markdown, preview the assembled document in an A4-like visual layout, and export the current workspace to `.docx`.

This design is intentionally aligned with the current codebase:

- `config.yaml` already defines the chapter set through `required_files`.
- `src/core/assembler.py` is the assembly boundary for preview and export.
- `src/core/docx_builder.py` remains the only authoritative export path.

The preview is a high-fidelity editing aid, not a byte-for-byte representation of the final Word layout.

## Scope

### In Scope
- Navigate and edit files under `workspace/chapters/`
- Persist chapter order for preview and export
- Debounced autosave back to chapter markdown files
- Assembled preview rendered inside the app
- One-click DOCX export through the existing build pipeline
- Basic file change detection for external edits

### Out of Scope
- True Word layout parity
- Character-accurate line mapping between Tk text layout and browser layout
- Full drag-and-drop tree management
- Multi-user editing

## Architecture

The application is a Tkinter `Toplevel` with three panes:

### 1. Navigator
- Lists chapter files from the active workspace
- Uses persisted chapter order from `config.yaml`
- Supports explicit reorder actions (`Move Up` / `Move Down`)
- Shows dirty state for the currently edited chapter

### 2. Editor
- Edits one markdown file at a time
- Applies lightweight markdown highlighting for common patterns
- Debounces autosave to disk
- Tracks in-memory dirty state until the pending autosave completes

### 3. Visualizer
- Renders the assembled document preview from all chapters
- Uses `tkinterweb.HtmlFrame` when available
- Falls back to the existing styled `tk.Text` preview when `tkinterweb` is unavailable
- Uses A4-styled page containers and chapter page breaks

## Data Model

### Source of Truth
The `.md` files in `workspace/chapters/` remain the source of truth for content.

### Chapter Order Persistence
Chapter order is persisted in `workspace/config.yaml` as `chapter_order`.

Rules:
- `chapter_order` is optional
- when absent, the app falls back to `required_files`
- reorder actions update `chapter_order`
- export and assembled preview must use the same resolved order

### Assembly Metadata
The assembler must expose chapter metadata for the UI:
- ordered file paths
- assembled markdown
- per-chapter start and end line offsets in the assembled document

This metadata is used for:
- chapter-level preview structure
- chapter selection and refresh behavior
- future sync improvements

## Save and Watch Model

The editor uses this contract:

1. User types into the editor
2. The buffer becomes dirty immediately
3. Autosave runs after a debounce interval
4. Dirty state clears only after a successful write
5. Preview refresh is scheduled from the same debounce cycle

External file monitoring uses lightweight polling by file mtime, not an extra dependency.

Rules:
- self-generated writes must not trigger reload thrash
- if the current file changes on disk and the editor is clean, reload it
- if the current file changes on disk while the editor is dirty, show a warning and keep the in-memory buffer

## Preview Model

### Rendering Strategy
- Build the preview from the assembled workspace, not only the current file
- Render each chapter inside an A4-styled `<section class="page">`
- Apply consistent document CSS for headings, tables, block quotes, images, and code blocks

### Fidelity Contract
The preview is "editorial fidelity", not "Word fidelity".

That means:
- chapter order must match export
- markdown structure must match export intent
- common block styling should look stable and readable
- exact page breaks, font metrics, and line wraps are not guaranteed to match the generated `.docx`

### Synchronization
Phase 1 supports bounded sync only:
- navigator selection loads the matching chapter into the editor
- saving or reordering updates the assembled preview
- preview chapters carry stable anchors by filename

Bi-directional line-to-DOM scroll sync is deferred until the assembler provides a richer source map and the preview path exposes reliable element geometry.

## Components and Responsibilities

### `src/core/config.py`
- load optional `chapter_order`
- save updated `chapter_order`

### `src/core/assembler.py`
- resolve ordered chapter filenames
- assemble markdown in the resolved order
- return chapter metadata for preview/UI use

### `src/ui/visual_builder/window.py`
- compose navigator, editor, preview, and toolbar
- manage autosave and file polling
- trigger preview refresh and DOCX export

### `src/ui/preview_utils.py`
- continue to provide markdown-to-HTML conversion
- remain the fallback path for text-only preview

## Success Criteria

- [ ] User can open a workspace and navigate every chapter from a sidebar
- [ ] Reordering chapters changes both preview order and export order
- [ ] Editor changes save back to the chapter file after a debounce interval
- [ ] Assembled preview refreshes within 800 ms after typing stops
- [ ] User can export the active workspace to a `.docx` through the existing builder
- [ ] App remains functional when `tkinterweb` is unavailable

## Risks and Mitigations

### Risk: Preview diverges from exported DOCX
Mitigation:
- keep export authoritative
- use the same assembler order for preview and export
- document the fidelity contract clearly in code and docs

### Risk: External file updates overwrite local edits
Mitigation:
- track dirty state explicitly
- poll mtimes
- only auto-reload clean buffers

### Risk: `tkinterweb` is unavailable or unstable
Mitigation:
- keep the in-app text preview fallback
- do not block editing or export on HTML preview availability

### Risk: Large documents slow down rendering
Mitigation:
- debounce preview rebuilds
- reuse existing markdown rendering helpers
- keep preview refresh scoped to assembled markdown generation plus HTML render
