---
type: wiki-page
status: active
created: 2026-05-23
last_confirmed: 2026-05-23
confidence: 0.81
quality_score: 0.87
sensitivity: internal
sources:
  - "[[wiki/m23-belyi-gf7-targeted-consistency-result]]"
  - "[[experiments/m23/reports/gf7-branch-search/gf7-targeted-linear-consistency-summary]]"
entities:
  - "[[entities/projects/m23-proof-factory]]"
  - "[[entities/concepts/belyi-map]]"
  - "[[entities/concepts/galois-candidate-search]]"
relationships:
  - target: "[[wiki/m23-belyi-gf7-targeted-consistency-result]]"
    type: "supersedes"
    confidence: 0.84
    note: "Re-ranks the targeted frontier after penalizing single-variable linear conflicts."
  - target: "[[wiki/m23-belyi-consistency-scoring-runner]]"
    type: "supports"
    confidence: 0.86
    note: "Motivated adding full linear-system rank checks to the scorer."
supersedes:
  - "[[wiki/m23-belyi-gf7-targeted-consistency-result]]"
superseded_by: []
review_after: 2026-06-23
---

# M23 Belyi GF(7) Targeted Linear Consistency Result

## Summary

The targeted linear consistency rescore completed with status `partial`. It found a branch with 20/25 unique rational reconstructions, zero hard contradictions, and zero single-variable linear conflicts.

A post-run full linear-system rank check showed that this branch is also inconsistent: the six linear equations among the five unresolved variables have rank `3`, while the augmented system has rank `4`.

## Result

| statistic | value |
| --- | ---: |
| prime | 7 |
| levels | 13 |
| depth | 12 |
| beam width | 35 |
| evaluated branches | 791 |
| initial prefix | `[3, 2, 0, 5, 0, 0, 0]` |
| best prefix | `[3, 2, 0, 5, 0, 0, 0, 5, 6, 4, 5, 0]` |
| best lambda | 11287492488 |
| best reconstruction | 20/25 unique coefficients |
| hard contradictions | 0 |
| single-variable linear conflicts | 0 |
| symbolic constraints | 46 |
| status | partial |

## Remaining Unknowns

- `p2[0]`
- `p4[0]`
- `p7[2]`
- `p7[6]`
- `p8[5]`

## Post-Run Linear-System Check

The full linear subsystem is inconsistent:

| statistic | value |
| --- | ---: |
| linear equations | 6 |
| coefficient rank | 3 |
| augmented rank | 4 |
| linear-system conflicts | 1 |

This motivated another scorer upgrade: branch scoring now penalizes full linear-system inconsistency before single-variable linear conflicts and before unique coefficient count.

## Next Run

Rerun the targeted frontier with the linear-system-aware scorer and a fresh checkpoint directory:

```powershell
.\.venv\Scripts\python experiments/m23/scripts/search_lambda_branches.py --prime 7 --levels 13 --depth 12 --beam-width 35 --max-numerator 250000 --max-denominator 250000 --score-levels 10 --score-max-numerator 50000 --score-max-denominator 50000 --refine-all --score-consistency --consistency-min-unique 20 --initial-prefix 3,2,0,5,0,0,0 --checkpoint-dir experiments/m23/reports/gf7-branch-search/checkpoints-targeted-linear-system-consistency --checkpoint-prefix gf7-targeted-linear-system-consistency --progress-every 10 --seed-json experiments/m23/reports/gf7-exhaustive/gf7-normalized-summary.json --out experiments/m23/reports/gf7-branch-search/gf7-targeted-linear-system-consistency-summary.json --markdown-out experiments/m23/reports/gf7-branch-search/gf7-targeted-linear-system-consistency-summary.md --title "M23 Belyi GF(7) Targeted Linear-System Consistency Rescore"
```

## Interpretation

This was another false shadow, but a valuable one. The scoring ladder is now stricter: unique count, hard residual contradictions, single-variable linear conflicts, and full linear-system rank consistency.
