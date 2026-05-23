---
type: ingest-log
status: active
created: 2026-05-23
last_confirmed: 2026-05-23
confidence: 0.80
quality_score: 0.86
sensitivity: internal
source: "M23 GF(7) overnight lambda branch-search result"
sources:
  - "[[wiki/m23-belyi-gf7-overnight-branch-runner]]"
  - "[[experiments/m23/reports/gf7-branch-search/gf7-overnight-summary]]"
entities:
  - "[[entities/projects/m23-proof-factory]]"
  - "[[entities/concepts/belyi-map]]"
relationships:
  - target: "[[wiki/m23-belyi-gf7-overnight-result]]"
    type: "supports"
    confidence: 0.86
supersedes: []
superseded_by: []
review_after: 2026-06-23
---

# M23 Belyi GF(7) Overnight Result Log

## Source

- Source: completed local overnight branch-search report.
- Source kind: generated JSON and Markdown reports.
- Sensitivity: internal.

## Actions

- Inspected the completed `gf7-overnight-summary` report.
- Identified that the top-level `best` field was reporting the final frontier winner rather than the strongest branch seen during the run.
- Added best-seen tracking and a regression test to the branch-search runner.
- Regenerated the overnight JSON and Markdown reports from the completed history without rerunning the expensive search.
- Created [[wiki/m23-belyi-gf7-overnight-result]].
- Updated [[index]], [[wiki/m23-belyi-gf7-overnight-branch-runner]], and [[wiki/m23-belyi-gf7-lambda-branch-search-report]].

## Result

- No complete rational reconstruction was found.
- Best branch seen: prefix `[3, 2, 0, 5, 0, 0, 0]`, lambda `12130`.
- Best reconstruction score: 20/25 unique coefficients.
- Remaining unresolved coefficients: `p7[1]`, `p7[3]`, `p7[6]`, `p8[2]`, `p8[4]`.

## Privacy Filtering

- No sensitive or private material was included.

## Follow-Up

- Run a safer wider-refinement search so promising branches are less likely to be pruned by cheap scoring.
- Consider a targeted reconstruction pass focused on the five unresolved coefficients.
