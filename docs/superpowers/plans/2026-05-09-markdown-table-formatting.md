# Markdown Table Formatting Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development
> (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Improve Markdown-table-to-DOCX rendering so tables no longer inherit paragraph formatting
that makes them look unbalanced, and so header/body cells render with clearer table-specific
styling.

**Architecture:** Keep table parsing in `DocxBuilder`, but move table-cell formatting decisions into
`DocxHelpers` so table styling is centralized and testable. Preserve current document behavior
outside tables and add regression coverage for the table-only rules.

**Tech Stack:** Python, `python-docx`, `pytest`, existing `DocxBuilder` / `DocxHelpers` utilities.

---

### Task 1: Lock Table Formatting Behavior With Tests

**Files:**

- Modify: `tests/test_docx_builder.py`
- Test: `tests/test_docx_builder.py`

- [ ] **Step 1: Add failing tests for table formatting**
- [ ] **Step 2: Run focused tests and confirm the table-format assertions fail for the intended
      reason**

### Task 2: Centralize Table Cell Formatting

**Files:**

- Modify: `src/core/docx_helpers.py`
- Modify: `src/core/docx_builder.py`
- Test: `tests/test_docx_builder.py`

- [ ] **Step 1: Add helper(s) for formatting Markdown table cells in DOCX**
- [ ] **Step 2: Apply those helpers from the Markdown table branch in `DocxBuilder`**
- [ ] **Step 3: Keep existing non-table paragraph formatting untouched**

### Task 3: Verify

**Files:**

- Modify: none
- Test: `tests/test_docx_builder.py`

- [ ] **Step 1: Run focused pytest for DOCX builder formatting**
- [ ] **Step 2: Run Ruff checks on touched files**
- [ ] **Step 3: Review resulting diff for scope and regressions**
