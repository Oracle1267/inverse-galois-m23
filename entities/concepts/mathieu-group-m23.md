---
type: entity
entity_type: concept
status: active
created: 2026-05-22
last_confirmed: 2026-05-22
confidence: 0.82
quality_score: 0.80
sensitivity: internal
sources:
  - "[[wiki/m23-proof-factory]]"
aliases:
  - M23
  - Mathieu group M23
  - 23T5
relationships:
  - target: "[[entities/projects/m23-proof-factory]]"
    type: "supports"
    confidence: 0.88
  - target: "[[entities/concepts/galois-verification-pipeline]]"
    type: "depends-on"
    confidence: 0.82
supersedes: []
superseded_by: []
review_after: 2026-06-22
---

# Mathieu Group M23

## Definition

`M23` is a sporadic simple Mathieu group with a natural transitive action of degree 23. In degree-23 transitive group notation it is `23T5`.

## Attributes

- Type: concept
- Order: 10200960
- Degree action: 23
- Project role: target Galois group

## Relationships

- Supports [[entities/projects/m23-proof-factory]] as the target group.
- Depends on [[entities/concepts/galois-verification-pipeline]] for computational recognition in candidate polynomials.

## Notes

The proof factory must distinguish `M23` from other transitive subgroups of `S23`, and especially from large generic groups such as `A23` and `S23`.
