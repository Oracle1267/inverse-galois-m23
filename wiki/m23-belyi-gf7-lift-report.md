---
type: wiki-page
status: active
created: 2026-05-23
last_confirmed: 2026-05-23
confidence: 0.84
quality_score: 0.88
sensitivity: internal
sources:
  - "[[wiki/m23-belyi-gf7-modular-survivor-report]]"
  - "[[experiments/m23/reports/gf7-lift/gf7-survivor-lift-mod117649]]"
entities:
  - "[[entities/projects/m23-proof-factory]]"
  - "[[entities/concepts/belyi-map]]"
  - "[[entities/concepts/galois-candidate-search]]"
relationships:
  - target: "[[wiki/m23-belyi-gf7-modular-survivor-report]]"
    type: "supports"
    confidence: 0.90
    note: "Uses the GF(7) modular survivor as the seed for prime-power lifting."
  - target: "[[wiki/m23-elkies-finite-field-solver]]"
    type: "supports"
    confidence: 0.86
    note: "Adds a lifting phase after finite-field search."
supersedes:
  - "[[wiki/m23-belyi-gf7-modular-survivor-report]]"
superseded_by: []
review_after: 2026-06-23
---

# M23 Belyi GF(7) Lift Report

## Summary

The `GF(7)` modular Belyi survivor lifted successfully through five Hensel-style correction steps, from modulus `7` to modulus `7^6 = 117649`.

This is a stronger positive signal than the original modular hit. It still is not a rational Belyi map or a degree-23 integer polynomial; it is a high-precision 7-adic approximation to the equation-system solution.

## Tooling

- New helper module: `experiments/m23/src/m23verify/lifting.py`
- New CLI: `experiments/m23/scripts/lift_belyi_survivor.py`
- Highest report: `experiments/m23/reports/gf7-lift/gf7-survivor-lift-mod117649.json`
- Highest Markdown report: `experiments/m23/reports/gf7-lift/gf7-survivor-lift-mod117649.md`

The lifting tool solves the linearized correction equations from modulus `7^k` to `7^(k+1)` while preserving:

- the Elkies identity;
- the derivative constraint;
- translation normalization.

## Result

| statistic | value |
| --- | ---: |
| initial modulus | 7 |
| final modulus | 117649 |
| correction steps | 5 |
| constraints per step | 48 |
| variables per step | 25 |
| rank per step | 24 |
| lambda correction | 0 at each recorded step |
| status | lifted |

## Lifted Coefficients Mod 117649

The coefficient lists are nonleading monic coefficients from highest degree down to constant term.

```text
lambda = 6
P2 = [117327, 103120]
P3 = [86057, 39728, 99753]
P4 = [8059, 107274, 19273, 17142]
P7 = [47710, 86867, 18521, 69511, 16784, 19400, 25882]
P8 = [93794, 69681, 78895, 82612, 111859, 115306, 32829, 100541]
```

## Interpretation

The modular survivor did not die at `49` or `343`; it continued to lift through `117649`. The next useful step is rational reconstruction or a more constrained normalization choice, because the linear system has rank 24 with 25 variables. In the current implementation, the free variable is left at zero correction, which keeps `lambda = 6` throughout the recorded lift.

