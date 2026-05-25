---
type: wiki-page
status: active
created: 2026-05-25
last_confirmed: 2026-05-25
confidence: 0.85
quality_score: 0.88
sensitivity: internal
sources:
  - "[[wiki/m23-belyi-gf7-targeted-groebner6-min18-result]]"
  - "[[experiments/m23/reports/gf7-branch-search/gf7-targeted-groebner6-consistency-min16-summary]]"
entities:
  - "[[entities/projects/m23-proof-factory]]"
  - "[[entities/concepts/belyi-map]]"
  - "[[entities/concepts/galois-candidate-search]]"
relationships:
  - target: "[[wiki/m23-belyi-gf7-targeted-groebner6-min18-result]]"
    type: "supersedes"
    confidence: 0.78
    note: "The min16 rescore relaxed the consistency-scoring threshold and found a lower-unique clean frontier after min18 found no clean scored kept candidates."
  - target: "[[wiki/m23-belyi-consistency-scoring-runner]]"
    type: "supports"
    confidence: 0.86
    note: "Confirms timeout quarantine and per-candidate progress are sufficient for completing the previously blocking run."
supersedes:
  - "[[wiki/m23-belyi-gf7-targeted-groebner6-min18-result]]"
superseded_by: []
review_after: 2026-06-25
---

# M23 Belyi GF(7) Targeted Groebner6 Min16 Result

## Summary

The targeted six-equation Groebner rescore with `--consistency-min-unique 16` completed with status `partial`. It did not find a complete exact reconstruction, but it escaped the contradiction-saturated min18 frontier by keeping a lower-unique branch with no detected hard, linear, linear-solution, or six-equation Groebner contradiction.

The best clean branch reconstructs `16 / 25` coefficients. That is weaker numerically than the earlier `23 / 25` branch, but stronger algebraically: the currently reconstructed values have not yet contradicted the exact Belyi identity tests.

## Result Table

| Field | Value |
| --- | --- |
| Prime | `7` |
| Levels | `13` |
| Depth | `12` |
| Beam width | `35` |
| Consistency threshold | `16` unique coefficients |
| Evaluated branches | `791` |
| Best prefix | `[3, 2, 0, 5, 0, 0, 0, 0, 5, 1, 6, 4]` |
| Best lambda | `67713364676` |
| Best reconstruction | `16 / 25` unique coefficients |
| Best conflicts | hard `0`, linear-system `0`, linear `0`, linear-solution `0`, Groebner `0` |
| Best Groebner timeouts | `0` |
| Final clean scored candidates | `4` |
| Total clean scored kept candidates | `7` |
| Groebner timeout candidates | `3` |
| Status | `partial` |

## Best Branch Details

Unresolved coefficients:

- `p2[0]`
- `p2[1]`
- `p3[0]`
- `p3[1]`
- `p4[2]`
- `p7[1]`
- `p7[3]`
- `p7[5]`
- `p8[3]`

Consistency profile:

| Check | Count |
| --- | ---: |
| Hard constant contradictions | `0` |
| Full linear-system conflicts | `0` |
| Single-variable linear conflicts | `0` |
| Linear-solution residual conflicts | `0` |
| Six-equation Groebner conflicts | `0` |
| Six-equation Groebner timeouts | `0` |
| Symbolic residual constraints | `46` |
| Linear-system equations | `3` |
| Linear-system rank | `2` |
| Augmented rank | `2` |

Interpretation: this is not a solution. It is a survivable partial equation system whose remaining unknowns still have room to absorb the exact constraints.

## Timeout Candidates

Three branches were quarantined because the capped Sympy Groebner check timed out:

- Prefix `[3, 2, 0, 5, 0, 0, 0, 0, 2, 0, 1]`, lambda `2058046087`, reconstruction `16 / 25`.
- Prefix `[3, 2, 0, 5, 0, 0, 0, 4, 1, 2, 5, 2]`, lambda `38197583556`, reconstruction `16 / 25`.
- Prefix `[3, 2, 0, 5, 0, 0, 0, 0, 2, 0, 1, 0]`, lambda `2058046087`, reconstruction `16 / 25`.

These are not rejected mathematically. They are lower-priority until checked with a stronger algebra system or longer timeout.

## Next Continuation

Continue from the four clean final branches rather than from the contradiction-heavy high-unique branches:

```powershell
$env:M23_GROEBNER_TIMEOUT_SECONDS = "60"

.\.venv\Scripts\python experiments/m23/scripts/search_lambda_branches.py --prime 7 --levels 14 --depth 13 --beam-width 35 --max-numerator 250000 --max-denominator 250000 --score-levels 10 --score-max-numerator 50000 --score-max-denominator 50000 --refine-all --score-consistency --consistency-min-unique 16 --initial-prefix 3,2,0,5,0,0,0,0,5,1,6,4 --initial-prefix 3,2,0,5,0,0,0,1,0,4,0,0 --initial-prefix 3,2,0,5,0,0,0,1,0,4,6,0 --initial-prefix 3,2,0,5,0,0,0,4,1,2,5,0 --checkpoint-dir experiments/m23/reports/gf7-branch-search/checkpoints-targeted-groebner6-clean-continuation --checkpoint-prefix gf7-targeted-groebner6-clean-continuation --progress-every 10 --seed-json experiments/m23/reports/gf7-exhaustive/gf7-normalized-summary.json --out experiments/m23/reports/gf7-branch-search/gf7-targeted-groebner6-clean-continuation-summary.json --markdown-out experiments/m23/reports/gf7-branch-search/gf7-targeted-groebner6-clean-continuation-summary.md --title "M23 Belyi GF(7) Targeted Groebner6 Clean Continuation"
```

## Interpretation

The min16 result changes the shape of the search. The earlier high-reconstruction branches were attractive because they looked close to complete, but exact-equation checks repeatedly exposed contradictions. The min16 run found lower-reconstruction branches that are less flashy but more algebraically honest.

The current best path is therefore to extend the clean lower-unique frontier and keep quarantined timeout cases available for later external algebra verification.
