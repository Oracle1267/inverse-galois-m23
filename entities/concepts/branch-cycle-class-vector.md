---
type: entity
entity_type: concept
status: active
created: 2026-05-22
last_confirmed: 2026-05-22
confidence: 0.78
quality_score: 0.80
sensitivity: internal
sources:
  - "[[sources/hafner-2022-m23-braid-orbits]]"
  - "[[sources/elkies-2013-complex-m23-polynomials]]"
aliases:
  - class vector
  - branch cycle vector
relationships:
  - target: "[[entities/concepts/galois-candidate-search]]"
    type: "uses"
    confidence: 0.84
  - target: "[[entities/concepts/mathieu-group-m23]]"
    type: "depends-on"
    confidence: 0.86
supersedes: []
superseded_by: []
review_after: 2026-06-22
---

# Branch Cycle Class Vector

## Definition

A branch-cycle class vector records the conjugacy classes of local monodromy elements for a branched cover. For the M23 search, class vectors describe which M23 conjugacy classes a candidate cover should realize.

## Attributes

- Type: concept
- Examples: `(14A,2A,2A,2A)`, `(15A,2A,2A,2A)`, `(3A,3A,3A,3A)`
- Use: constrains candidate generation before polynomial coefficient search

## Relationships

- Used by [[entities/concepts/galois-candidate-search]].
- Related to [[entities/concepts/braid-orbit]].

## Evidence

- Hafner uses class vectors to organize M23 braid-orbit searches.
- Elkies uses branch orders and cycle structures to derive polynomial identities for complex M23 covers.

## Notes

For this project, class vectors are likely a better starting point than sparse coefficient templates.
