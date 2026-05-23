---
type: wiki-page
status: active
created: 2026-05-23
last_confirmed: 2026-05-23
confidence: 0.80
quality_score: 0.87
sensitivity: internal
sources:
  - "[[wiki/m23-belyi-consistency-scoring-runner]]"
  - "[[experiments/m23/reports/gf7-branch-search/gf7-targeted-consistency-summary]]"
entities:
  - "[[entities/projects/m23-proof-factory]]"
  - "[[entities/concepts/belyi-map]]"
  - "[[entities/concepts/galois-candidate-search]]"
relationships:
  - target: "[[wiki/m23-belyi-consistency-scoring-runner]]"
    type: "supports"
    confidence: 0.86
    note: "Records the first targeted consistency rescore using hard contradiction counts."
  - target: "[[wiki/m23-belyi-gf7-targeted-overnight-result]]"
    type: "supersedes"
    confidence: 0.82
    note: "Re-ranks the prior 23/25 branch behind zero-hard-contradiction branches."
supersedes:
  - "[[wiki/m23-belyi-gf7-targeted-overnight-result]]"
superseded_by: []
review_after: 2026-06-23
---

# M23 Belyi GF(7) Targeted Consistency Result

## Summary

The targeted consistency rescore completed with status `partial`. It found that the earlier 23/25 reconstruction signal was weaker than several lower-unique-count candidates once exact-equation contradictions were scored.

The best hard-contradiction-scored branch had 22/25 unique rational reconstructions and zero hard contradictions. A post-run linear symbolic check then showed this top branch is still inconsistent: multiple residual equations force different exact values for `p3[0]`.

## Result

| statistic | value |
| --- | ---: |
| prime | 7 |
| levels | 13 |
| depth | 12 |
| beam width | 35 |
| evaluated branches | 791 |
| initial prefix | `[3, 2, 0, 5, 0, 0, 0]` |
| best prefix | `[3, 2, 0, 5, 0, 0, 0, 1, 1, 3, 0, 0]` |
| best lambda | 893556285 |
| best reconstruction | 22/25 unique coefficients |
| hard contradictions | 0 |
| symbolic constraints | 46 |
| status | partial |

## Remaining Unknowns

- `p3[0]`
- `p4[3]`
- `p7[6]`

## Post-Run Linear Check

The top branch had no constant residual contradiction, but the first few symbolic residuals already imply incompatible values for `p3[0]`. Therefore this top branch is also a false rational shadow.

This motivated an upgrade to the consistency scorer: it now detects cheap linear symbolic conflicts and penalizes branches where one unresolved coefficient is forced to multiple exact values.

## Next Run

Rerun the same frontier with the upgraded linear-conflict-aware scorer and a fresh checkpoint directory:

```powershell
.\.venv\Scripts\python experiments/m23/scripts/search_lambda_branches.py --prime 7 --levels 13 --depth 12 --beam-width 35 --max-numerator 250000 --max-denominator 250000 --score-levels 10 --score-max-numerator 50000 --score-max-denominator 50000 --refine-all --score-consistency --consistency-min-unique 20 --initial-prefix 3,2,0,5,0,0,0 --checkpoint-dir experiments/m23/reports/gf7-branch-search/checkpoints-targeted-linear-consistency --checkpoint-prefix gf7-targeted-linear-consistency --progress-every 10 --seed-json experiments/m23/reports/gf7-exhaustive/gf7-normalized-summary.json --out experiments/m23/reports/gf7-branch-search/gf7-targeted-linear-consistency-summary.json --markdown-out experiments/m23/reports/gf7-branch-search/gf7-targeted-linear-consistency-summary.md --title "M23 Belyi GF(7) Targeted Linear Consistency Rescore"
```

## Interpretation

The search is now filtering shadows in progressively stricter layers: unique reconstruction count, hard residual contradictions, and linear symbolic conflicts. This run did not find a candidate map, but it made the scorer substantially more discriminating.
