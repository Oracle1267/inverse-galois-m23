---
type: wiki-page
status: active
created: 2026-05-24
last_confirmed: 2026-05-24
confidence: 0.83
quality_score: 0.88
sensitivity: internal
sources:
  - "[[wiki/m23-belyi-gf7-targeted-linear-system-consistency-result]]"
  - "[[experiments/m23/reports/gf7-branch-search/gf7-targeted-groebner-consistency-summary]]"
entities:
  - "[[entities/projects/m23-proof-factory]]"
  - "[[entities/concepts/belyi-map]]"
  - "[[entities/concepts/galois-candidate-search]]"
relationships:
  - target: "[[wiki/m23-belyi-gf7-targeted-linear-system-consistency-result]]"
    type: "supersedes"
    confidence: 0.84
    note: "Reruns the targeted frontier after adding low-degree Groebner penalties to branch scoring."
  - target: "[[wiki/m23-belyi-consistency-scoring-runner]]"
    type: "supports"
    confidence: 0.87
    note: "Shows that the high-unique targeted frontier has no clean scored branches at the current threshold."
supersedes:
  - "[[wiki/m23-belyi-gf7-targeted-linear-system-consistency-result]]"
superseded_by: []
review_after: 2026-06-24
---

# M23 Belyi GF(7) Targeted Groebner Consistency Result

## Summary

The targeted Groebner consistency rescore completed with status `partial`. It did not find an exact reconstruction. The best branch remained the previous 20/25 prefix, but it now carries a low-degree Groebner conflict in the run output itself.

Across the kept frontier, no scored branch was clean: every candidate with enough unique coefficients to trigger consistency scoring had at least one hard, linear-system, single-variable linear, or Groebner conflict.

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
| low-degree Groebner conflicts | 1 |
| symbolic constraints | 46 |
| status | partial |

## Frontier Diagnostic

The kept candidates tell a stronger story than the nominal best branch:

- Kept candidates inspected across beam history: `147`.
- Clean scored kept candidates: `0`.
- By the final depth, all `35` kept candidates were scored and all had at least one consistency conflict.
- The top three final candidates had no hard, linear-system, or single-variable linear conflict, but each had `groebner_conflict_count = 1`.

This means the current targeted beam is attracted to branches that look numerically rational but are algebraically impossible under the exact equation system.

## Next Run

Score consistency earlier by lowering the threshold from `20` unique coefficients to `18`. This should let the beam avoid contradictory branches before they dominate the frontier:

```powershell
.\.venv\Scripts\python experiments/m23/scripts/search_lambda_branches.py --prime 7 --levels 13 --depth 12 --beam-width 35 --max-numerator 250000 --max-denominator 250000 --score-levels 10 --score-max-numerator 50000 --score-max-denominator 50000 --refine-all --score-consistency --consistency-min-unique 18 --initial-prefix 3,2,0,5,0,0,0 --checkpoint-dir experiments/m23/reports/gf7-branch-search/checkpoints-targeted-groebner-consistency-min18 --checkpoint-prefix gf7-targeted-groebner-consistency-min18 --progress-every 10 --seed-json experiments/m23/reports/gf7-exhaustive/gf7-normalized-summary.json --out experiments/m23/reports/gf7-branch-search/gf7-targeted-groebner-consistency-min18-summary.json --markdown-out experiments/m23/reports/gf7-branch-search/gf7-targeted-groebner-consistency-min18-summary.md --title "M23 Belyi GF(7) Targeted Groebner Consistency Min18 Rescore"
```

## Interpretation

The 20/25 signal has now been demoted from "near miss" to "persistent false shadow." The investigation should either apply consistency scoring earlier in the same targeted region or return to a wider branch search that does not inherit this prefix so strongly.
