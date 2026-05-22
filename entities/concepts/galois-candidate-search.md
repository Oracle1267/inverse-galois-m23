---
type: entity
entity_type: concept
status: active
created: 2026-05-22
last_confirmed: 2026-05-22
confidence: 0.76
quality_score: 0.80
sensitivity: internal
sources:
  - "[[wiki/m23-proof-factory]]"
aliases:
  - candidate generation
  - polynomial search
relationships:
  - target: "[[entities/projects/m23-proof-factory]]"
    type: "supports"
    confidence: 0.84
  - target: "[[entities/concepts/galois-verification-pipeline]]"
    type: "depends-on"
    confidence: 0.86
supersedes: []
superseded_by: []
review_after: 2026-06-22
---

# Galois Candidate Search

## Definition

Galois candidate search is the constrained generation of polynomial candidates from mathematical families, local signatures, and learned failure constraints.

## Attributes

- Type: concept
- Inputs: candidate families, parameter ranges, modular constraints, ramification patterns
- Outputs: polynomial candidates and search-batch reports

## Relationships

- Supports [[entities/projects/m23-proof-factory]].
- Depends on [[entities/concepts/galois-verification-pipeline]] to reject weak candidates quickly.

## Notes

For the M23 target, random polynomial search is not the strategy. Candidate search should be literature-guided and constraint-updated.
