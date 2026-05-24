---
type: wiki-page
status: active
created: 2026-05-24
last_confirmed: 2026-05-24
confidence: 0.85
quality_score: 0.88
sensitivity: internal
sources:
  - "[[wiki/m23-belyi-gf7-targeted-linear-solution-min18-result]]"
  - "[[experiments/m23/reports/gf7-branch-search/gf7-targeted-groebner6-consistency-min18-summary]]"
entities:
  - "[[entities/projects/m23-proof-factory]]"
  - "[[entities/concepts/belyi-map]]"
  - "[[entities/concepts/galois-candidate-search]]"
relationships:
  - target: "[[wiki/m23-belyi-gf7-targeted-linear-solution-min18-result]]"
    type: "supersedes"
    confidence: 0.84
    note: "Reruns the min18 targeted frontier after raising the Groebner cap to six equations."
  - target: "[[wiki/m23-belyi-consistency-scoring-runner]]"
    type: "supports"
    confidence: 0.88
    note: "Shows the targeted frontier has no clean scored candidates under the current scorer."
supersedes:
  - "[[wiki/m23-belyi-gf7-targeted-linear-solution-min18-result]]"
superseded_by: []
review_after: 2026-06-24
---

# M23 Belyi GF(7) Targeted Groebner6 Min18 Result

## Summary

The targeted min18 rescore with the six-equation Groebner check completed with status `partial`. It did not find a solution, and it did not leave any clean scored candidates in the kept beam.

The best branch had 20/25 unique coefficients, but it had `groebner_conflict_count = 1`. Every kept candidate with enough reconstructed coefficients to be scored had at least one consistency conflict.

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
| best prefix | `[3, 2, 0, 5, 0, 0, 0, 1, 2, 3, 3, 1]` |
| best lambda | 20707177322 |
| best reconstruction | 20/25 unique coefficients |
| hard contradictions | 0 |
| linear-system conflicts | 0 |
| single-variable linear conflicts | 0 |
| linear-solution conflicts | 0 |
| six-equation Groebner conflicts | 1 |
| clean scored kept candidates | 0 |
| status | partial |

## Frontier Diagnostic

The kept frontier was contradiction-saturated under the current scorer:

- Kept candidates inspected across beam history: `147`.
- Clean scored kept candidates: `0`.
- Final kept candidates: `35`.
- Final clean scored candidates: `0`.

This is stronger than the previous min18 result: the apparent clean 18/25 branch disappeared once the Groebner cap was raised.

## Next Run

Score consistency even earlier by lowering the threshold from `18` to `16`. This checks whether the beam should have turned away before the currently targeted region became dominated by high-unique but contradictory branches:

```powershell
.\.venv\Scripts\python experiments/m23/scripts/search_lambda_branches.py --prime 7 --levels 13 --depth 12 --beam-width 35 --max-numerator 250000 --max-denominator 250000 --score-levels 10 --score-max-numerator 50000 --score-max-denominator 50000 --refine-all --score-consistency --consistency-min-unique 16 --initial-prefix 3,2,0,5,0,0,0 --checkpoint-dir experiments/m23/reports/gf7-branch-search/checkpoints-targeted-groebner6-consistency-min16 --checkpoint-prefix gf7-targeted-groebner6-consistency-min16 --progress-every 10 --seed-json experiments/m23/reports/gf7-exhaustive/gf7-normalized-summary.json --out experiments/m23/reports/gf7-branch-search/gf7-targeted-groebner6-consistency-min16-summary.json --markdown-out experiments/m23/reports/gf7-branch-search/gf7-targeted-groebner6-consistency-min16-summary.md --title "M23 Belyi GF(7) Targeted Groebner6 Consistency Min16 Rescore"
```

## Interpretation

This narrow targeted prefix is close to exhausted under the current scoring model. A min16 rerun is the next local check because it changes the beam earlier. If that also produces no clean scored frontier, the next strategic move should be a wider search from an earlier prefix or a different modular survivor/search family.
