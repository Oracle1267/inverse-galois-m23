---
type: wiki-page
status: active
created: 2026-05-22
last_confirmed: 2026-05-22
confidence: 0.74
quality_score: 0.84
sensitivity: internal
sources:
  - "[[wiki/m23-elkies-finite-field-solver]]"
  - "[[experiments/m23/reports/2026-05-22-belyi-gf5-normalized-500]]"
entities:
  - "[[entities/projects/m23-proof-factory]]"
  - "[[entities/concepts/belyi-map]]"
  - "[[entities/concepts/galois-candidate-search]]"
relationships:
  - target: "[[wiki/m23-elkies-finite-field-solver]]"
    type: "supports"
    confidence: 0.84
    note: "Records the current normalized-first finite-field search frontier."
  - target: "[[wiki/m23-belyi-gf5-prefix-report]]"
    type: "related-to"
    confidence: 0.86
    note: "Extends the earlier 50-triple GF(5) prefix run with direct normalization."
  - target: "[[wiki/m23-belyi-gf7-normalized-500-report]]"
    type: "related-to"
    confidence: 0.86
    note: "Provides the first same-size comparison over a second finite field."
supersedes: []
superseded_by: []
review_after: 2026-06-22
---

# M23 Belyi GF(5) Normalized 500 Report

## Summary

The normalized-first Belyi search ran the Elkies-style identity over `GF(5)` with translation normalization, coprime left factors, nonzero `lambda`, derivative compatibility, and coprime-first enumeration.

The run generated 948 normalized left-factor triples, tested 500 coprime triples, scanned 2,000 lambda values, and found no modular solutions.

## Artifact

- Markdown report: [[experiments/m23/reports/2026-05-22-belyi-gf5-normalized-500]]
- JSON report: `experiments/m23/reports/2026-05-22-belyi-gf5-normalized-500.json`

## Interpretation

This is a bounded negative result in `GF(5)`. It does not weaken the Elkies-style route; it only says that this constrained prefix contains no modular equation-system survivor.

The operational improvement is meaningful: the same 50 tested-triple prefix previously required 708 raw enumerated triples, while normalized-first generation reached 50 tested triples after 88 generated triples. The 500-triple run extends that improved mode by an order of magnitude.

The next useful branch is to compare behavior across more small finite fields or encode additional branch-cycle restrictions before scaling the search volume.
