---
type: wiki-page
status: active
created: 2026-05-23
last_confirmed: 2026-05-23
confidence: 0.80
quality_score: 0.88
sensitivity: internal
sources:
  - "[[wiki/m23-belyi-gf7-overnight-branch-runner]]"
  - "[[experiments/m23/reports/gf7-branch-search/gf7-overnight-summary]]"
entities:
  - "[[entities/projects/m23-proof-factory]]"
  - "[[entities/concepts/belyi-map]]"
  - "[[entities/concepts/galois-candidate-search]]"
relationships:
  - target: "[[wiki/m23-belyi-gf7-overnight-branch-runner]]"
    type: "supports"
    confidence: 0.86
    note: "Records the completed unattended branch-search run produced by the runner."
  - target: "[[wiki/m23-belyi-gf7-lambda-branch-search-report]]"
    type: "supersedes"
    confidence: 0.82
    note: "Improves the prior lambda-branch frontier from 16/25 to 20/25 reconstructed coefficients."
supersedes:
  - "[[wiki/m23-belyi-gf7-lambda-branch-search-report]]"
superseded_by: []
review_after: 2026-06-23
---

# M23 Belyi GF(7) Overnight Result

## Summary

The checkpointed overnight `GF(7)` lambda branch search completed its requested depth and did not find a complete rational reconstruction. It improved the best reconstruction signal from 16/25 to 20/25 unique coefficients.

The run also exposed and fixed a reporting issue: the runner had been reporting the last frontier winner as `best`, even when a stronger branch had appeared earlier. The corrected report now records both the best branch seen and the final frontier branch.

## Result

| statistic | value |
| --- | ---: |
| prime | 7 |
| levels | 12 |
| depth | 8 |
| beam width | 25 |
| cheap branches scored | 1,106 |
| best prefix seen | `[3, 2, 0, 5, 0, 0, 0]` |
| best lambda seen | 12130 |
| best reconstruction | 20/25 unique coefficients |
| final frontier prefix | `[3, 2, 0, 5, 0, 2, 0, 0]` |
| final frontier reconstruction | 19/25 unique coefficients |
| status | partial |

## Remaining Unknowns

The five unresolved coefficients in the best reconstruction are:

- `p7[1]`
- `p7[3]`
- `p7[6]`
- `p8[2]`
- `p8[4]`

## Interpretation

This is a meaningful improvement in the computational search, not a solution. The branch with `lambda = 12130` is the strongest current rational-reconstruction signal, but five coefficients remain unresolved under the current lift level and rational bounds.

The cheap scoring pass can prune a branch that scores better under full reconstruction bounds. Future runs should either increase the refinement width enough to refine every child of the beam frontier, or use a more conservative protected-branch rule for strong prior branches.
