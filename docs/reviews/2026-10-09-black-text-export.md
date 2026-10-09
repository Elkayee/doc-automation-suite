# Black-text export review

User request: report templates export with black text only. Control assessed the output artifact
contract as Hard; direct implementation and independent Codex Standards/Spec review found no
remaining implementation blocker.

The shared builder normalizes Word runs/styles, including theme colors and raw footnote parts, at
save time. Existing templates remain unchanged. Font sizes, bold, text, links and field semantics
are preserved. LibreOffice's newly created hyperlink style initially reintroduced 000080 into the
refreshed DOCX; the UNO helper now sets paragraph/character style CharColor to zero after field
refresh, before saving either final format.

Discriminating checks:

- The new custom-template regression failed before the fix on direct red and theme color/tint; it
  passes with source-template hash, bold/size, link and raw-footnote checks. Styling only headings
  would still fail this fixture.
- Isolated suite initially: 109 passed, one existing Starlette warning. After the version update:
  108 passed, one native-display skip, one warning. Ruff and lock checks pass. Remote CI has not
  run.
- Frozen 0.2.1 final academic export: DOCX font colors are exclusively 000000; all 1,422 PDF glyphs
  across four pages have RGB (0, 0, 0). Evidence:
  artifacts/windows-acceptance/black-text-verification.json and black-text-report.docx/pdf.

The existing 0.2.0 application was running, so 0.2.1 uses a separate versioned folder and preserves
its processes/files. The ZIP stores complete file bytes; local immutable vendor resources were
linked after hash verification. Release checks and final artifact hashes are in TASK.md and
black-text-release.json. The previously recorded frozen interactive GUI input limit remains
NOT_EVALUATED; the color change is verified through the shared core and actual frozen CLI.
