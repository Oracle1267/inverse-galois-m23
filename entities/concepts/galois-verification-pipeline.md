---
type: entity
entity_type: concept
status: active
created: 2026-05-22
last_confirmed: 2026-05-22
confidence: 0.78
quality_score: 0.82
sensitivity: internal
sources:
  - "[[wiki/m23-proof-factory]]"
aliases:
  - Galois checker
  - candidate verifier
relationships:
  - target: "[[entities/projects/m23-proof-factory]]"
    type: "supports"
    confidence: 0.90
  - target: "[[entities/concepts/mathieu-group-m23]]"
    type: "supports"
    confidence: 0.84
supersedes: []
superseded_by: []
review_after: 2026-06-22
---

# Galois Verification Pipeline

## Definition

The Galois verification pipeline is the sequence of mechanical and mathematical checks used to classify candidate polynomials.

## Attributes

- Type: concept
- Tools: Magma, GAP, Sage, PARI/GP
- Inputs: polynomial candidates
- Outputs: rejection reason, strong-candidate report, or proof-ready evidence bundle

## Relationships

- Supports [[entities/projects/m23-proof-factory]].
- Supports [[entities/concepts/mathieu-group-m23]] recognition through cycle-type and subgroup filters.

## Notes

The checker must be built before large searches, because otherwise the project accumulates untrusted candidate noise.
