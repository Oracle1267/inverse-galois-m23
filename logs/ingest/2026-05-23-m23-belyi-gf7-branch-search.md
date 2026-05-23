---
type: ingest-log
status: active
created: 2026-05-23
last_confirmed: 2026-05-23
confidence: 0.78
quality_score: 0.85
sensitivity: internal
source: "M23 GF(7) lambda branch-search local run"
sources:
  - "[[wiki/m23-belyi-gf7-reconstruction-report]]"
  - "[[experiments/m23/reports/gf7-branch-search/gf7-lambda-beam25-depth5-mod282475249]]"
entities:
  - "[[entities/projects/m23-proof-factory]]"
  - "[[entities/concepts/belyi-map]]"
relationships:
  - target: "[[wiki/m23-belyi-gf7-lambda-branch-search-report]]"
    type: "supports"
    confidence: 0.86
supersedes: []
superseded_by: []
review_after: 2026-06-23
---

# M23 Belyi GF(7) Branch Search Log

## Source

- Source: local beam-search tool output.
- Source kind: generated JSON and Markdown reports.
- Sensitivity: internal.

## Actions

- Added a lambda branch-search helper and CLI.
- Added test coverage for branch-search history and CLI report writing.
- Ran a large beam-search attempt with beam width 25 and depth 5. The shell command timed out, but the process produced valid JSON and Markdown reports.
- Ran a smaller bounded beam-search attempt with beam width 5 and depth 4 as a fallback check.
- Created [[wiki/m23-belyi-gf7-lambda-branch-search-report]].
- Updated [[index]] and [[wiki/m23-elkies-finite-field-solver]].

## Result

- Strongest completed branch-search run: beam width 25, depth 5, lift level 10.
- Evaluated branches: 581.
- Best prefix: `[3, 4, 0, 0, 0]`.
- Best lambda: 223.
- Best reconstruction score: 16/25 unique coefficients.
- Status: partial.

## Privacy Filtering

- No sensitive or private material was included.

## Follow-Up

- Add checkpointing and progress output before running wider branch searches.
- Consider cheaper branch scoring before full rational reconstruction.
