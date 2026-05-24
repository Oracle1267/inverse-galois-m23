---
type: wiki-page
status: active
created: 2026-05-24
last_confirmed: 2026-05-24
confidence: 0.84
quality_score: 0.88
sensitivity: internal
sources:
  - "[[wiki/m23-belyi-gf7-targeted-groebner-consistency-result]]"
  - "[[experiments/m23/reports/gf7-branch-search/gf7-targeted-groebner-consistency-min18-summary]]"
entities:
  - "[[entities/projects/m23-proof-factory]]"
  - "[[entities/concepts/belyi-map]]"
  - "[[entities/concepts/galois-candidate-search]]"
relationships:
  - target: "[[wiki/m23-belyi-gf7-targeted-groebner-consistency-result]]"
    type: "supersedes"
    confidence: 0.84
    note: "Scores consistency earlier by lowering the threshold from 20 to 18 unique coefficients."
  - target: "[[wiki/m23-belyi-consistency-scoring-runner]]"
    type: "supports"
    confidence: 0.88
    note: "Motivated adding linear-solution residual checking to the scorer."
supersedes:
  - "[[wiki/m23-belyi-gf7-targeted-groebner-consistency-result]]"
superseded_by: []
review_after: 2026-06-24
---

# M23 Belyi GF(7) Targeted Groebner Min18 Result

## Summary

The targeted Groebner rescore with `--consistency-min-unique 18` completed with status `partial`. It initially found a 19/25 branch with no hard, linear-system, single-variable linear, or low-degree Groebner conflicts.

A post-run linear-solution residual check ruled out that apparent clean branch. The linear subsystem uniquely determines all six unresolved coefficients; substituting those values back into the full residual system leaves 39 nonzero constant contradictions.

## Result

| statistic | value |
| --- | ---: |
| prime | 7 |
| levels | 13 |
| depth | 12 |
| beam width | 35 |
| consistency min unique | 18 |
| evaluated branches | 791 |
| initial prefix | `[3, 2, 0, 5, 0, 0, 0]` |
| best prefix | `[3, 2, 0, 5, 0, 0, 0, 3, 6, 5, 0, 5]` |
| best lambda | 70878240425 |
| best reconstruction | 19/25 unique coefficients |
| reported hard contradictions | 0 |
| reported linear-system conflicts | 0 |
| reported single-variable linear conflicts | 0 |
| reported low-degree Groebner conflicts | 0 |
| post-run linear-solution residual conflicts | 39 |
| status | partial |

## Remaining Unknowns

- `p3[0]`
- `p3[1]`
- `p3[2]`
- `p4[0]`
- `p7[5]`
- `p8[6]`

## Post-Run Linear-Solution Check

The linear subsystem has rank `6` across the six unresolved variables, so it uniquely solves the remaining coefficients. That solved completion does not satisfy the nonlinear identity residuals.

This motivated another scorer upgrade: when a linear subsystem uniquely solves all unresolved variables, the scorer substitutes the solution into every symbolic residual. Any remaining nonzero constant residual is treated as a `linear_solution_conflict`.

## Next Run

Rerun the min18 targeted frontier with the linear-solution residual scorer:

```powershell
.\.venv\Scripts\python experiments/m23/scripts/search_lambda_branches.py --prime 7 --levels 13 --depth 12 --beam-width 35 --max-numerator 250000 --max-denominator 250000 --score-levels 10 --score-max-numerator 50000 --score-max-denominator 50000 --refine-all --score-consistency --consistency-min-unique 18 --initial-prefix 3,2,0,5,0,0,0 --checkpoint-dir experiments/m23/reports/gf7-branch-search/checkpoints-targeted-linear-solution-consistency-min18 --checkpoint-prefix gf7-targeted-linear-solution-consistency-min18 --progress-every 10 --seed-json experiments/m23/reports/gf7-exhaustive/gf7-normalized-summary.json --out experiments/m23/reports/gf7-branch-search/gf7-targeted-linear-solution-consistency-min18-summary.json --markdown-out experiments/m23/reports/gf7-branch-search/gf7-targeted-linear-solution-consistency-min18-summary.md --title "M23 Belyi GF(7) Targeted Linear-Solution Consistency Min18 Rescore"
```

## Interpretation

The min18 threshold helped the beam escape the previously contradiction-saturated 20/25 branch, but the new 19/25 branch was still a false shadow. The search loop remains productive because each near miss is being converted into an automated rejection rule.
