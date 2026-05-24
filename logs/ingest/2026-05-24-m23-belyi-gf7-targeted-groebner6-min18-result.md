---
type: ingest-log
status: active
created: 2026-05-24
last_confirmed: 2026-05-24
confidence: 0.85
quality_score: 0.84
sensitivity: internal
source: "local targeted Groebner6 min18 rescore report"
sources:
  - "[[wiki/m23-belyi-gf7-targeted-linear-solution-min18-result]]"
  - "[[experiments/m23/reports/gf7-branch-search/gf7-targeted-groebner6-consistency-min18-summary]]"
entities:
  - "[[entities/projects/m23-proof-factory]]"
  - "[[entities/concepts/belyi-map]]"
  - "[[entities/concepts/galois-candidate-search]]"
relationships:
  - target: "[[wiki/m23-belyi-gf7-targeted-groebner6-min18-result]]"
    type: "supports"
    confidence: 0.88
supersedes: []
superseded_by: []
review_after: 2026-06-24
---

# M23 Belyi GF(7) Targeted Groebner6 Min18 Result Ingest

## Source

- Source: `experiments/m23/reports/gf7-branch-search/gf7-targeted-groebner6-consistency-min18-summary.json`.
- Source kind: local search result.
- Sensitivity: internal.

## Actions

- Recorded the completed targeted Groebner6 min18 rescore.
- Confirmed the run found no solution.
- Counted zero clean scored candidates among the kept frontier.
- Identified a min16 rerun as the next local test before widening the search.

## Entities Created or Updated

- Updated [[entities/projects/m23-proof-factory]] by recording the current targeted prefix as contradiction-saturated under the six-equation Groebner scorer at min18.

## Wiki Pages Created or Updated

- Created [[wiki/m23-belyi-gf7-targeted-groebner6-min18-result]].
- Updated [[wiki/m23-belyi-consistency-scoring-runner]].
- Updated [[wiki/m23-elkies-finite-field-solver]].
- Updated [[index]].
- Updated [[dashboards/llm-wiki-dashboard]].

## Privacy Filtering

- No private or credential-like content was included. The report contains mathematical search artifacts and local relative paths only.

## Confidence and Quality Notes

- Confidence is high that this exact targeted min18 frontier has no clean scored candidate under the current scorer.
- Confidence remains exploratory for whether a lower threshold, wider branch, or different survivor can still lead to a rational M23 construction.

## Follow-Up

- Rerun the targeted frontier with `--consistency-min-unique 16`.
