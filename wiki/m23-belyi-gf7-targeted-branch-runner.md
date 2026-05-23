---
type: wiki-page
status: active
created: 2026-05-23
last_confirmed: 2026-05-23
confidence: 0.80
quality_score: 0.87
sensitivity: internal
sources:
  - "[[wiki/m23-belyi-gf7-overnight-result]]"
  - "[[experiments/m23/reports/gf7-branch-search/gf7-targeted-smoke]]"
  - "[[wiki/m23-belyi-gf7-targeted-overnight-result]]"
entities:
  - "[[entities/projects/m23-proof-factory]]"
  - "[[entities/concepts/belyi-map]]"
  - "[[entities/concepts/galois-candidate-search]]"
relationships:
  - target: "[[wiki/m23-belyi-gf7-overnight-result]]"
    type: "supports"
    confidence: 0.86
    note: "Continues the strongest known lambda branch from the overnight run."
  - target: "[[wiki/m23-belyi-gf7-overnight-branch-runner]]"
    type: "supports"
    confidence: 0.82
    note: "Extends the checkpointed runner with initial-prefix and refine-all modes."
  - target: "[[wiki/m23-belyi-gf7-targeted-overnight-result]]"
    type: "supports"
    confidence: 0.86
    note: "The targeted runner produced the completed 23/25 result."
supersedes: []
superseded_by: []
review_after: 2026-06-23
---

# M23 Belyi GF(7) Targeted Branch Runner

## Summary

The branch-search CLI can now start from one or more known lambda prefixes and can refine every child in the active frontier. This makes the next overnight run a targeted continuation of the current best branch instead of a broad restart.

The target prefix is `[3, 2, 0, 5, 0, 0, 0]`, the best branch from [[wiki/m23-belyi-gf7-overnight-result]].

## New Controls

- `--initial-prefix`: repeatable comma-separated lambda digit prefix. The search begins at that prefix length.
- `--refine-all`: fully reconstructs every child of the current frontier before pruning to the beam.

## Smoke Result

| statistic | value |
| --- | ---: |
| prime | 7 |
| levels | 9 |
| depth | 8 |
| beam width | 3 |
| evaluated branches | 7 |
| initial prefix | `[3, 2, 0, 5, 0, 0, 0]` |
| refine all | true |
| status | partial |

The smoke run is a wiring check only. Its low reconstruction score is expected because it used shallow lift level and small rational bounds.

## Overnight Command

```powershell
.\.venv\Scripts\python experiments/m23/scripts/search_lambda_branches.py --prime 7 --levels 13 --depth 12 --beam-width 35 --max-numerator 250000 --max-denominator 250000 --score-levels 10 --score-max-numerator 50000 --score-max-denominator 50000 --refine-all --initial-prefix 3,2,0,5,0,0,0 --checkpoint-dir experiments/m23/reports/gf7-branch-search/checkpoints-targeted-overnight --checkpoint-prefix gf7-targeted-overnight --progress-every 10 --seed-json experiments/m23/reports/gf7-exhaustive/gf7-normalized-summary.json --out experiments/m23/reports/gf7-branch-search/gf7-targeted-overnight-summary.json --markdown-out experiments/m23/reports/gf7-branch-search/gf7-targeted-overnight-summary.md --title "M23 Belyi GF(7) Targeted Overnight Branch Search"
```

If interrupted, rerun the same command with `--resume`.

## Uncertainty

This remains a heuristic branch search. It is stronger than the previous cheap score-then-refine pass because every child in the current frontier receives full reconstruction before pruning, but it is still not an exhaustive proof over all lambda branches.

## Completed Run

The first targeted overnight run is recorded in [[wiki/m23-belyi-gf7-targeted-overnight-result]]. It improved the reconstruction signal to 23/25 coefficients but remained partial.
