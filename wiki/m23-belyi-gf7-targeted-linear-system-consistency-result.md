---
type: wiki-page
status: active
created: 2026-05-23
last_confirmed: 2026-05-23
confidence: 0.82
quality_score: 0.88
sensitivity: internal
sources:
  - "[[wiki/m23-belyi-gf7-targeted-linear-consistency-result]]"
  - "[[experiments/m23/reports/gf7-branch-search/gf7-targeted-linear-system-consistency-summary]]"
entities:
  - "[[entities/projects/m23-proof-factory]]"
  - "[[entities/concepts/belyi-map]]"
  - "[[entities/concepts/galois-candidate-search]]"
relationships:
  - target: "[[wiki/m23-belyi-gf7-targeted-linear-consistency-result]]"
    type: "supersedes"
    confidence: 0.84
    note: "Re-ranks the targeted frontier after penalizing full linear-system conflicts."
  - target: "[[wiki/m23-belyi-consistency-scoring-runner]]"
    type: "supports"
    confidence: 0.87
    note: "Motivated adding low-degree nonlinear Groebner checks to the scorer."
supersedes:
  - "[[wiki/m23-belyi-gf7-targeted-linear-consistency-result]]"
superseded_by: []
review_after: 2026-06-23
---

# M23 Belyi GF(7) Targeted Linear-System Consistency Result

## Summary

The targeted linear-system consistency rescore completed with status `partial`. It found a branch with 20/25 unique rational reconstructions and no detected hard, single-variable linear, or full linear-system contradictions.

A post-run nonlinear consistency diagnostic still ruled out the branch. After solving the linear subsystem, the first four low-degree residual equations have a Groebner basis containing `1`, so the remaining unresolved variables cannot satisfy the exact equations.

## Result

| statistic | value |
| --- | ---: |
| prime | 7 |
| levels | 13 |
| depth | 12 |
| beam width | 35 |
| evaluated branches | 791 |
| initial prefix | `[3, 2, 0, 5, 0, 0, 0]` |
| best prefix | `[3, 2, 0, 5, 0, 0, 0, 2, 3, 2, 5, 1]` |
| best lambda | 24425473967 |
| best reconstruction | 20/25 unique coefficients |
| hard contradictions | 0 |
| single-variable linear conflicts | 0 |
| full linear-system conflicts | 0 |
| symbolic constraints | 46 |
| status | partial |

## Remaining Unknowns

- `p3[0]`
- `p3[1]`
- `p4[0]`
- `p4[3]`
- `p8[6]`

## Post-Run Nonlinear Check

The linear equations first force:

```text
p3_0 = -46861035124/44146546011
p4_0 = 30065434571/88293092022
```

After substituting those values, the reduced nonlinear residuals over `p3_1`, `p4_3`, and `p8_6` are inconsistent. A Groebner basis computed from the first four low-degree reduced residuals contains `1`.

This motivated another scorer upgrade: branch scoring now penalizes low-degree Groebner contradictions after hard, linear-system, and single-variable linear conflicts, but before raw unique coefficient count.

## Next Run

Rerun the targeted frontier with the low-degree Groebner-aware scorer and a fresh checkpoint directory:

```powershell
.\.venv\Scripts\python experiments/m23/scripts/search_lambda_branches.py --prime 7 --levels 13 --depth 12 --beam-width 35 --max-numerator 250000 --max-denominator 250000 --score-levels 10 --score-max-numerator 50000 --score-max-denominator 50000 --refine-all --score-consistency --consistency-min-unique 20 --initial-prefix 3,2,0,5,0,0,0 --checkpoint-dir experiments/m23/reports/gf7-branch-search/checkpoints-targeted-groebner-consistency --checkpoint-prefix gf7-targeted-groebner-consistency --progress-every 10 --seed-json experiments/m23/reports/gf7-exhaustive/gf7-normalized-summary.json --out experiments/m23/reports/gf7-branch-search/gf7-targeted-groebner-consistency-summary.json --markdown-out experiments/m23/reports/gf7-branch-search/gf7-targeted-groebner-consistency-summary.md --title "M23 Belyi GF(7) Targeted Groebner Consistency Rescore"
```

## Interpretation

This was another false shadow. It was useful because it exposed the next failure mode: a branch can pass constant, single-variable linear, and full linear-system checks while still being impossible once low-degree nonlinear residuals are considered.
