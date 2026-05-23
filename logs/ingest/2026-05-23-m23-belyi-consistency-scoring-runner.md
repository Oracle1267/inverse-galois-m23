---
type: ingest-log
status: active
created: 2026-05-23
last_confirmed: 2026-05-23
confidence: 0.78
quality_score: 0.82
sensitivity: internal
source: "local implementation and smoke report"
sources:
  - "[[wiki/m23-belyi-gf7-targeted-overnight-result]]"
  - "[[experiments/m23/reports/gf7-branch-search/consistency-smoke]]"
entities:
  - "[[entities/projects/m23-proof-factory]]"
  - "[[entities/concepts/belyi-map]]"
  - "[[entities/concepts/galois-candidate-search]]"
relationships:
  - target: "[[wiki/m23-belyi-consistency-scoring-runner]]"
    type: "supports"
    confidence: 0.86
supersedes: []
superseded_by: []
review_after: 2026-06-23
---

# M23 Belyi Consistency Scoring Runner Ingest

## Source

- Source: local code changes in `experiments/m23/src/m23verify/consistency.py`, `experiments/m23/src/m23verify/branch_search.py`, and `experiments/m23/scripts/search_lambda_branches.py`.
- Source kind: implementation, tests, and generated smoke report.
- Sensitivity: internal.

## Actions

- Added symbolic partial consistency scoring for reconstructed Belyi branch candidates.
- Added branch-score priority for hard exact-equation contradictions.
- Tightened early stopping so complete but inexact reconstructions do not terminate the branch search.
- Fixed consistency-score ordering so candidates below `--consistency-min-unique` do not outrank candidates that were actually consistency-scored.
- Added CLI flags `--score-consistency` and `--consistency-min-unique`.
- Added checkpoint compatibility metadata for consistency-scored runs.
- Added a controlled smoke report under `experiments/m23/reports/gf7-branch-search/`.

## Entities Created or Updated

- Updated [[entities/projects/m23-proof-factory]] by adding a more discriminating local search loop behavior.

## Wiki Pages Created or Updated

- Created [[wiki/m23-belyi-consistency-scoring-runner]].
- Updated [[wiki/m23-elkies-finite-field-solver]].
- Updated [[wiki/m23-belyi-gf7-targeted-overnight-result]].
- Updated [[index]].
- Updated [[dashboards/llm-wiki-dashboard]].

## Privacy Filtering

- No private or credential-like content was included. Generated reports contain only mathematical search artifacts and local relative paths.

## Confidence and Quality Notes

- Confidence is moderate-high for the implementation behavior because focused tests and a CLI smoke were run.
- Confidence remains exploratory for mathematical promise; this is a search heuristic, not a proof.

## Follow-Up

- Run the recommended `GF(7)` consistency-scored continuation from the current best prefix.
- Inspect whether the best branch reduces hard contradiction count before optimizing only for unique reconstruction count.
