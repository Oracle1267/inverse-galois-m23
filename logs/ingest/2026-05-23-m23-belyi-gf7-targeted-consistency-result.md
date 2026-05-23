---
type: ingest-log
status: active
created: 2026-05-23
last_confirmed: 2026-05-23
confidence: 0.80
quality_score: 0.82
sensitivity: internal
source: "local targeted consistency rescore report"
sources:
  - "[[wiki/m23-belyi-consistency-scoring-runner]]"
  - "[[experiments/m23/reports/gf7-branch-search/gf7-targeted-consistency-summary]]"
entities:
  - "[[entities/projects/m23-proof-factory]]"
  - "[[entities/concepts/belyi-map]]"
  - "[[entities/concepts/galois-candidate-search]]"
relationships:
  - target: "[[wiki/m23-belyi-gf7-targeted-consistency-result]]"
    type: "supports"
    confidence: 0.86
supersedes: []
superseded_by: []
review_after: 2026-06-23
---

# M23 Belyi GF(7) Targeted Consistency Result Ingest

## Source

- Source: `experiments/m23/reports/gf7-branch-search/gf7-targeted-consistency-summary.json`.
- Source kind: local search result and post-run symbolic diagnostic.
- Sensitivity: internal.

## Actions

- Recorded the completed targeted consistency rescore.
- Identified a new best hard-contradiction-scored prefix with 22/25 unique coefficients and zero hard contradictions.
- Ran a post-run linear symbolic check showing the best prefix forces incompatible exact values for `p3[0]`.
- Updated the consistency scorer to penalize linear symbolic conflicts.

## Entities Created or Updated

- Updated [[entities/projects/m23-proof-factory]] by adding a stricter branch-scoring filter.

## Wiki Pages Created or Updated

- Created [[wiki/m23-belyi-gf7-targeted-consistency-result]].
- Updated [[wiki/m23-belyi-consistency-scoring-runner]].
- Updated [[wiki/m23-elkies-finite-field-solver]].
- Updated [[index]].
- Updated [[dashboards/llm-wiki-dashboard]].

## Privacy Filtering

- No private or credential-like content was included. The report contains mathematical search artifacts and local relative paths only.

## Confidence and Quality Notes

- Confidence is high that the reported run completed and that the top branch has a linear symbolic conflict.
- Confidence remains exploratory for the broader M23 search because this is still a finite-field/lift heuristic path.

## Follow-Up

- Rerun the targeted frontier with the upgraded linear-conflict-aware scorer.
