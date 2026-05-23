---
type: ingest-log
status: active
created: 2026-05-23
last_confirmed: 2026-05-23
confidence: 0.80
quality_score: 0.86
sensitivity: internal
source: "M23 GF(7) targeted lambda branch runner"
sources:
  - "[[wiki/m23-belyi-gf7-overnight-result]]"
  - "[[experiments/m23/reports/gf7-branch-search/gf7-targeted-smoke]]"
entities:
  - "[[entities/projects/m23-proof-factory]]"
  - "[[entities/concepts/belyi-map]]"
relationships:
  - target: "[[wiki/m23-belyi-gf7-targeted-branch-runner]]"
    type: "supports"
    confidence: 0.86
supersedes: []
superseded_by: []
review_after: 2026-06-23
---

# M23 Belyi GF(7) Targeted Runner Log

## Source

- Source: local code changes, tests, and generated targeted smoke artifacts.
- Source kind: generated tooling and reports.
- Sensitivity: internal.

## Actions

- Added `--initial-prefix` to start branch search from a known lambda digit prefix.
- Added `--refine-all` to fully reconstruct every child in the active frontier before beam pruning.
- Added tests for initial-prefix search, full refinement, and CLI argument support.
- Ran a small targeted `GF(7)` smoke search from prefix `[3, 2, 0, 5, 0, 0, 0]`.
- Created [[wiki/m23-belyi-gf7-targeted-branch-runner]].
- Updated [[index]], [[dashboards/llm-wiki-dashboard]], [[wiki/m23-elkies-finite-field-solver]], and [[wiki/m23-belyi-gf7-overnight-result]].

## Result

- The new controls are ready for an unattended targeted overnight search.
- Smoke run status: partial.
- Smoke run evaluated branches: 7.

## Privacy Filtering

- No sensitive or private material was included.

## Follow-Up

- Run the targeted overnight command and compare its best reconstruction score against the current 20/25 branch.
