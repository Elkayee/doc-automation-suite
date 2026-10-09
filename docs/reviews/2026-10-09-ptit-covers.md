# PTIT cover review

Codex Control reviewed this change directly under the installed four-tier routing policy. The
finalized spec/context assessment is Hard, approved for direct Codex; no Dely Run or AGY review was
dispatched. The git baseline was clean. Changes are limited to the essay templates, template
generator/loader, metadata substitution, version alignment, tests and related documentation.

Two existing-selector choices now use the user's authoritative
`dist/DocAutomationSuite-0.2.1/Cover_Ptit.docx`: group assignments with five member slots and
individual assignments with student name and ID. The original is copied byte-for-byte to
`templates/tieu_luan_nd30/Cover_Ptit.docx`; its SHA-256 is
`bac9504df4041f5fa6ce0f72cdcc71b397d7ca7fd6fc740cf272825f82755fa4`. New projects copy an editable
DOCX. Existing project configuration/templates remain unchanged. Required metadata uses existing
draft warnings/final rejection.

| Requirement                                    | Instrument and observed rejection                                                                                                                                                                                                                                  |
| ---------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Correct group/individual cover and author data | Both template exports and XML/text checks pass. Mutation probes export successfully but reject an individual label on the group template and stale author/ID text.                                                                                                 |
| Preserve source layout/logo                    | Table properties, section margins, original EMF bytes and drawing presence match. A successful missing-logo export is rejected by the mutation oracle.                                                                                                             |
| Keep the original center alignment             | The initial present-but-wrong implementation inherited the body indent; the regression rejected missing explicit cover indentation. Source indents now match, including intentional indents in the original. Rendered covers were compared with the original page. |
| Preserve rich text and missing values          | Split-run placeholder test retains bold/italic and treats inserted placeholder-like text literally. Missing student ID is visible in the draft, rejects final export and preserves the previous DOCX.                                                              |
| Keep legacy projects                           | Non-PTIT template test retains literal text and its original section count. No user workspaces were edited.                                                                                                                                                        |
| Usable choice and metadata forms               | Actual source Tk windows show both template labels. Group form is 534 px high; individual form is 370 px high. Separate window-only captures document the selector and forms.                                                                                      |
| Real reports                                   | Group and individual final Word/PDF exports each have three pages, a single cover, readable title/author/ID, logo, updated TOC/page fields and only black PDF text glyphs. Actual cover pages were inspected.                                                      |

The final export also rejects the earlier successful-but-wrong candidate that printed an internal
cover instruction on the TOC page. A baseline-red regression observed the leaked text; the existing
[[COVER]] marker now acknowledges the loaded cover without creating a second cover. Final DOCX/PDF
contain one cover and no instruction text.

Source verification: focused tests pass; full suite in
`C:/Users/Home33/AppData/Local/Temp/doc-suite-ptit-r2-tests-_ggxcfge` reports 114 passed, one
existing Starlette/httpx warning, 11.49 seconds. Ruff and offline lockfile verification pass.
Evidence is under `artifacts/windows-acceptance/ptit-final-r2/`, including source-verification.json,
mutation-probes.json, rendered covers and source GUI captures.

The separate Windows 0.2.2 distribution is verified locally. From a temporary cwd with isolated data
and a restricted PATH, the actual frozen CLI created both template projects and exported final
DOCX/PDF; frozen API exported the individual project. Both exports use the bundled
LibreOffice/Pandoc paths. The actual GUI started and its own window was captured with PrintWindow,
avoiding unrelated desktop pixels. Full frozen GUI input remains NOT_EVALUATED: Orca's synthetic
click was unverified, and the target later stopped being observable. No claim of a completed GUI
input workflow is made from that attempt.

GUI SHA-256: `94c06249520839540c2ccfd68729f916d3ab77e7d8e635db0c37b311cd70c9c4`. CLI SHA-256:
`fd0f70754e0801d7dd81e3ca86d5413879e1babc7431738268499fed05487f9f`. ZIP SHA-256:
`1a1cde987199d214e7f00698dc5f02c155482dbcbce934f1b6ce72b14b96c5f2`. The ZIP is 633,316,772 bytes;
all 20,853 manifest-listed files match the release manifest, which also matches the distribution
folder. Version lines identify LibreOffice 26.8.1.1 and Pandoc 3.11 without local user paths. The
original 0.2.1 cover hash remains exact. Evidence: frozen-verification.json,
release-verification.json and frozen report cover captures under the same ptit-final-r2 evidence
folder. This is local verification; no remote CI, publication or merge is claimed.

Limits: five group-member slots follow the supplied source. The report editor's HTML preview remains
approximate; inspect exported PDF for exact pagination. No assertion of broader institution
compliance is made beyond the supplied cover.

The final ZIP contains 20,854 entries including the manifest. Final frozen Word/PDF exports also
reject internal instruction text and retain a clean TOC.
