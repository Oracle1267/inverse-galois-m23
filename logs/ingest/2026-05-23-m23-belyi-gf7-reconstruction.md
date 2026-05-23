---
type: ingest-log
status: active
created: 2026-05-23
last_confirmed: 2026-05-23
confidence: 0.78
quality_score: 0.85
sensitivity: internal
source: "M23 GF(7) Belyi rational reconstruction local runs"
sources:
  - "[[wiki/m23-belyi-gf7-lift-report]]"
  - "[[experiments/m23/reports/gf7-reconstruction/gf7-reconstruct-lambda223-10000-mod282475249]]"
entities:
  - "[[entities/projects/m23-proof-factory]]"
  - "[[entities/concepts/belyi-map]]"
relationships:
  - target: "[[wiki/m23-belyi-gf7-reconstruction-report]]"
    type: "supports"
    confidence: 0.86
supersedes: []
superseded_by: []
review_after: 2026-06-23
---

# M23 Belyi GF(7) Reconstruction Log

## Source

- Source: local lift and reconstruction tool outputs.
- Source kind: generated JSON and Markdown reports.
- Sensitivity: internal.

## Actions

- Added a rational reconstruction helper and CLI.
- Added test coverage for integer residues, fractional residues, exact degenerate reconstruction, and the reconstruction CLI.
- Exposed `lambda` correction digits in the lift helper and CLI.
- Tested the zero-free-variable lift branch.
- Tested a first greedy `lambda` branch search.
- Created [[wiki/m23-belyi-gf7-reconstruction-report]].
- Updated [[index]] and [[wiki/m23-elkies-finite-field-solver]].

## Result

- The zero-free-variable branch reached `7^10` and reconstructed only partially.
- A steered branch with `lambda` corrections `[3,4,0,0,0,0,0,0,0]` reached `7^10` and improved reconstruction to 16/25 unique coefficients under a 10000/10000 bound.
- The same branch reached `7^12`, but a wider 80000/80000 reconstruction window remained partial.
- No complete rational Belyi map has been reconstructed yet.

## Privacy Filtering

- No sensitive or private material was included.

## Follow-Up

- Build a systematic free-parameter search over `lambda` correction sequences with backtracking or beam search.

