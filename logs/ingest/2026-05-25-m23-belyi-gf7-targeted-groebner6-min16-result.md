---
type: ingest-log
status: active
created: 2026-05-25
last_confirmed: 2026-05-25
confidence: 0.86
quality_score: 0.88
sensitivity: internal
sources:
  - "[[experiments/m23/reports/gf7-branch-search/gf7-targeted-groebner6-consistency-min16-summary]]"
  - "[[wiki/m23-belyi-gf7-targeted-groebner6-min16-result]]"
entities:
  - "[[entities/projects/m23-proof-factory]]"
  - "[[entities/concepts/belyi-map]]"
  - "[[entities/concepts/galois-candidate-search]]"
relationships:
  - target: "[[wiki/m23-belyi-gf7-targeted-groebner6-min16-result]]"
    type: "supports"
    confidence: 0.90
    note: "Records the completed min16 targeted six-equation Groebner rescore."
supersedes: []
superseded_by: []
review_after: 2026-06-25
---

# Ingest Log: M23 Belyi GF(7) Targeted Groebner6 Min16 Result

## Source

- Local report: `experiments/m23/reports/gf7-branch-search/gf7-targeted-groebner6-consistency-min16-summary.json`
- Markdown report: `experiments/m23/reports/gf7-branch-search/gf7-targeted-groebner6-consistency-min16-summary.md`

## Actions

- Recorded that the min16 targeted six-equation Groebner rescore completed with status `partial`.
- Created [[wiki/m23-belyi-gf7-targeted-groebner6-min16-result]].
- Identified four clean final scored branches, led by prefix `[3, 2, 0, 5, 0, 0, 0, 0, 5, 1, 6, 4]` and lambda `67713364676`.
- Recorded three Groebner timeout candidates as quarantined rather than rejected.
- Updated the continuation plan to branch from clean lower-unique candidates instead of high-unique contradictory candidates.

## Privacy

No credentials, private conversations, or PII were copied into the synthesized page. The content is internal mathematical experiment metadata.

## Follow-Up

Run the clean-frontier continuation at `levels 14`, `depth 13`, `beam-width 35`, and `consistency-min-unique 16`.
