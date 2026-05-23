---
type: ingest-log
status: active
created: 2026-05-23
last_confirmed: 2026-05-23
confidence: 0.80
quality_score: 0.86
sensitivity: internal
source: "M23 GF(7) checkpointed lambda branch runner"
sources:
  - "[[wiki/m23-belyi-gf7-lambda-branch-search-report]]"
  - "[[experiments/m23/reports/gf7-branch-search/gf7-checkpointed-smoke]]"
entities:
  - "[[entities/projects/m23-proof-factory]]"
  - "[[entities/concepts/belyi-map]]"
  - "[[entities/concepts/galois-candidate-search]]"
relationships:
  - target: "[[wiki/m23-belyi-gf7-overnight-branch-runner]]"
    type: "supports"
    confidence: 0.86
supersedes: []
superseded_by: []
review_after: 2026-06-23
---

# M23 Belyi GF(7) Overnight Runner Log

## Source

- Source: local code changes, test output, and generated smoke-run artifacts.
- Source kind: generated tooling and reports.
- Sensitivity: internal.

## Actions

- Added a checkpointed lambda branch-search helper.
- Added CLI flags for checkpoint directory, checkpoint prefix, resume, cheaper scoring bounds, refinement width, progress cadence, and quiet mode.
- Added branch-search tests for checkpoint writing, CLI checkpoint mode, low score-level handling, and numeric checkpoint resume order.
- Regenerated the checkpointed `GF(7)` smoke report and checkpoint artifacts.
- Created [[wiki/m23-belyi-gf7-overnight-branch-runner]].
- Updated [[index]], [[dashboards/llm-wiki-dashboard]], [[wiki/m23-belyi-gf7-lambda-branch-search-report]], and [[wiki/m23-elkies-finite-field-solver]].

## Result

- Smoke run status: partial.
- Smoke run best prefix: `[4, 5]`.
- Smoke run best lambda: 279.
- Smoke run reconstruction score: 7/25 unique coefficients.
- The runner is ready for a longer unattended local run with checkpoints and resume.

## Privacy Filtering

- No sensitive or private material was included.

## Follow-Up

- Run the overnight command and inspect `gf7-overnight-summary.json`.
- If a complete reconstruction appears, verify the exact identity and export the resulting degree-23 polynomial for Magma/GAP verification.
