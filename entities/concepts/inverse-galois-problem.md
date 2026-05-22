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
  - IGP
relationships:
  - target: "[[entities/projects/m23-proof-factory]]"
    type: "supports"
    confidence: 0.86
  - target: "[[entities/concepts/mathieu-group-m23]]"
    type: "related-to"
    confidence: 0.82
supersedes: []
superseded_by: []
review_after: 2026-06-22
---

# Inverse Galois Problem

## Definition

The inverse Galois problem asks whether every finite group occurs as the Galois group of some field extension of `Q`.

## Attributes

- Type: concept
- Current project target: realize `M23` over `Q`
- Concrete output form: integer polynomial whose splitting field has the desired Galois group

## Relationships

- Supports [[entities/projects/m23-proof-factory]].
- Related to [[entities/concepts/mathieu-group-m23]].

## Notes

For this project, existence is expected by experts but not known for `M23` over `Q` as of sources checked on 2026-05-22.
