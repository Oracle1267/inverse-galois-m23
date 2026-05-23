---
type: ingest-log
status: active
created: 2026-05-23
last_confirmed: 2026-05-23
confidence: 0.86
quality_score: 0.88
sensitivity: internal
source: "M23 GF(7) Belyi modular survivor local run"
sources:
  - "[[wiki/m23-belyi-gf7-deep-100000-report]]"
  - "[[experiments/m23/reports/gf7-exhaustive/gf7-normalized-290000-300000]]"
entities:
  - "[[entities/projects/m23-proof-factory]]"
  - "[[entities/concepts/belyi-map]]"
  - "[[entities/concepts/galois-candidate-search]]"
relationships:
  - target: "[[wiki/m23-belyi-gf7-modular-survivor-report]]"
    type: "supports"
    confidence: 0.90
supersedes: []
superseded_by: []
review_after: 2026-06-23
---

# M23 Belyi GF(7) Survivor Log

## Source

- Source: `experiments/m23/reports/gf7-exhaustive/`
- Source kind: local batch-runner output.
- Sensitivity: internal.

## Actions

- Ingested the completed `GF(7)` runner output that stopped with `stopped_reason: solution_found`.
- Identified one survivor in `experiments/m23/reports/gf7-exhaustive/gf7-normalized-290000-300000.json`.
- Independently verified the survivor from its stored coefficients.
- Created [[wiki/m23-belyi-gf7-modular-survivor-report]].
- Marked [[wiki/m23-belyi-gf7-deep-100000-report]] as superseded by the survivor report.
- Updated [[wiki/m23-elkies-finite-field-solver]] and [[index]].

## Result

- Runner interval: 100,000-300,000 tested triples.
- Total constrained `GF(7)` coverage including the earlier checkpoint: 300,000 tested triples.
- Solutions found: 1.
- Survivor lambda: 6.
- Identity residual mod 7: all zero.
- Derivative residual mod 7: all zero.
- Translation normalization residual: 0.
- Left factors pairwise coprime: true.

## Privacy Filtering

- No sensitive or private material was included.

## Follow-Up

- Use the modular survivor as a seed for lifting or rational reconstruction rather than continuing blind `GF(7)` enumeration as the immediate next step.

