---
type: ingest-log
status: active
created: 2026-05-25
last_confirmed: 2026-05-25
confidence: 0.84
quality_score: 0.86
sensitivity: internal
sources:
  - "[[experiments/m23/reports/gf7-branch-search/gf7-targeted-groebner6-clean-continuation-summary]]"
  - "[[wiki/m23-belyi-gf7-clean-continuation-result]]"
entities:
  - "[[entities/projects/m23-proof-factory]]"
  - "[[entities/concepts/belyi-map]]"
  - "[[entities/concepts/galois-candidate-search]]"
relationships:
  - target: "[[wiki/m23-belyi-gf7-clean-continuation-result]]"
    type: "supports"
    confidence: 0.90
    note: "Records the one-digit continuation of the clean min16 frontier."
supersedes: []
superseded_by: []
review_after: 2026-06-25
---

# Ingest Log: M23 Belyi GF(7) Clean Continuation Result

## Source

- Local report: `experiments/m23/reports/gf7-branch-search/gf7-targeted-groebner6-clean-continuation-summary.json`
- Markdown report: `experiments/m23/reports/gf7-branch-search/gf7-targeted-groebner6-clean-continuation-summary.md`

## Actions

- Recorded the clean-frontier continuation result.
- Noted that the run evaluated `28` branches because four length-12 prefixes were each extended by one base-7 digit.
- Recorded that the best branch dropped to `5 / 25` unique rational reconstructions at precision `7^14`.
- Marked the clean lower-unique frontier as weakened rather than continued.

## Privacy

No sensitive material was copied into the synthesized page.

## Follow-Up

Prefer checking quarantined timeout branches with stronger algebra or changing search strategy over continuing this weakened frontier directly.
