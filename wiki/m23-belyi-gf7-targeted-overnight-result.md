---
type: wiki-page
status: active
created: 2026-05-23
last_confirmed: 2026-05-23
confidence: 0.80
quality_score: 0.88
sensitivity: internal
sources:
  - "[[wiki/m23-belyi-gf7-targeted-branch-runner]]"
  - "[[experiments/m23/reports/gf7-branch-search/gf7-targeted-overnight-summary]]"
entities:
  - "[[entities/projects/m23-proof-factory]]"
  - "[[entities/concepts/belyi-map]]"
  - "[[entities/concepts/galois-candidate-search]]"
relationships:
  - target: "[[wiki/m23-belyi-gf7-targeted-branch-runner]]"
    type: "supports"
    confidence: 0.86
    note: "Records the completed targeted continuation run."
  - target: "[[wiki/m23-belyi-gf7-overnight-result]]"
    type: "supersedes"
    confidence: 0.82
    note: "Improves the reconstruction signal from 20/25 to 23/25 coefficients."
supersedes:
  - "[[wiki/m23-belyi-gf7-overnight-result]]"
superseded_by: []
review_after: 2026-06-23
---

# M23 Belyi GF(7) Targeted Overnight Result

## Summary

The targeted continuation run completed with status `partial`. It improved the best rational reconstruction signal from 20/25 to 23/25 unique coefficients, but did not produce a complete exact Belyi identity.

The two unresolved entries are `p4[3]` and `p8[7]`. A follow-up symbolic consistency check showed that the current 23 reconstructed coefficients already fail some exact identity coefficients that do not depend on those two unknowns. This means the result is a useful search signal, not a near-proof with only two missing numbers.

## Result

| statistic | value |
| --- | ---: |
| prime | 7 |
| levels | 13 |
| depth | 12 |
| beam width | 35 |
| evaluated branches | 791 |
| initial prefix | `[3, 2, 0, 5, 0, 0, 0]` |
| best prefix | `[3, 2, 0, 5, 0, 0, 0, 6, 4, 2, 0, 0]` |
| best lambda | 760965862 |
| best reconstruction | 23/25 unique coefficients |
| status | partial |

## Remaining Unknowns

- `p4[3]`
- `p8[7]`

## Follow-Up Checks

Wider bounded reconstruction produced ambiguous candidate sets rather than a unique completion:

- Bound 500,000: `p4[3]` had 4 candidates; `p8[7]` had none.
- Bound 1,000,000: `p4[3]` had 12 candidates; `p8[7]` had 10 candidates; no exact pair worked.
- Bound 2,000,000: `p4[3]` had 46 candidates; `p8[7]` had 52 candidates; no exact pair worked.

A symbolic check with `p4[3]` and `p8[7]` as variables found nonzero exact-equation coefficients independent of those variables. Therefore, at least one of the currently unique reconstructed coefficients is likely a false small-rational reconstruction at this lift level and bound.

## Interpretation

The targeted search found a much stronger numerical shadow, but the current scoring function is still too naive: it rewards many unique rational reconstructions even when the resulting partial rational object is already inconsistent with exact equations.

The next search program should add a partial exact-consistency score, or move to deeper lifting and then re-score candidates by whether the unique reconstructed subset survives exact coefficient checks.
