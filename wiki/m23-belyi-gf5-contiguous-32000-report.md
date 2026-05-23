---
type: wiki-page
status: stale
created: 2026-05-22
last_confirmed: 2026-05-22
confidence: 0.76
quality_score: 0.86
sensitivity: internal
sources:
  - "[[wiki/m23-elkies-finite-field-solver]]"
  - "[[wiki/m23-belyi-gf5-contiguous-24000-report]]"
  - "[[experiments/m23/reports/2026-05-22-belyi-gf5-normalized-24000-28000]]"
  - "[[experiments/m23/reports/2026-05-22-belyi-gf5-normalized-28000-32000]]"
entities:
  - "[[entities/projects/m23-proof-factory]]"
  - "[[entities/concepts/belyi-map]]"
  - "[[entities/concepts/galois-candidate-search]]"
relationships:
  - target: "[[wiki/m23-elkies-finite-field-solver]]"
    type: "supports"
    confidence: 0.86
    note: "Records the current resumed GF(5) finite-field search coverage."
  - target: "[[wiki/m23-belyi-gf5-contiguous-24000-report]]"
    type: "supersedes"
    confidence: 0.88
    note: "Extends the same GF(5) search line from 24,000 to 32,000 tested triples."
supersedes:
  - "[[wiki/m23-belyi-gf5-contiguous-24000-report]]"
superseded_by:
  - "[[wiki/m23-belyi-gf5-exhausted-report]]"
review_after: 2026-06-22
---

# M23 Belyi GF(5) Contiguous 32000 Report

## Summary

The normalized-first Belyi search over `GF(5)` has now covered a contiguous prefix of 32,000 counted coprime, translation-normalized left-factor triples under the nonzero-lambda and derivative constraints.

No modular equation-system survivor was found in this prefix.

## New Coverage Since 24000

| tested-triple interval | tested triples | derived lambda checks | lambda derivation rejections | result |
| --- | ---: | ---: | ---: | --- |
| 24,000-28,000 | 4,000 | 4,000 | 4,000 | no solutions |
| 28,000-32,000 | 4,000 | 4,000 | 4,000 | no solutions |

## Total Coverage

- Covered interval: 0-32,000 tested triples.
- Solutions found: 0.
- Current continuation offset: `--start-left-factor-triples 32000`.

The intervals from 10,000 onward use `--derivative-first --derive-lambda`. These flags preserve the same derivative-constrained identity check while reducing repeated factorization and lambda scanning.

## Interpretation

This is still a bounded negative result, not exhaustion of the full `GF(5)` search space. It does show a stable early pattern: in the accelerated intervals, every tested left-factor triple fails because the forced lambda condition is not admissible.

The next contiguous batch should start at `--start-left-factor-triples 32000`.

## Supersession

This page is superseded by [[wiki/m23-belyi-gf5-exhausted-report]], which records exhaustion of the full constrained `GF(5)` search space.
