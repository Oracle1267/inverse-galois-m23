---
type: ingest-log
status: active
created: 2026-05-23
last_confirmed: 2026-05-23
confidence: 0.80
quality_score: 0.86
sensitivity: internal
source: "M23 GF(7) targeted overnight branch-search result"
sources:
  - "[[wiki/m23-belyi-gf7-targeted-branch-runner]]"
  - "[[experiments/m23/reports/gf7-branch-search/gf7-targeted-overnight-summary]]"
entities:
  - "[[entities/projects/m23-proof-factory]]"
  - "[[entities/concepts/belyi-map]]"
relationships:
  - target: "[[wiki/m23-belyi-gf7-targeted-overnight-result]]"
    type: "supports"
    confidence: 0.86
supersedes: []
superseded_by: []
review_after: 2026-06-23
---

# M23 Belyi GF(7) Targeted Overnight Result Log

## Source

- Source: completed local targeted overnight branch-search report.
- Source kind: generated JSON and Markdown reports, plus local follow-up reconstruction checks.
- Sensitivity: internal.

## Actions

- Inspected `gf7-targeted-overnight-summary`.
- Ran wider reconstruction checks on the two unresolved coefficients.
- Ran a symbolic consistency check with `p4[3]` and `p8[7]` treated as variables.
- Created [[wiki/m23-belyi-gf7-targeted-overnight-result]].
- Updated [[index]], [[dashboards/llm-wiki-dashboard]], [[wiki/m23-belyi-gf7-targeted-branch-runner]], and [[wiki/m23-elkies-finite-field-solver]].

## Result

- No complete rational reconstruction was found.
- Best branch: prefix `[3, 2, 0, 5, 0, 0, 0, 6, 4, 2, 0, 0]`, lambda `760965862`.
- Best reconstruction score: 23/25 unique coefficients.
- Remaining unresolved coefficients: `p4[3]`, `p8[7]`.
- Wider candidate enumeration up to bound 2,000,000 did not produce an exact completion.
- Symbolic consistency check indicated that the current unique rational reconstructions are not jointly exact.

## Privacy Filtering

- No sensitive or private material was included.

## Follow-Up

- Add a partial exact-consistency score before running another broad search.
- Consider deeper lifting with stricter exact-equation consistency checks.
