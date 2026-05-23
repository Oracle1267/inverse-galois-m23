---
type: wiki-page
status: active
created: 2026-05-23
last_confirmed: 2026-05-23
confidence: 0.84
quality_score: 0.89
sensitivity: internal
sources:
  - "[[wiki/m23-elkies-finite-field-solver]]"
  - "[[wiki/m23-belyi-gf7-deep-100000-report]]"
  - "[[experiments/m23/reports/gf7-exhaustive/gf7-normalized-290000-300000]]"
entities:
  - "[[entities/projects/m23-proof-factory]]"
  - "[[entities/concepts/belyi-map]]"
  - "[[entities/concepts/galois-candidate-search]]"
relationships:
  - target: "[[wiki/m23-elkies-finite-field-solver]]"
    type: "supports"
    confidence: 0.90
    note: "Provides the first modular survivor found by the finite-field Belyi solver."
  - target: "[[wiki/m23-belyi-gf7-deep-100000-report]]"
    type: "supersedes"
    confidence: 0.88
    note: "Extends the same GF(7) search line from a 100,000 frontier to a modular survivor by 300,000 tested triples."
supersedes:
  - "[[wiki/m23-belyi-gf7-deep-100000-report]]"
superseded_by: []
review_after: 2026-06-23
---

# M23 Belyi GF(7) Modular Survivor Report

## Summary

The constrained normalized-first Belyi search over `GF(7)` found one modular equation-system survivor in the batch `290000-300000`.

This is a real finite-field survivor of the local equation system. It is not yet an integer polynomial, a rational Belyi map, or a proof that the final Galois group is `M23`.

## Runner Result

- Report directory: `experiments/m23/reports/gf7-exhaustive/`
- Summary file: `experiments/m23/reports/gf7-exhaustive/gf7-normalized-summary.json`
- Survivor batch: `experiments/m23/reports/gf7-exhaustive/gf7-normalized-290000-300000.json`
- Stopped reason: `solution_found`.
- Runner interval: 100,000-300,000 tested triples.
- New tested triples in this run: 200,000.
- Total constrained `GF(7)` coverage including earlier checkpoint: 300,000 tested triples.
- Solutions found: 1.
- Next offset if continuing search: `--start-left-factor-triples 300000`.

## Survivor

The coefficient lists are nonleading monic coefficients from highest degree down to constant term.

Over `GF(7)`:

```text
lambda = 6
P2 = x^2 + 3
P3 = x^3 + 6*x^2 + 3*x + 3
P4 = x^4 + 2*x^3 + 6*x^2 + 2*x + 6
P7 = x^7 + 5*x^6 + 4*x^5 + 6*x^4 + x^3 + 5*x^2 + 3*x + 3
P8 = x^8 + x^7 + 3*x^6 + 5*x^5 + 5*x^4 + 6*x^3 + 2*x^2 + 6*x
```

It satisfies:

```text
P2^2 * P3 * P4^4 = P7 * P8^2 + 6 mod 7
```

## Independent Local Verification

The stored survivor was independently rechecked from its coefficients:

| check | result |
| --- | --- |
| identity residual mod 7 | all zero |
| derivative residual mod 7 | all zero |
| translation normalization residual | 0 |
| left factors pairwise coprime | true |

The batch rejected 9,999 of its 10,000 tested triples at lambda derivation, leaving this single survivor.

## Interpretation

This is the first positive signal from the local equation-system path. The next mathematical step is not to treat the survivor as the requested degree-23 integer polynomial. The next step is to use the modular survivor as a seed for lifting: try to recover compatible higher-precision or rational coefficients satisfying the Elkies identity, then derive a candidate degree-23 polynomial and pass it through the M23 verification standard.

