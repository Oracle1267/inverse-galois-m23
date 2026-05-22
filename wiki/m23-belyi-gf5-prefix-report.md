---
type: wiki-page
status: active
created: 2026-05-22
last_confirmed: 2026-05-22
confidence: 0.72
quality_score: 0.82
sensitivity: internal
sources:
  - "[[wiki/m23-elkies-finite-field-solver]]"
  - "[[experiments/m23/reports/2026-05-22-belyi-gf5-prefix]]"
entities:
  - "[[entities/projects/m23-proof-factory]]"
  - "[[entities/concepts/belyi-map]]"
  - "[[entities/concepts/galois-candidate-search]]"
relationships:
  - target: "[[wiki/m23-elkies-finite-field-solver]]"
    type: "supports"
    confidence: 0.82
    note: "Records the first report-producing finite-field prefix run."
  - target: "[[entities/concepts/belyi-map]]"
    type: "uses"
    confidence: 0.78
supersedes: []
superseded_by: []
review_after: 2026-06-22
---

# M23 Belyi GF(5) Prefix Report

## Summary

The first report-producing Belyi search ran the Elkies-style identity over `GF(5)` with translation normalization, coprime left factors, nonzero `lambda`, derivative compatibility, and coprime-first enumeration.

The run internally enumerated 708 raw left-factor triples, tested 50 coprime triples, scanned 200 lambda values, and found no modular solutions.

## Artifact

- Markdown report: [[experiments/m23/reports/2026-05-22-belyi-gf5-prefix]]
- JSON report: `experiments/m23/reports/2026-05-22-belyi-gf5-prefix.json`

## Interpretation

This is a bounded negative result, not evidence against the Elkies-style path. Its value is operational: it confirms that the finite-field solver can produce durable artifacts and that constrained prefix searches can now be compared across runs.

The next useful step is either a longer bounded run or a smarter generator that produces normalized, coprime left-factor triples directly instead of filtering the raw enumeration.
