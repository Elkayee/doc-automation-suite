# CLAUDE.md

Behavioral guidelines to reduce common LLM coding mistakes. Merge with project-specific instructions
as needed.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:

- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:

- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:

- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:

- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:

```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant
clarification.

---

**These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to
overcomplication, and clarifying questions come before implementation rather than after mistakes.
This file provides guidance to Claude Code (claude.ai/code) when working with code in this
repository.

## Project Overview

This repository is a specialized toolkit for document processing and office automation, primarily
focused on `.docx`, `.xlsx`, and `.pptx` files. It includes a comprehensive collection of "skills"
(modular AI guidance) for handling complex office document formatting, conversion, and
standardization, particularly following Vietnamese administrative standards (NĐ 30).

## NMCNPM Group Project Requirements

- **Group Size**: 5-6 members with 1 designated leader.
- **Deadline**: Before 23:00 on 2026-04-25.
- **Shared Tasks**:
  - Problem description (user requirements).
  - Software Requirements Specification (SRS): functional and non-functional.
  - General Use Case (UC) diagram.
  - Entity Class diagram.
- **Individual Member Tasks** (at least 1 complex UC per member):
  - Detailed UC diagram.
  - UC Specification.
  - Activity diagram.
  - _Note_: Choose "large" UCs with business logic/constraints; avoid simple CRUD or Auth.

## Report Structure (DOCX/PDF)

- **Cover Page**: Topic name, member list with assigned UCs.
- **Part 1 (Common Tasks)**:
  - Problem Description (Natural language, 2-3 pages, customer perspective).
  - Software Requirements (Actors, functional/UCs, non-functional, general UC diagram).
  - Entity Class Diagram (Entities, properties, methods, relationships).
- **Part 2 (Individual Results)**:
  - Detailed UC Diagram.
  - UC Specification.
  - Activity Diagram.

## Architecture & Structure

- `/skills`: The core of the repository, containing specialized guidance and scripts for various
  tasks.
  - `handling-docx-files/`: Technical skills for low-level `.docx` manipulation (XML/OOXML).
  - `xu-ly-van-phong/`: High-level office automation following Vietnamese standards, including
    templates and color palettes.
  - `subagent-driven-development/`, `systematic-debugging/`, `test-driven-development/`: General
    software engineering methodology skills.
- `/node_modules`: Project dependencies (managed by npm).
- `package.json`: Defines project dependencies (currently includes `docx`).

## Development Commands

### Environment Setup

- Install dependencies: `npm install`
- Install Python dependencies (for document scripts):
  `pip install python-docx openpyxl pypdf pdfplumber pdf2docx`

### Document Processing (via scripts)

Many scripts are located within specific skill directories.

- Unpack DOCX: `python skills/xu-ly-van-phong/scripts/office/unpack.py <file.docx> <output_dir>`
- Pack DOCX: `python skills/xu-ly-van-phong/scripts/office/pack.py <input_dir> <output.docx>`
- Convert DOC to DOCX:
  `python skills/xu-ly-van-phong/scripts/office/soffice.py --headless --convert-to docx <file.doc>`
- Convert PDF to DOCX:
  `python skills/xu-ly-van-phong/scripts/convert/convert_pdf_to_docx.py <input.pdf> <output.docx>`

## Code Style & Standards

- **Office XML Manipulation**: When editing existing documents, prefer unpacking to XML, modifying,
  and repacking to preserve formatting.
- **Vietnamese Standards**: Follow `skills/xu-ly-van-phong/standards/nd30.md` for administrative
  documents.
- **Consistency**: Use the color palettes defined in `skills/xu-ly-van-phong/standards/color/` for
  professional deliverables.
- **Skills Usage**: Refer to `SKILL.md` in each subdirectory for specific usage patterns and common
  mistakes.
