# Report authoring upgrade

Approved scope: the user requested implementation on 2026-10-09 after reviewing
docs/research/2026-10-09-document-authoring-upgrade.md. All three priorities apply: Word/PDF
quality, authoring UI, and CLI/API/batch automation.

Keep the existing Python/Tkinter application and Markdown/YAML workspaces. Provide generic editable
academic and office templates; no claim of institution-specific or legal compliance. Preserve
existing workspaces and the research report.

## Delivery

1. Fix required-chapter validation, missing-image validation, stale render cache, legacy settings
   and the default report scaffold. Add atomic saves/recovery.
2. A shared export function serves GUI, CLI, API and make.py. Draft exports may carry warnings;
   final exports reject missing required content/assets. Existing default DOCX commands remain
   usable as drafts.
3. Complete report metadata, semantic headings, sections, page fields, TOC, numbered
   captions/cross-references and document templates. Add authoring forms, grouped Vietnamese
   actions, background export and recovery/conflict handling.
4. Add PDF export with explicit renderer discovery/failure, field refresh and actual artifact
   checks; sequential manifest batches with independent results. Keep desktop Word automation
   separate from unattended API execution.
5. Add academic citations/equations through a proven Pandoc path and CSV/XLSX metadata input for
   batches, preserving missing values.

## Acceptance instruments and counterexamples

| Requirement                  | Instrument                                               | Present-but-wrong counterexample                                                            |
| ---------------------------- | -------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| Required chapters/assets     | Regression and export tests                              | Export succeeds but silently omits a required chapter or substitutes an error for an image  |
| Correct cached diagrams/math | Mock renderer with changed source and identical position | Changed source retrieves the first image                                                    |
| Settings compatibility       | Export XML/config assertions                             | Legacy spacing setting is accepted but ignored                                              |
| Safe saves/recovery          | Inject write failure and external edit                   | Partial write or autosave overwrites the external version                                   |
| Shared entrypoints           | CLI/API/core integration tests                           | Same input has different validation or semantic DOCX structure                              |
| Report structure             | DOCX XML plus rendered sample inspection                 | Heading text looks right but is not semantic; TOC/page fields are stale                     |
| PDF                          | Open/check/extract real generated PDF                    | Exit code is zero but PDF is absent, empty or missing expected text/fields                  |
| Batch/data                   | Mixed success/error and missing-value tests              | First failed item aborts later items; missing spreadsheet value becomes zero                |
| GUI                          | Native smoke and actual visible authoring inspection     | Export blocks event loop, action cannot be reached at laptop width, or recovery loses edits |
| Citations/equations          | Render fixture and inspect DOCX OMML/references          | LaTeX is only an image or citation text remains unresolved                                  |

Known risks: data preservation, changed validation contract, background/UI state, external renderer
behavior, and template fidelity. No user reports are used for destructive checks. User-standard
templates, public hosting, merge and publication remain outside this local implementation.
