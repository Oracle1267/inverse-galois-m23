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
  - "[[sources/hafner-2022-m23-braid-orbits]]"
aliases:
  - Hurwitz braid orbit
relationships:
  - target: "[[entities/concepts/branch-cycle-class-vector]]"
    type: "uses"
    confidence: 0.84
  - target: "[[entities/concepts/galois-candidate-search]]"
    type: "supports"
    confidence: 0.80
supersedes: []
superseded_by: []
review_after: 2026-06-22
---

# Braid Orbit

## Definition

A braid orbit is an orbit of generating systems under the Hurwitz braid group action. In rigidity-style inverse Galois searches, braid orbits help determine whether a class vector can produce a cover with the desired arithmetic properties.

## Attributes

- Type: concept
- Inputs: finite group, class vector, generating systems
- Outputs: orbit sizes, genera, symmetry behavior, possible realization routes

## Relationships

- Uses [[entities/concepts/branch-cycle-class-vector]].
- Supports [[entities/concepts/galois-candidate-search]].

## Evidence

- Hafner's M23 paper is organized around braid orbit computations and their new invariants.

## Notes

For the current project, braid-orbit data is a way to prioritize candidate families before doing coefficient search.
