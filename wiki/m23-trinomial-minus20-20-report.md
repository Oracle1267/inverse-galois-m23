---
type: wiki-page
status: active
created: 2026-05-22
last_confirmed: 2026-05-22
confidence: 0.78
quality_score: 0.84
sensitivity: internal
sources:
  - "[[wiki/m23-ledger-summary]]"
  - "[[experiments/m23/reports/2026-05-22-trinomial-minus20-20-summary]]"
entities:
  - "[[entities/projects/m23-proof-factory]]"
  - "[[entities/concepts/galois-candidate-search]]"
  - "[[entities/concepts/galois-verification-pipeline]]"
relationships:
  - target: "[[wiki/m23-ledger-summary]]"
    type: "supports"
    confidence: 0.90
    note: "Durable interpretation of the generated batch report."
  - target: "[[wiki/m23-search-loop]]"
    type: "depends-on"
    confidence: 0.88
supersedes: []
superseded_by: []
review_after: 2026-06-22
---

# M23 Trinomial Minus20 20 Report

## Summary

The `[-20,20]` trinomial scan tested the family `x^23 + a*x + b` for nonzero integer `a,b` with `-20 <= a,b <= 20`. The latest ledger state has 1600 unique candidates, all rejected by the local M23 filter, with no active survivors.

The generated artifact is [[experiments/m23/reports/2026-05-22-trinomial-minus20-20-summary]].

## Key Observations

- The ledger contains 1601 entries because one candidate, `x^23 - 2*x - 4`, first survived weak filters and was later rejected by stronger filters.
- The most common first rejecting good prime was `p = 5`, followed by `p = 3`, `p = 2`, `p = 7`, and `p = 11`.
- The most frequent incompatible cycle type was `[13, 8, 2]` at `p = 2`, appearing 400 times.
- Only 78 of the latest rejections were reducible over `Q`; most failures were cycle-type incompatibilities.

## Interpretation

This is negative evidence for small-height trinomials, not for the inverse Galois target `M23/Q`. The search process is working, but this family appears to be strongly and systematically filtered out by early modular cycle tests.

The next generator should change structure rather than merely expand the same trinomial box. Useful next directions include sparse quadrinomials, discriminant-aware candidate generation, or literature-guided branch-cycle families.
