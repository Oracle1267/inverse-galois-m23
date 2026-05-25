---
type: wiki-page
status: active
created: 2026-05-25
last_confirmed: 2026-05-25
confidence: 0.84
quality_score: 0.86
sensitivity: internal
sources:
  - "[[wiki/m23-belyi-gf7-targeted-groebner6-min16-result]]"
  - "[[experiments/m23/reports/gf7-branch-search/gf7-targeted-groebner6-clean-continuation-summary]]"
entities:
  - "[[entities/projects/m23-proof-factory]]"
  - "[[entities/concepts/belyi-map]]"
  - "[[entities/concepts/galois-candidate-search]]"
relationships:
  - target: "[[wiki/m23-belyi-gf7-targeted-groebner6-min16-result]]"
    type: "depends-on"
    confidence: 0.88
    note: "This run continued the four clean final branches from the min16 rescore by one additional base-7 digit."
  - target: "[[wiki/m23-belyi-consistency-scoring-runner]]"
    type: "supports"
    confidence: 0.82
    note: "Shows that the clean lower-unique frontier did not persist at the next p-adic precision."
supersedes: []
superseded_by: []
review_after: 2026-06-25
---

# M23 Belyi GF(7) Clean Continuation Result

## Summary

The clean-frontier continuation from four min16 prefixes completed quickly because it only extended each length-12 prefix by one base-7 digit. It evaluated `28` branches, exactly `4 x 7`.

The result is a negative signal for this frontier. At precision `7^14`, the best branch reconstructed only `5 / 25` coefficients, far below the `16 / 25` threshold needed to run symbolic consistency scoring. The previous clean `16 / 25` signal therefore did not persist under one more digit of p-adic precision.

## Result Table

| Field | Value |
| --- | --- |
| Prime | `7` |
| Levels | `14` |
| Depth | `13` |
| Beam width | `35` |
| Initial prefixes | `4` |
| Evaluated branches | `28` |
| Best prefix | `[3, 2, 0, 5, 0, 0, 0, 0, 5, 1, 6, 4, 2]` |
| Best lambda | `261491385490` |
| Best reconstruction | `5 / 25` unique coefficients |
| Consistency checks | Not run; no branch reached `16 / 25` |
| Status | `partial` |

## Interpretation

This does not mathematically disprove the broader M23 Belyi approach. It does make this particular clean lower-unique frontier much less promising. A genuine rational lift should normally become more stable, not lose almost all unique rational reconstructions after one more p-adic digit under the same rational bounds.

The next search should either revisit quarantined timeout branches with a stronger algebra system, or change the search strategy rather than continuing deeper on this weakened frontier.
