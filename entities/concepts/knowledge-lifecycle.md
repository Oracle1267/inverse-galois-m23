---
type: entity
entity_type: concept
status: active
created: 2026-05-20
last_confirmed: 2026-05-20
confidence: 0.86
quality_score: 0.86
sensitivity: internal
sources:
  - "[[llm-wiki]]"
aliases:
  - memory lifecycle
  - retention lifecycle
relationships:
  - target: "[[governance/lifecycle-policy]]"
    type: "supports"
    confidence: 0.92
  - target: "[[entities/concepts/crystallization]]"
    type: "related-to"
    confidence: 0.80
supersedes: []
superseded_by: []
review_after: 2026-06-20
---

# Knowledge Lifecycle

## Definition

Knowledge lifecycle is the practice of tracking how claims age, strengthen, weaken, become superseded, or move between memory tiers.

## Attributes

- Type: concept
- Key fields: `confidence`, `last_confirmed`, `review_after`, `supersedes`, `superseded_by`

## Relationships

- Supports [[governance/lifecycle-policy]].
- Related to [[entities/concepts/crystallization]] because explorations can become durable memory.

## Notes

This vault treats forgetting as deprioritization rather than deletion.
