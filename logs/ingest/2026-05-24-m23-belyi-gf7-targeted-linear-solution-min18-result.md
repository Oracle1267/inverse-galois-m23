---
type: ingest-log
status: active
created: 2026-05-24
last_confirmed: 2026-05-24
confidence: 0.84
quality_score: 0.84
sensitivity: internal
source: "local targeted linear-solution min18 rescore report"
sources:
  - "[[wiki/m23-belyi-gf7-targeted-groebner-min18-result]]"
  - "[[experiments/m23/reports/gf7-branch-search/gf7-targeted-linear-solution-consistency-min18-summary]]"
entities:
  - "[[entities/projects/m23-proof-factory]]"
  - "[[entities/concepts/belyi-map]]"
  - "[[entities/concepts/galois-candidate-search]]"
relationships:
  - target: "[[wiki/m23-belyi-gf7-targeted-linear-solution-min18-result]]"
    type: "supports"
    confidence: 0.88
supersedes: []
superseded_by: []
review_after: 2026-06-24
---

# M23 Belyi GF(7) Targeted Linear-Solution Min18 Result Ingest

## Source

- Source: `experiments/m23/reports/gf7-branch-search/gf7-targeted-linear-solution-consistency-min18-summary.json`.
- Source kind: local search result and post-run larger Groebner diagnostic.
- Sensitivity: internal.

## Actions

- Recorded the completed targeted linear-solution min18 rescore.
- Identified one apparent clean 18/25 branch.
- Ran a post-run six-equation Groebner probe showing that the apparent clean branch is impossible.
- Raised the default low-degree Groebner scorer cap from four to six equations.

## Entities Created or Updated

- Updated [[entities/projects/m23-proof-factory]] by recording six-equation low-degree Groebner consistency as the current scorer.

## Wiki Pages Created or Updated

- Created [[wiki/m23-belyi-gf7-targeted-linear-solution-min18-result]].
- Updated [[wiki/m23-belyi-consistency-scoring-runner]].
- Updated [[wiki/m23-elkies-finite-field-solver]].
- Updated [[index]].
- Updated [[dashboards/llm-wiki-dashboard]].

## Privacy Filtering

- No private or credential-like content was included. The report contains mathematical search artifacts and local relative paths only.

## Confidence and Quality Notes

- Confidence is high that the reported 18/25 branch is ruled out by the six-equation Groebner probe.
- Confidence remains exploratory for whether the broader `GF(7)` survivor can still lead to a rational M23 construction.

## Follow-Up

- Rerun the min18 targeted frontier with the upgraded six-equation Groebner scorer.
