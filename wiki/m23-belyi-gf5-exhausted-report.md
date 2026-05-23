---
type: wiki-page
status: active
created: 2026-05-22
last_confirmed: 2026-05-22
confidence: 0.82
quality_score: 0.88
sensitivity: internal
sources:
  - "[[wiki/m23-elkies-finite-field-solver]]"
  - "[[wiki/m23-belyi-gf5-contiguous-32000-report]]"
entities:
  - "[[entities/projects/m23-proof-factory]]"
  - "[[entities/concepts/belyi-map]]"
  - "[[entities/concepts/galois-candidate-search]]"
relationships:
  - target: "[[wiki/m23-elkies-finite-field-solver]]"
    type: "supports"
    confidence: 0.88
    note: "Records exhaustion of the constrained GF(5) finite-field search."
  - target: "[[wiki/m23-belyi-gf5-contiguous-32000-report]]"
    type: "supersedes"
    confidence: 0.90
    note: "Extends the same GF(5) search line from a 32,000-prefix result to full exhaustion."
supersedes:
  - "[[wiki/m23-belyi-gf5-contiguous-32000-report]]"
superseded_by: []
review_after: 2026-06-22
---

# M23 Belyi GF(5) Exhausted Report

## Summary

The constrained normalized-first Belyi search over `GF(5)` is exhausted.

It tested all 212,636 pairwise-coprime, translation-normalized left-factor triples under the nonzero-lambda and derivative constraints. No modular equation-system survivor was found.

## Final Local Runner Result

- Report directory: `experiments/m23/reports/gf5-exhaustive/`
- Summary file: `experiments/m23/reports/gf5-exhaustive/gf5-normalized-summary.json`
- Batch size: 4,000 tested triples.
- Batch count from offset 32,000: 46.
- Previously covered prefix: 0-32,000 tested triples.
- Local runner coverage: 32,000-212,636 tested triples.
- Total constrained `GF(5)` coverage: 0-212,636 tested triples.
- Solutions found: 0.
- Final stop reason: `exhausted`.

## Rejection Profile

Across the local runner interval, every tested candidate failed the forced-lambda condition:

| statistic | value |
| --- | ---: |
| tested left-factor triples | 180,636 |
| derived lambda checks | 180,636 |
| lambda derivation rejections | 180,636 |
| normalization rejections | 0 |
| derivative rejections | 0 |
| solutions | 0 |

## Interpretation

This exhausts the current constrained `GF(5)` finite-field search line. It does not disprove the Elkies-style construction over other finite fields or under stronger/different equation constraints.

The next meaningful branch is either deeper `GF(7)` coverage or a new mathematical filter that narrows the Belyi identity before scaling to larger finite fields.
