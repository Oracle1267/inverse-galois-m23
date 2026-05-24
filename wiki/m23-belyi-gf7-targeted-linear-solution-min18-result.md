---
type: wiki-page
status: active
created: 2026-05-24
last_confirmed: 2026-05-24
confidence: 0.84
quality_score: 0.88
sensitivity: internal
sources:
  - "[[wiki/m23-belyi-gf7-targeted-groebner-min18-result]]"
  - "[[experiments/m23/reports/gf7-branch-search/gf7-targeted-linear-solution-consistency-min18-summary]]"
entities:
  - "[[entities/projects/m23-proof-factory]]"
  - "[[entities/concepts/belyi-map]]"
  - "[[entities/concepts/galois-candidate-search]]"
relationships:
  - target: "[[wiki/m23-belyi-gf7-targeted-groebner-min18-result]]"
    type: "supersedes"
    confidence: 0.84
    note: "Reruns the min18 targeted frontier after adding linear-solution residual scoring."
  - target: "[[wiki/m23-belyi-consistency-scoring-runner]]"
    type: "supports"
    confidence: 0.88
    note: "Motivated raising the low-degree Groebner cap from four to six equations."
supersedes:
  - "[[wiki/m23-belyi-gf7-targeted-groebner-min18-result]]"
superseded_by: []
review_after: 2026-06-24
---

# M23 Belyi GF(7) Targeted Linear-Solution Min18 Result

## Summary

The targeted min18 rescore with linear-solution residual checking completed with status `partial`. It left one apparently clean scored branch at 18/25 unique coefficients.

A post-run larger Groebner probe ruled out that branch. The default scorer had checked four low-degree equations; checking six low-degree equations produced a Groebner basis containing `1`.

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
| best prefix | `[3, 2, 0, 5, 0, 0, 0, 1, 2, 3, 3, 2]` |
| best lambda | 34548464523 |
| best reconstruction | 18/25 unique coefficients |
| reported hard contradictions | 0 |
| reported linear-system conflicts | 0 |
| reported single-variable linear conflicts | 0 |
| reported linear-solution conflicts | 0 |
| reported low-degree Groebner conflicts | 0 |
| post-run six-equation Groebner conflicts | 1 |
| status | partial |

## Remaining Unknowns

- `p2[0]`
- `p4[0]`
- `p4[2]`
- `p7[1]`
- `p8[1]`
- `p8[2]`
- `p8[7]`

## Post-Run Groebner Probe

The branch has seven unresolved variables and a consistent but underdetermined linear subsystem:

| statistic | value |
| --- | ---: |
| linear equations | 4 |
| linear rank | 3 |
| augmented rank | 3 |

The four-equation Groebner check did not prove inconsistency. A six-equation low-degree Groebner check did prove inconsistency, so the scorer cap was raised from four to six equations.

## Next Run

Rerun the min18 targeted frontier with the six-equation Groebner scorer:

```powershell
.\.venv\Scripts\python experiments/m23/scripts/search_lambda_branches.py --prime 7 --levels 13 --depth 12 --beam-width 35 --max-numerator 250000 --max-denominator 250000 --score-levels 10 --score-max-numerator 50000 --score-max-denominator 50000 --refine-all --score-consistency --consistency-min-unique 18 --initial-prefix 3,2,0,5,0,0,0 --checkpoint-dir experiments/m23/reports/gf7-branch-search/checkpoints-targeted-groebner6-consistency-min18 --checkpoint-prefix gf7-targeted-groebner6-consistency-min18 --progress-every 10 --seed-json experiments/m23/reports/gf7-exhaustive/gf7-normalized-summary.json --out experiments/m23/reports/gf7-branch-search/gf7-targeted-groebner6-consistency-min18-summary.json --markdown-out experiments/m23/reports/gf7-branch-search/gf7-targeted-groebner6-consistency-min18-summary.md --title "M23 Belyi GF(7) Targeted Groebner6 Consistency Min18 Rescore"
```

## Interpretation

This targeted prefix keeps producing increasingly subtle false shadows. The useful outcome is that the search now rejects more of them automatically. If the six-equation Groebner run leaves no clean branch, the next strategic move is likely to widen or restart from an earlier prefix rather than continue tightening this narrow branch.
