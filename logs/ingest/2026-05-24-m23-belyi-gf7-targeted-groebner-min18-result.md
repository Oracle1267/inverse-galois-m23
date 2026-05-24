---
type: ingest-log
status: active
created: 2026-05-24
last_confirmed: 2026-05-24
confidence: 0.84
quality_score: 0.84
sensitivity: internal
source: "local targeted Groebner min18 rescore report"
sources:
  - "[[wiki/m23-belyi-gf7-targeted-groebner-consistency-result]]"
  - "[[experiments/m23/reports/gf7-branch-search/gf7-targeted-groebner-consistency-min18-summary]]"
entities:
  - "[[entities/projects/m23-proof-factory]]"
  - "[[entities/concepts/belyi-map]]"
  - "[[entities/concepts/galois-candidate-search]]"
relationships:
  - target: "[[wiki/m23-belyi-gf7-targeted-groebner-min18-result]]"
    type: "supports"
    confidence: 0.88
supersedes: []
superseded_by: []
review_after: 2026-06-24
---

# M23 Belyi GF(7) Targeted Groebner Min18 Result Ingest

## Source

- Source: `experiments/m23/reports/gf7-branch-search/gf7-targeted-groebner-consistency-min18-summary.json`.
- Source kind: local search result and post-run linear-solution residual diagnostic.
- Sensitivity: internal.

## Actions

- Recorded the completed targeted Groebner min18 rescore.
- Identified an apparent clean 19/25 branch.
- Ran a post-run linear-solution residual check showing that the apparent clean branch is impossible.
- Upgraded the consistency scorer to penalize linear-solution residual conflicts.

## Entities Created or Updated

- Updated [[entities/projects/m23-proof-factory]] by recording linear-solution residual consistency as a scoring filter.

## Wiki Pages Created or Updated

- Created [[wiki/m23-belyi-gf7-targeted-groebner-min18-result]].
- Updated [[wiki/m23-belyi-consistency-scoring-runner]].
- Updated [[wiki/m23-elkies-finite-field-solver]].
- Updated [[index]].
- Updated [[dashboards/llm-wiki-dashboard]].

## Privacy Filtering

- No private or credential-like content was included. The report contains mathematical search artifacts and local relative paths only.

## Confidence and Quality Notes

- Confidence is high that the reported 19/25 branch is ruled out after linear-solution substitution.
- Confidence remains exploratory for whether the broader `GF(7)` survivor can still lead to a rational M23 construction.

## Follow-Up

- Rerun the min18 targeted frontier with the upgraded linear-solution residual scorer.
