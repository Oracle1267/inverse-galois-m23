---
type: wiki-page
status: stale
created: 2026-05-23
last_confirmed: 2026-05-23
confidence: 0.78
quality_score: 0.86
sensitivity: internal
sources:
  - "[[wiki/m23-belyi-gf7-lift-report]]"
  - "[[experiments/m23/reports/gf7-reconstruction/gf7-reconstruct-lambda223-10000-mod282475249]]"
  - "[[experiments/m23/reports/gf7-reconstruction/gf7-reconstruct-lambda223-80000-mod13841287201]]"
entities:
  - "[[entities/projects/m23-proof-factory]]"
  - "[[entities/concepts/belyi-map]]"
  - "[[entities/concepts/galois-candidate-search]]"
relationships:
  - target: "[[wiki/m23-belyi-gf7-lift-report]]"
    type: "supports"
    confidence: 0.86
    note: "Attempts rational reconstruction from the successful GF(7) prime-power lifts."
  - target: "[[wiki/m23-elkies-finite-field-solver]]"
    type: "supports"
    confidence: 0.82
    note: "Adds rational reconstruction as the next phase after lifting."
supersedes:
  - "[[wiki/m23-belyi-gf7-lift-report]]"
superseded_by:
  - "[[wiki/m23-belyi-gf7-lambda-branch-search-report]]"
review_after: 2026-06-23
---

# M23 Belyi GF(7) Reconstruction Report

## Summary

Rational reconstruction was added and run against the lifted `GF(7)` Belyi survivor. The result is partial, not complete: the lifted survivor has real 7-adic consistency, but the current branches do not yet reconstruct into a full rational Belyi map under the tested bounds.

The important new finding is that the lift has one free direction. The free variable is the `lambda` correction digit at each prime-power lift step. The first nonzero steering test improved rational reconstruction from 10/25 unique coefficients to 16/25 unique coefficients.

## Tooling

- New helper module: `experiments/m23/src/m23verify/reconstruction.py`
- New CLI: `experiments/m23/scripts/reconstruct_belyi_lift.py`
- Updated lift CLI: `experiments/m23/scripts/lift_belyi_survivor.py` now accepts `--lambda-corrections`.

## Reconstruction Attempts

| branch | modulus | bound | unique coefficients | status |
| --- | ---: | ---: | ---: | --- |
| lambda fixed at 6 | `7^6 = 117649` | 500/500 | 10/25 | partial |
| lambda fixed at 6 | `7^8 = 5764801` | 1000/1000 | 6/25 | partial |
| lambda fixed at 6 | `7^10 = 282475249` | 10000/10000 | 10/25 | partial |
| lambda corrections `[3,4,0,0,0,0,0,0,0]`, lambda 223 | `7^10 = 282475249` | 10000/10000 | 16/25 | partial |
| lambda corrections `[3,4,0,0,0,0,0,0,0,0,0]`, lambda 223 | `7^12 = 13841287201` | 80000/80000 | 9/25 | partial |

## Interpretation

The modular survivor is not a one-off: it lifts deeply. However, the current reconstruction attempts have not produced a full rational solution. The one-dimensional freedom in the lift is now the main object of study. A naive zero-free-variable branch keeps `lambda = 6`; a simple greedy first-pass branch gives `lambda = 223` and improves low-bound reconstruction but still does not complete it.

The next useful step is a systematic search over the free `lambda` correction sequence, scored by rational reconstruction and exact residual checks. A better version should treat `lambda` as a 7-adic parameter rather than greedily fixing digits without backtracking.

## Supersession

This page is superseded by [[wiki/m23-belyi-gf7-lambda-branch-search-report]], which records the first bounded beam search over the free `lambda` correction sequence.
