---
type: ingest-log
status: active
created: 2026-05-23
last_confirmed: 2026-05-23
confidence: 0.81
quality_score: 0.82
sensitivity: internal
source: "local targeted linear consistency rescore report"
sources:
  - "[[wiki/m23-belyi-gf7-targeted-consistency-result]]"
  - "[[experiments/m23/reports/gf7-branch-search/gf7-targeted-linear-consistency-summary]]"
entities:
  - "[[entities/projects/m23-proof-factory]]"
  - "[[entities/concepts/belyi-map]]"
  - "[[entities/concepts/galois-candidate-search]]"
relationships:
  - target: "[[wiki/m23-belyi-gf7-targeted-linear-consistency-result]]"
    type: "supports"
    confidence: 0.86
supersedes: []
superseded_by: []
review_after: 2026-06-23
---

# M23 Belyi GF(7) Targeted Linear Consistency Result Ingest

## Source

- Source: `experiments/m23/reports/gf7-branch-search/gf7-targeted-linear-consistency-summary.json`.
- Source kind: local search result and post-run linear-system diagnostic.
- Sensitivity: internal.

## Actions

- Recorded the completed targeted linear consistency rescore.
- Identified a 20/25 branch with no hard contradictions and no single-variable linear conflicts.
- Ran a post-run rank check showing the branch's full linear subsystem is inconsistent.
- Upgraded the consistency scorer to penalize full linear-system conflicts.

## Entities Created or Updated

- Updated [[entities/projects/m23-proof-factory]] by adding full linear-system consistency as a scoring filter.

## Wiki Pages Created or Updated

- Created [[wiki/m23-belyi-gf7-targeted-linear-consistency-result]].
- Updated [[wiki/m23-belyi-consistency-scoring-runner]].
- Updated [[wiki/m23-elkies-finite-field-solver]].
- Updated [[index]].
- Updated [[dashboards/llm-wiki-dashboard]].

## Privacy Filtering

- No private or credential-like content was included. The report contains mathematical search artifacts and local relative paths only.

## Confidence and Quality Notes

- Confidence is high that the reported branch is ruled out by its linear subsystem.
- Confidence remains exploratory for the broader M23 search.

## Follow-Up

- Rerun the targeted frontier with the upgraded linear-system-aware scorer.
