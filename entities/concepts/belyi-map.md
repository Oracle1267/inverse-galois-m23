---
type: entity
entity_type: concept
status: active
created: 2026-05-22
last_confirmed: 2026-05-22
confidence: 0.76
quality_score: 0.78
sensitivity: internal
sources:
  - "[[sources/elkies-2013-complex-m23-polynomials]]"
aliases:
  - three-point cover
relationships:
  - target: "[[entities/concepts/galois-candidate-search]]"
    type: "supports"
    confidence: 0.82
  - target: "[[entities/concepts/branch-cycle-class-vector]]"
    type: "depends-on"
    confidence: 0.78
supersedes: []
superseded_by: []
review_after: 2026-06-22
---

# Belyi Map

## Definition

A Belyi map is a branched cover of the projective line with only three branch points. In the M23 context, such maps encode branch-cycle data that can lead to explicit polynomial identities.

## Attributes

- Type: concept
- Relevant M23 branch orders from Elkies: `23`, `2`, and `4`
- Useful output: structured polynomial identities rather than unconstrained coefficient search

## Relationships

- Supports [[entities/concepts/galois-candidate-search]].
- Depends on [[entities/concepts/branch-cycle-class-vector]].

## Evidence

- Elkies uses a Belyi-map-style equation system to compute complex degree-23 polynomials with monodromy `M23`.

## Notes

The next computational experiment should probably imitate this equation-system shape over finite fields before attempting any rational or integral lift.
