---
type: wiki-page
status: active
created: 2026-05-23
last_confirmed: 2026-05-23
confidence: 0.78
quality_score: 0.86
sensitivity: internal
sources:
  - "[[wiki/m23-belyi-gf7-targeted-overnight-result]]"
  - "[[experiments/m23/reports/gf7-branch-search/consistency-smoke]]"
  - "[[wiki/m23-belyi-gf7-targeted-linear-system-consistency-result]]"
  - "[[wiki/m23-belyi-gf7-targeted-groebner-consistency-result]]"
  - "[[wiki/m23-belyi-gf7-targeted-groebner-min18-result]]"
  - "[[wiki/m23-belyi-gf7-targeted-linear-solution-min18-result]]"
entities:
  - "[[entities/projects/m23-proof-factory]]"
  - "[[entities/concepts/belyi-map]]"
  - "[[entities/concepts/galois-candidate-search]]"
relationships:
  - target: "[[wiki/m23-belyi-gf7-targeted-overnight-result]]"
    type: "depends-on"
    confidence: 0.84
    note: "The new score responds to the symbolic inconsistency found in the 23/25 targeted result."
  - target: "[[wiki/m23-elkies-finite-field-solver]]"
    type: "supports"
    confidence: 0.82
    note: "Adds a stronger branch-search scoring mode to the finite-field/lift/reconstruct pipeline."
supersedes: []
superseded_by: []
review_after: 2026-06-23
---

# M23 Belyi Consistency-Scored Branch Runner

## Summary

The lambda branch search now has a consistency-aware scoring mode. Instead of only rewarding candidates that reconstruct many small rational coefficients, it can test whether the already-reconstructed coefficients are jointly compatible with the exact Belyi identity, derivative identity, and translation normalization.

## Scoring Logic

The new partial consistency check treats unique rational reconstructions as fixed rational numbers and unresolved or ambiguous entries as symbolic variables. It then expands the three exact constraints:

```text
P2^2 * P3 * P4^4 - P7 * P8^2 - lambda = 0
d/dx(P2^2 * P3 * P4^4) - 23 * P2 * P4^3 * P8 = 0
coefficient_x22(P2^2 * P3 * P4^4) = 0
```

Each coefficient residual is classified as:

- `zero`: already exactly compatible.
- `symbolic`: still depends on unresolved entries.
- `hard`: a nonzero constant contradiction, impossible to fix with the remaining unknowns.

When `--score-consistency` is enabled, the branch score prioritizes fewer hard contradictions before raw unique coefficient count. This directly addresses the prior failure mode where a 23/25 reconstruction looked strong but already violated exact equations independent of the two missing entries.

## CLI Flags

- `--score-consistency`: enable symbolic partial consistency scoring during full/refined branch evaluation.
- `--consistency-min-unique N`: only run the symbolic scorer after at least `N` reconstructed entries are unique.

The cheaper pre-score pass remains numeric-only. Checkpoints record both options, so resume runs reject incompatible parameter changes.

The search loop also stops early only for a complete and exact reconstruction. A complete but inexact reconstruction is treated as an invalid branch signal, not as a found solution.

Candidates below `--consistency-min-unique` are kept below candidates that actually receive consistency scoring. This preserves the threshold as a compute guard instead of letting unscored candidates outrank scored candidates because of tuple-shape differences.

The scorer also detects cheap linear symbolic conflicts. If two residual equations independently force different exact values for the same unresolved coefficient, the branch is treated as symbolically inconsistent even when no residual is a standalone nonzero constant.

The scorer now also rank-checks the full linear subsystem across all unresolved coefficients. If the coefficient matrix and augmented matrix have different ranks, the branch is treated as linearly inconsistent even when no single variable has an obvious forced-value conflict.

The scorer now also runs a capped low-degree Groebner check over six equations. It first tries the lowest-degree symbolic residuals directly. If that does not prove inconsistency, it substitutes any solved linear subsystem and tries the lowest-degree reduced nonlinear residuals. A basis containing `1` is treated as a nonlinear conflict.

The scorer now also checks linear-solution residuals. If the linear subsystem uniquely solves every unresolved variable, it substitutes that solution into all symbolic residuals. Remaining nonzero constant residuals are treated as a conflict.

## Verified Smoke

The controlled degenerate identity smoke passed with `hard_contradiction_count = 0`, `linear_solution_conflict_count = 0`, `groebner_conflict_count = 0`, and `symbolic_constraint_count = 0`:

```powershell
.\.venv\Scripts\python experiments/m23/scripts/search_lambda_branches.py --prime 2 --levels 2 --depth 1 --beam-width 1 --max-numerator 10 --max-denominator 10 --score-consistency --consistency-min-unique 0 --checkpoint-dir experiments/m23/reports/gf7-branch-search/checkpoints-consistency-smoke --checkpoint-prefix consistency-smoke --p2 0,0 --p3 0,0,0 --p4 0,0,0,0 --p7 0,0,0,0,0,0,0 --p8 0,0,0,0,0,0,0,0 --lambda 0 --out experiments/m23/reports/gf7-branch-search/consistency-smoke.json --markdown-out experiments/m23/reports/gf7-branch-search/consistency-smoke.md --title "M23 Belyi Consistency Scoring Smoke"
```

## Recommended Next Run

The targeted linear-solution min18 rescore found an apparent clean branch, but a post-run six-equation Groebner check ruled it out. Rerun the min18 frontier with the upgraded scorer:

```powershell
.\.venv\Scripts\python experiments/m23/scripts/search_lambda_branches.py --prime 7 --levels 13 --depth 12 --beam-width 35 --max-numerator 250000 --max-denominator 250000 --score-levels 10 --score-max-numerator 50000 --score-max-denominator 50000 --refine-all --score-consistency --consistency-min-unique 18 --initial-prefix 3,2,0,5,0,0,0 --checkpoint-dir experiments/m23/reports/gf7-branch-search/checkpoints-targeted-groebner6-consistency-min18 --checkpoint-prefix gf7-targeted-groebner6-consistency-min18 --progress-every 10 --seed-json experiments/m23/reports/gf7-exhaustive/gf7-normalized-summary.json --out experiments/m23/reports/gf7-branch-search/gf7-targeted-groebner6-consistency-min18-summary.json --markdown-out experiments/m23/reports/gf7-branch-search/gf7-targeted-groebner6-consistency-min18-summary.md --title "M23 Belyi GF(7) Targeted Groebner6 Consistency Min18 Rescore"
```

If interrupted, rerun the same command with `--resume`.

## Interpretation

This does not prove an M23 polynomial exists on this branch. It makes the automated search more honest: a candidate must now look good as a partial exact equation system, not merely as a collection of individually plausible rational numbers.
