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
  - "[[experiments/m23/reports/2026-05-22-belyi-gf5-normalized-500]]"
  - "[[experiments/m23/reports/2026-05-22-belyi-gf5-normalized-500-1000]]"
  - "[[experiments/m23/reports/2026-05-22-belyi-gf5-normalized-1000-6000]]"
  - "[[experiments/m23/reports/2026-05-22-belyi-gf5-normalized-6000-8000]]"
  - "[[experiments/m23/reports/2026-05-22-belyi-gf5-normalized-8000-10000]]"
  - "[[experiments/m23/reports/2026-05-22-belyi-gf5-normalized-10000-12000]]"
  - "[[experiments/m23/reports/2026-05-22-belyi-gf5-normalized-12000-16000]]"
  - "[[experiments/m23/reports/2026-05-22-belyi-gf5-normalized-16000-20000]]"
  - "[[experiments/m23/reports/2026-05-22-belyi-gf5-normalized-20000-24000]]"
entities:
  - "[[entities/projects/m23-proof-factory]]"
  - "[[entities/concepts/belyi-map]]"
  - "[[entities/concepts/galois-candidate-search]]"
relationships:
  - target: "[[wiki/m23-elkies-finite-field-solver]]"
    type: "supports"
    confidence: 0.86
    note: "Records the current resumed GF(5) finite-field search coverage."
  - target: "[[wiki/m23-belyi-gf5-normalized-500-report]]"
    type: "supersedes"
    confidence: 0.82
    note: "Extends the same GF(5) search line beyond the first 500 tested triples."
supersedes:
  - "[[wiki/m23-belyi-gf5-normalized-500-report]]"
superseded_by:
  - "[[wiki/m23-belyi-gf5-contiguous-32000-report]]"
review_after: 2026-06-22
---

# M23 Belyi GF(5) Contiguous 24000 Report

## Summary

The normalized-first Belyi search over `GF(5)` has now covered a contiguous prefix of 24,000 counted coprime, translation-normalized left-factor triples under the nonzero-lambda and derivative constraints.

No modular equation-system survivor was found in this prefix.

## Coverage

| tested-triple interval | tested triples | lambda checks | result |
| --- | ---: | ---: | --- |
| 0-500 | 500 | 2,000 | no solutions |
| 500-1,000 | 500 | 2,000 | no solutions |
| 1,000-6,000 | 5,000 | 20,000 | no solutions |
| 6,000-8,000 | 2,000 | 8,000 | no solutions |
| 8,000-10,000 | 2,000 | 8,000 | no solutions |
| 10,000-12,000 | 2,000 | 2,000 | no solutions |
| 12,000-16,000 | 4,000 | 4,000 | no solutions |
| 16,000-20,000 | 4,000 | 4,000 | no solutions |
| 20,000-24,000 | 4,000 | 4,000 | no solutions |

The later intervals use `--derivative-first --derive-lambda`, which preserves the same derivative-constrained identity check while reducing repeated factorization and lambda scanning.

## Interpretation

This is a bounded negative result in `GF(5)`. It does not exhaust the finite-field search, but it makes the current frontier explicit and resumable.

The next contiguous batch should start at `--start-left-factor-triples 24000`.

## Supersession

This page is superseded by [[wiki/m23-belyi-gf5-contiguous-32000-report]], which extends the same search line through 32,000 tested triples.
