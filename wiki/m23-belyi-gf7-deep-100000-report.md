---
type: wiki-page
status: active
created: 2026-05-22
last_confirmed: 2026-05-22
confidence: 0.78
quality_score: 0.86
sensitivity: internal
sources:
  - "[[wiki/m23-elkies-finite-field-solver]]"
  - "[[wiki/m23-belyi-gf7-normalized-500-report]]"
  - "[[experiments/m23/reports/gf7-deep/gf7-normalized-96500-100000]]"
entities:
  - "[[entities/projects/m23-proof-factory]]"
  - "[[entities/concepts/belyi-map]]"
  - "[[entities/concepts/galois-candidate-search]]"
relationships:
  - target: "[[wiki/m23-elkies-finite-field-solver]]"
    type: "supports"
    confidence: 0.86
    note: "Records the current GF(7) finite-field search frontier."
  - target: "[[wiki/m23-belyi-gf7-normalized-500-report]]"
    type: "supersedes"
    confidence: 0.88
    note: "Extends the same GF(7) search line from 500 to 100,000 tested triples."
supersedes:
  - "[[wiki/m23-belyi-gf7-normalized-500-report]]"
superseded_by: []
review_after: 2026-06-22
---

# M23 Belyi GF(7) Deep 100000 Report

## Summary

The constrained normalized-first Belyi search over `GF(7)` has covered the prefix from 0 through 100,000 counted coprime, translation-normalized left-factor triples under the nonzero-lambda and derivative constraints.

No modular equation-system survivor was found.

## Local Runner Result

- Report directory: `experiments/m23/reports/gf7-deep/`
- Summary file: `experiments/m23/reports/gf7-deep/gf7-normalized-summary.json`
- Batch size: 4,000 tested triples.
- Batch count from offset 500: 25.
- Previously covered prefix: 0-500 tested triples.
- Local runner coverage: 500-100,000 tested triples.
- Total constrained `GF(7)` coverage: 0-100,000 tested triples.
- Solutions found: 0.
- Final stop reason: `target_reached`.
- Next offset: `--start-left-factor-triples 100000`.

## Rejection Profile

Across the local runner interval, every tested candidate failed the forced-lambda condition:

| statistic | value |
| --- | ---: |
| tested left-factor triples | 99,500 |
| derived lambda checks | 99,500 |
| lambda derivation rejections | 99,500 |
| normalization rejections | 0 |
| derivative prefilter rejections | 0 |
| derivative rejections | 0 |
| solutions | 0 |

## Interpretation

This is a bounded negative result, not full `GF(7)` exhaustion. It does show the same rejection pattern seen in the later `GF(5)` run: once `P8` and lambda are forced, the tested triples fail at the lambda derivation stage.

The next `GF(7)` continuation should start at `--start-left-factor-triples 100000`, but a more useful next step may be to add stronger branch-cycle or structural filters before scaling this line further.
