# Visual Doc Builder Implementation Plan

**Goal:** ship a usable three-pane workspace for editing chapter markdown, previewing the assembled document, and exporting `.docx` from the current workspace.

**Execution rule:** reuse the current assembler, preview helpers, and DOCX build path. Do not create a second export pipeline.

## Task 1: Stabilize Core Ordering and Assembly

**Files**
- Modify: `src/core/config.py`
- Modify: `src/core/assembler.py`

- [ ] Add optional `chapter_order` support to `TemplateConfig`
- [ ] Add a save path for updating chapter order in `config.yaml`
- [ ] Make the assembler resolve chapter order from `chapter_order` first, then `required_files`
- [ ] Expose assembled chapter metadata for UI use

## Task 2: Build the Visual Builder Window

**Files**
- Create: `src/ui/visual_builder/__init__.py`
- Create: `src/ui/visual_builder/window.py`

- [ ] Create a `Tkinter` `Toplevel` with navigator, editor, preview, and toolbar areas
- [ ] Load chapters from the active workspace
- [ ] Show the selected chapter in the editor
- [ ] Add `Move Up`, `Move Down`, `Save`, `Refresh`, and `Build DOCX` actions

## Task 3: Add Editing Behavior and Word-style Formatting

**Files**
- Modify: `src/ui/visual_builder/window.py`
- Modify: `src/core/config.py`

- [ ] Add lightweight markdown highlighting in the editor
- [ ] Implement a "Paragraph Settings" dialog (Alignment, Indent, Spacing)
- [ ] Save formatting settings to `config.yaml` under a `formatting` key
- [ ] Add debounced autosave
- [ ] Track dirty state in the window title and status label

## Task 4: Add Assembled Preview with Custom Styling

**Files**
- Create: `src/ui/visual_builder/styles.css`
- Modify: `src/ui/visual_builder/window.py`

- [ ] Render preview from the assembled workspace, not just the current chapter
- [ ] Dynamic CSS generation: Inject the user's paragraph settings into the HTML preview
- [ ] Use `tkinterweb.HtmlFrame` when available
- [ ] Style preview pages as A4-like chapter pages with stable anchors

## Task 5: Hierarchical Navigation (Outline)

**Files**
- Modify: `src/ui/visual_builder/window.py`

- [ ] Add a "Headings" tab to the Navigator
- [ ] Parse Markdown headers from the assembled document to build a tree
- [ ] Implement "Click-to-jump": clicking a heading jumps the editor to that section

## Task 5: Integrate with Dashboard

**Files**
- Modify: `src/ui/dashboard.py`

- [ ] Replace the minimal workspace popup with `VisualBuilderWindow`
- [ ] Keep the existing legacy workflow entry point available

## Task 6: Verify the Workflow

**Files**
- No code changes required

- [ ] Open a workspace from the dashboard
- [ ] Edit a chapter and confirm autosave
- [ ] Reorder chapters and confirm order persists in `config.yaml`
- [ ] Confirm preview refresh stays within the 800 ms debounce target
- [ ] Run DOCX export from the visual builder
