---
type: wiki-page
status: active
created: 2026-05-22
last_confirmed: 2026-05-22
confidence: 0.72
quality_score: 0.82
sensitivity: internal
sources:
  - "[[wiki/m23-literature-constraint-map]]"
  - "[[sources/elkies-2013-complex-m23-polynomials]]"
entities:
  - "[[entities/projects/m23-proof-factory]]"
  - "[[entities/concepts/belyi-map]]"
  - "[[entities/concepts/branch-cycle-class-vector]]"
  - "[[entities/concepts/galois-candidate-search]]"
relationships:
  - target: "[[wiki/m23-literature-constraint-map]]"
    type: "supports"
    confidence: 0.84
    note: "Implements the first finite-field search layer suggested by the literature map."
  - target: "[[entities/concepts/belyi-map]]"
    type: "uses"
    confidence: 0.82
supersedes: []
superseded_by: []
review_after: 2026-06-22
---

# M23 Elkies Finite Field Solver

## Summary

The first Elkies-style finite-field solver searches the identity

```text
P2^2 * P3 * P4^4 = P7 * P8^2 + lambda
```

over `GF(p)`. It enumerates or derives left-side monic factors `P2`, `P3`, and `P4`, scans `lambda`, derives possible right-side factors `P7` and `P8` by square-divisor factorization, and verifies the full residual.

## Commands

Degenerate sanity check:

```powershell
.\.venv\Scripts\python experiments/m23/scripts/solve_belyi_modp.py --modulus 2 --fixed-p2 0,0 --fixed-p3 0,0,0 --fixed-p4 0,0,0,0 --max-solutions 1
```

Constrained prefix search:

```powershell
.\.venv\Scripts\python experiments/m23/scripts/solve_belyi_modp.py --modulus 5 --max-left-factor-triples 50 --max-solutions 3 --require-translation-normalized --require-coprime-left --coprime-first --require-nonzero-lambda --require-derivative
```

Constrained prefix search with report artifacts:

```powershell
.\.venv\Scripts\python experiments/m23/scripts/solve_belyi_modp.py --modulus 5 --max-left-factor-triples 50 --max-solutions 3 --require-translation-normalized --require-coprime-left --coprime-first --require-nonzero-lambda --require-derivative --out experiments/m23/reports/2026-05-22-belyi-gf5-prefix.json --markdown-out experiments/m23/reports/2026-05-22-belyi-gf5-prefix.md --title "M23 Belyi GF(5) Prefix Search"
```

Normalized-first report-producing search:

```powershell
.\.venv\Scripts\python experiments/m23/scripts/solve_belyi_modp.py --modulus 5 --max-left-factor-triples 500 --max-solutions 3 --require-translation-normalized --normalized-first --require-coprime-left --coprime-first --require-nonzero-lambda --require-derivative --out experiments/m23/reports/2026-05-22-belyi-gf5-normalized-500.json --markdown-out experiments/m23/reports/2026-05-22-belyi-gf5-normalized-500.md --title "M23 Belyi GF(5) Normalized 500 Search"
```

## Current Behavior

- The degenerate sanity check finds the expected identity with all factors equal to powers of `x` and `lambda = 0`.
- The constrained prefix search over `GF(2)` with coprime left factors, nonzero `lambda`, and derivative compatibility found no solutions in the first 20 left-factor triples.
- A constrained prefix search over `GF(5)` with translation normalization, coprime left factors, nonzero `lambda`, derivative compatibility, and `--coprime-first` found no solutions after internally enumerating 708 raw triples, testing 50 coprime triples, and scanning 200 lambda values.
- The normalized-first `GF(5)` run found no solutions after generating 948 normalized triples, testing 500 coprime triples, and scanning 2,000 lambda values.
- The solver has explicit bounds through `--max-left-factor-triples` and `--max-solutions` to avoid runaway enumeration.
- The CLI can now write reproducible JSON and Markdown reports with `--out`, `--markdown-out`, and `--title`.

## Report Artifacts

- [[experiments/m23/reports/2026-05-22-belyi-gf5-prefix]] records the current `GF(5)` prefix run.
- [[wiki/m23-belyi-gf5-prefix-report]] interprets that run as a bounded negative result and a reporting-pipeline check.
- [[experiments/m23/reports/2026-05-22-belyi-gf5-normalized-500]] records the larger normalized-first `GF(5)` run.
- [[wiki/m23-belyi-gf5-normalized-500-report]] interprets the larger run as the current finite-field search frontier.

## Derivative Constraint

Away from characteristic 23, the identity should also satisfy:

```text
d/dx(P2^2 * P3 * P4^4) = 23 * P2 * P4^3 * P8
```

The CLI flag `--require-derivative` enforces this relation. In the current `GF(2)` false-positive check with `P4 = x^4 + 1`, the raw identity produces four solutions, but all four are rejected by the derivative constraint.

## Translation Normalization

Away from characteristic 23, a monic degree-23 polynomial can be translated to eliminate the `x^22` coefficient. The CLI flag `--require-translation-normalized` enforces that normal form on the left polynomial `P2^2 * P3 * P4^4`.

In a fixed `GF(5)` sample with `P2 = x^2 + x`, the normalization flag rejected the factor triple before any lambda values were tested.

The CLI flag `--normalized-first` uses the coefficient relation `2*a(P2) + c(P3) + 4*f(P4) = 0 mod p` to derive the leading non-monic coefficient of `P3` when translation normalization is required. This makes the prefix budget count generated normalized triples instead of raw triples that are later rejected.

## Enumeration Order

The CLI flags `--coprime-first` and `--normalized-first` change the meaning of the left-factor prefix budget. Non-coprime triples can be skipped before counting, and translation-normalized triples can be generated directly. The raw default ordering remains available for reproducibility.

## Interpretation

This is not yet a serious M23 construction. It is the first tested finite-field search primitive for the equation-system path. The next improvements should add stronger branch-cycle constraints, test a second finite field, or run longer report-producing searches.
