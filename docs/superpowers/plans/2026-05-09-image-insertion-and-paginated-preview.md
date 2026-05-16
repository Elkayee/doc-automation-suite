# Image Insertion And Paginated Preview Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development
> (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Let users insert ordinary report images into chapter Markdown, see them render immediately
in preview, and view preview pages that approximate DOCX pagination.

**Architecture:** Add a shared Markdown-image parser and project asset import path so the editor,
preview, and DOCX builder all understand the same image syntax. Replace chapter-per-page HTML
preview with block-based pagination that estimates page breaks from current page and paragraph
settings.

**Tech Stack:** Python, Tkinter, `tkinterweb`, `python-docx`, existing preview/docx helpers, pytest.

---

### Task 1: Lock Image Syntax And Pagination With Tests

**Files:**

- Create: `tests/test_markdown_image_support.py`
- Modify: `tests/test_preview_anchor_mapping.py`
- Modify: `tests/test_docx_builder.py`

- [ ] Add failing tests for Markdown image parsing and serialization
- [ ] Add failing tests for paginated HTML preview with images
- [ ] Add failing tests for DOCX image rendering with caption/alignment metadata

### Task 2: Shared Image Parsing And Asset Import

**Files:**

- Create: `src/core/markdown_image.py`
- Create: `src/core/image_assets.py`
- Modify: `src/ui/visual_builder/window.py`

- [ ] Implement a shared image syntax parser and serializer
- [ ] Implement project-local asset import into `assets/images`
- [ ] Add an editor action to insert image Markdown at the cursor

### Task 3: Preview Rendering And Pagination

**Files:**

- Modify: `src/ui/preview_utils.py`
- Modify: `src/ui/visual_builder/window.py`
- Modify: `src/ui/visual_builder/styles.css`

- [ ] Teach preview block parsing and HTML rendering to understand report images
- [ ] Add block-based pagination using current DOCX page and paragraph settings
- [ ] Preserve anchor-based editor/preview sync after pagination

### Task 4: DOCX Image Rendering

**Files:**

- Modify: `src/core/docx_builder.py`
- Modify: `src/core/docx_helpers.py`
- Test: `tests/test_docx_builder.py`

- [ ] Render shared Markdown image syntax into DOCX with alignment and caption support
- [ ] Reuse the shared parser instead of regex-only image handling

### Task 5: Verify

**Files:**

- Modify: none

- [ ] Run focused pytest for image, preview, and DOCX behavior
- [ ] Run Ruff checks on touched Python files
- [ ] Review diff for scope creep and note remaining fidelity gaps
