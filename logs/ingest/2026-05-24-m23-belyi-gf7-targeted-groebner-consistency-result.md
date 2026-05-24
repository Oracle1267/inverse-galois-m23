---
type: ingest-log
status: active
created: 2026-05-24
last_confirmed: 2026-05-24
confidence: 0.83
quality_score: 0.83
sensitivity: internal
source: "local targeted Groebner consistency rescore report"
sources:
  - "[[wiki/m23-belyi-gf7-targeted-linear-system-consistency-result]]"
  - "[[experiments/m23/reports/gf7-branch-search/gf7-targeted-groebner-consistency-summary]]"
entities:
  - "[[entities/projects/m23-proof-factory]]"
  - "[[entities/concepts/belyi-map]]"
  - "[[entities/concepts/galois-candidate-search]]"
relationships:
  - target: "[[wiki/m23-belyi-gf7-targeted-groebner-consistency-result]]"
    type: "supports"
    confidence: 0.87
supersedes: []
superseded_by: []
review_after: 2026-06-24
---

# M23 Belyi GF(7) Targeted Groebner Consistency Result Ingest

## Source

- Source: `experiments/m23/reports/gf7-branch-search/gf7-targeted-groebner-consistency-summary.json`.
- Source kind: local search result.
- Sensitivity: internal.

## Actions

- Recorded the completed targeted Groebner consistency rescore.
- Confirmed that the previous 20/25 branch is now marked with a Groebner conflict during the run.
- Counted zero clean scored candidates among the kept frontier.
- Identified earlier consistency scoring as the next local search move.

## Entities Created or Updated

- Updated [[entities/projects/m23-proof-factory]] by recording the current targeted `GF(7)` frontier as contradiction-saturated at the current threshold.

## Wiki Pages Created or Updated

- Created [[wiki/m23-belyi-gf7-targeted-groebner-consistency-result]].
- Updated [[wiki/m23-belyi-consistency-scoring-runner]].
- Updated [[wiki/m23-elkies-finite-field-solver]].
- Updated [[index]].
- Updated [[dashboards/llm-wiki-dashboard]].

## Privacy Filtering

- No private or credential-like content was included. The report contains mathematical search artifacts and local relative paths only.

## Confidence and Quality Notes

- Confidence is high that the run did not find a solution and that the kept scored frontier had no clean candidates.
- Confidence remains exploratory for whether the broader `GF(7)` survivor can still lead to a rational M23 construction.

## Follow-Up

- Rerun the targeted frontier with `--consistency-min-unique 18`.
