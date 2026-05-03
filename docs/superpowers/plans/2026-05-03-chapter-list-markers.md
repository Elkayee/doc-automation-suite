# Chapter List Markers Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add per-chapter and per-subchapter configurable bullet markers by nesting level, and apply them consistently in the visual builder preview and DOCX export.

**Architecture:** Store per-file settings in `config.yaml` under `settings.chapter_settings.<filename>`. Add a focused helper for chapter-scoped settings lookup and list-marker resolution. Keep markdown syntax standard in the editor, then render/export with configured markers based on indentation level.

**Tech Stack:** Python, Tkinter, python-docx, existing markdown/preview pipeline, unittest

---

### Task 1: Add failing tests for chapter-scoped list marker resolution

**Files:**
- Create: `tests/test_chapter_list_markers.py`
- Test: `tests/test_chapter_list_markers.py`

- [ ] **Step 1: Write the failing test**
- [ ] **Step 2: Run test to verify it fails**
- [ ] **Step 3: Implement minimal chapter settings helper**
- [ ] **Step 4: Run test to verify it passes**

### Task 2: Add failing tests for preview list parsing/rendering with custom markers

**Files:**
- Modify: `tests/test_preview_anchor_mapping.py`
- Test: `tests/test_preview_anchor_mapping.py`

- [ ] **Step 1: Write failing tests for nested list marker selection**
- [ ] **Step 2: Run test to verify it fails**
- [ ] **Step 3: Extend preview parsing/rendering to keep list items separate and apply configured markers**
- [ ] **Step 4: Run test to verify it passes**

### Task 3: Add chapter marker settings UI in visual builder

**Files:**
- Modify: `src/ui/visual_builder/window.py`

- [ ] **Step 1: Add toolbar action for current chapter list markers**
- [ ] **Step 2: Add dialog that edits level-1..level-5 markers for the selected file**
- [ ] **Step 3: Save under `settings.chapter_settings.<filename>.list_markers_by_level`**
- [ ] **Step 4: Refresh preview after save**

### Task 4: Apply configured markers in DOCX export

**Files:**
- Modify: `src/core/docx_builder.py`
- Modify: `src/core/docx_helpers.py`

- [ ] **Step 1: Resolve effective marker for each bullet line from file + indent level**
- [ ] **Step 2: Emit bullet paragraphs with configured marker text**
- [ ] **Step 3: Keep existing indentation behavior**
- [ ] **Step 4: Verify export path still builds**

### Task 5: Verify end to end

**Files:**
- Test: `tests/test_chapter_list_markers.py`
- Test: `tests/test_preview_anchor_mapping.py`

- [ ] **Step 1: Run targeted unit tests**
- [ ] **Step 2: Run `python -m compileall src`**
- [ ] **Step 3: Smoke-check preview and DOCX builder logic**
