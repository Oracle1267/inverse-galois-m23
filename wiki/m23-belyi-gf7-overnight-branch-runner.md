---
type: wiki-page
status: active
created: 2026-05-23
last_confirmed: 2026-05-23
confidence: 0.80
quality_score: 0.87
sensitivity: internal
sources:
  - "[[wiki/m23-belyi-gf7-lambda-branch-search-report]]"
  - "[[experiments/m23/reports/gf7-branch-search/gf7-checkpointed-smoke]]"
entities:
  - "[[entities/projects/m23-proof-factory]]"
  - "[[entities/concepts/belyi-map]]"
  - "[[entities/concepts/galois-candidate-search]]"
relationships:
  - target: "[[wiki/m23-belyi-gf7-lambda-branch-search-report]]"
    type: "supports"
    confidence: 0.84
    note: "Implements the checkpointed and cheaper branch-search follow-up identified by the first lambda beam search."
  - target: "[[wiki/m23-elkies-finite-field-solver]]"
    type: "supports"
    confidence: 0.84
    note: "Extends the local finite-field tooling with an unattended lambda-branch runner."
supersedes: []
superseded_by: []
review_after: 2026-06-23
---

# M23 Belyi GF(7) Overnight Branch Runner

## Summary

The `GF(7)` lambda branch search now has an unattended runner mode. It writes per-depth checkpoints, prints progress to stderr, can resume from the latest completed depth, and uses a cheaper score-then-refine pass before full rational reconstruction.

This is a search tool, not a proof. A complete hit would still need exact identity verification, polynomial extraction, and independent Galois-group verification.

## Claims

- `experiments/m23/scripts/search_lambda_branches.py` supports `--checkpoint-dir`, `--checkpoint-prefix`, `--resume`, `--progress-every`, and `--quiet`.
- Checkpoints are selected by numeric depth, so `depth-10` resumes after `depth-9`.
- The checkpointed runner can score many branches with lower-cost reconstruction bounds, then refine only the top beam candidates with the full bounds.
- A smoke run over the stored `GF(7)` survivor completed and wrote JSON, Markdown, and checkpoint artifacts.

## Smoke Result

| statistic | value |
| --- | ---: |
| prime | 7 |
| levels | 8 |
| depth | 2 |
| beam width | 3 |
| evaluated branches | 28 |
| best prefix | `[4, 5]` |
| best lambda | 279 |
| unique reconstructed coefficients | 7/25 |
| status | partial |

## Overnight Command

```powershell
.\.venv\Scripts\python experiments/m23/scripts/search_lambda_branches.py --prime 7 --levels 12 --depth 8 --beam-width 25 --max-numerator 80000 --max-denominator 80000 --score-levels 8 --score-max-numerator 10000 --score-max-denominator 10000 --refine-multiplier 2 --checkpoint-dir experiments/m23/reports/gf7-branch-search/checkpoints-overnight --checkpoint-prefix gf7-overnight --progress-every 10 --seed-json experiments/m23/reports/gf7-exhaustive/gf7-normalized-summary.json --out experiments/m23/reports/gf7-branch-search/gf7-overnight-summary.json --markdown-out experiments/m23/reports/gf7-branch-search/gf7-overnight-summary.md --title "M23 Belyi GF(7) Overnight Lambda Branch Search"
```

If interrupted, rerun the same command with `--resume`.

## Uncertainty

This runner is heuristic because the beam can discard a branch that only becomes good at a deeper level. It is useful for searching shadows of a rational map, but a negative overnight run is not an exhaustion proof.
