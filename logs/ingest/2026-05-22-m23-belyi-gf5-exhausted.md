---
type: ingest-log
status: active
created: 2026-05-22
last_confirmed: 2026-05-22
confidence: 0.86
quality_score: 0.88
sensitivity: internal
source: "M23 GF(5) Belyi exhaustive local run"
sources:
  - "[[wiki/m23-belyi-gf5-contiguous-32000-report]]"
entities:
  - "[[entities/projects/m23-proof-factory]]"
  - "[[entities/concepts/belyi-map]]"
relationships:
  - target: "[[wiki/m23-belyi-gf5-exhausted-report]]"
    type: "supports"
    confidence: 0.90
supersedes: []
superseded_by: []
review_after: 2026-06-22
---

# M23 Belyi GF(5) Exhausted Log

## Actions

- Ingested the completed local runner output from `experiments/m23/reports/gf5-exhaustive/`.
- Confirmed the runner stopped with `stopped_reason: exhausted`.
- Confirmed the runner found no solutions.
- Created [[wiki/m23-belyi-gf5-exhausted-report]].
- Marked [[wiki/m23-belyi-gf5-contiguous-32000-report]] as superseded.
- Updated [[wiki/m23-elkies-finite-field-solver]] and [[index]].

## Result

- Tested left-factor triples in local runner interval: 180,636.
- Total constrained `GF(5)` tested triples including previous checkpoints: 212,636.
- Solutions found: 0.
- The constrained `GF(5)` search line is exhausted.

## Privacy Filtering

- No sensitive or private material was included.

## Follow-Up

- Decide whether to deepen `GF(7)` or add stronger Belyi/branch-cycle constraints before scaling.
