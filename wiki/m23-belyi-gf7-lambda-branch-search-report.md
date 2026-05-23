---
type: wiki-page
status: active
created: 2026-05-23
last_confirmed: 2026-05-23
confidence: 0.78
quality_score: 0.86
sensitivity: internal
sources:
  - "[[wiki/m23-belyi-gf7-reconstruction-report]]"
  - "[[experiments/m23/reports/gf7-branch-search/gf7-lambda-beam25-depth5-mod282475249]]"
  - "[[experiments/m23/reports/gf7-branch-search/gf7-checkpointed-smoke]]"
entities:
  - "[[entities/projects/m23-proof-factory]]"
  - "[[entities/concepts/belyi-map]]"
  - "[[entities/concepts/galois-candidate-search]]"
relationships:
  - target: "[[wiki/m23-belyi-gf7-reconstruction-report]]"
    type: "supports"
    confidence: 0.86
    note: "Searches the free lambda correction direction identified during reconstruction."
  - target: "[[wiki/m23-elkies-finite-field-solver]]"
    type: "supports"
    confidence: 0.82
    note: "Adds a bounded beam-search phase for the 7-adic free parameter."
  - target: "[[wiki/m23-belyi-gf7-overnight-branch-runner]]"
    type: "supports"
    confidence: 0.84
    note: "The checkpointed runner implements the report's next engineering step."
supersedes:
  - "[[wiki/m23-belyi-gf7-reconstruction-report]]"
superseded_by:
  - "[[wiki/m23-belyi-gf7-overnight-result]]"
review_after: 2026-06-23
---

# M23 Belyi GF(7) Lambda Branch Search Report

## Summary

A beam-search tool was added for the one-dimensional `lambda` correction freedom in the `GF(7)` lift. The first wider bounded run evaluated 581 branches and recovered the same best branch already found by the earlier greedy probe. The runner now also has checkpointing, resume support, progress output, and cheaper score-then-refine mode for unattended local searches.

No complete rational reconstruction was found.

## Tooling

- New helper module: `experiments/m23/src/m23verify/branch_search.py`
- New CLI: `experiments/m23/scripts/search_lambda_branches.py`
- Current branch-search report: `experiments/m23/reports/gf7-branch-search/gf7-lambda-beam25-depth5-mod282475249.json`
- Checkpointed smoke report: `experiments/m23/reports/gf7-branch-search/gf7-checkpointed-smoke.json`
- Operating page for the unattended runner: [[wiki/m23-belyi-gf7-overnight-branch-runner]]

## Result

| statistic | value |
| --- | ---: |
| prime | 7 |
| lift modulus | `7^10 = 282475249` |
| search depth | 5 lambda digits |
| beam width | 25 |
| evaluated branches | 581 |
| best prefix | `[3, 4, 0, 0, 0]` |
| best lambda | 223 |
| unique reconstructed coefficients | 16/25 |
| status | partial |

The beam width 25, depth 5 run exceeded the shell timeout, but it left valid JSON and Markdown reports. This still suggests the current implementation needs progress output and checkpointing before larger beam searches are practical.

## Checkpointed Smoke Result

| statistic | value |
| --- | ---: |
| prime | 7 |
| levels | 8 |
| search depth | 2 lambda digits |
| beam width | 3 |
| evaluated branches | 28 |
| best prefix | `[4, 5]` |
| best lambda | 279 |
| unique reconstructed coefficients | 7/25 |
| status | partial |

## Interpretation

The beam search confirms that the simple greedy branch was not merely a one-off local choice, but it also did not find a complete rational map. The best branch remains the `lambda = 223` family at this resolution and scoring bound. Other beam candidates with 16/25 unique coefficients include lambda values 251, 181, and 1973.

The next useful action is to run the checkpointed overnight search and inspect whether any deeper `lambda` branch raises the rational reconstruction score. A partial or negative run should be treated as heuristic evidence only, since beam search is not exhaustive.
