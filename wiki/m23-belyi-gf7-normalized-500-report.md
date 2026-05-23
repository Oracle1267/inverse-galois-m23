---
type: wiki-page
status: stale
created: 2026-05-22
last_confirmed: 2026-05-22
confidence: 0.74
quality_score: 0.84
sensitivity: internal
sources:
  - "[[wiki/m23-elkies-finite-field-solver]]"
  - "[[experiments/m23/reports/2026-05-22-belyi-gf7-normalized-500]]"
entities:
  - "[[entities/projects/m23-proof-factory]]"
  - "[[entities/concepts/belyi-map]]"
  - "[[entities/concepts/galois-candidate-search]]"
relationships:
  - target: "[[wiki/m23-elkies-finite-field-solver]]"
    type: "supports"
    confidence: 0.84
    note: "Records the second finite-field comparison run for the normalized-first search."
  - target: "[[wiki/m23-belyi-gf5-normalized-500-report]]"
    type: "related-to"
    confidence: 0.86
    note: "Uses the same tested-triple budget over a different finite field."
supersedes: []
superseded_by:
  - "[[wiki/m23-belyi-gf7-deep-100000-report]]"
review_after: 2026-06-22
---

# M23 Belyi GF(7) Normalized 500 Report

## Summary

The normalized-first Belyi search ran the Elkies-style identity over `GF(7)` with translation normalization, coprime left factors, nonzero `lambda`, derivative compatibility, and coprime-first enumeration.

The run generated 827 normalized left-factor triples, tested 500 coprime triples, scanned 3,000 lambda values, and found no modular solutions.

## Artifact

- Markdown report: [[experiments/m23/reports/2026-05-22-belyi-gf7-normalized-500]]
- JSON report: `experiments/m23/reports/2026-05-22-belyi-gf7-normalized-500.json`

## Comparison

The same 500 tested-triple budget over `GF(5)` generated 948 normalized triples and scanned 2,000 lambda values. The `GF(7)` run generated fewer triples before reaching 500 coprime cases, but scanned more lambdas because `GF(7)` has six nonzero lambda values.

Neither run produced a modular equation-system survivor.

## Interpretation

This is a bounded negative result in `GF(7)`. It is useful mainly as a second-field comparison point: early behavior is consistent with the `GF(5)` prefix, where the current constraints produce no survivors before the chosen budget limit.

The next useful branch is to add more mathematical filtering before factorization, or to run a modest grid over several primes with smaller per-prime budgets to see whether any field has a qualitatively different rejection profile.

## Supersession

This page is superseded by [[wiki/m23-belyi-gf7-deep-100000-report]], which extends the same constrained `GF(7)` line through 100,000 tested triples.
