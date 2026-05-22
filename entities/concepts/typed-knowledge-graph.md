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
  - typed graph
  - entity graph
relationships:
  - target: "[[governance/schema]]"
    type: "supports"
    confidence: 0.92
  - target: "[[entities/concepts/hybrid-search]]"
    type: "supports"
    confidence: 0.78
supersedes: []
superseded_by: []
review_after: 2026-06-20
---

# Typed Knowledge Graph

## Definition

A typed knowledge graph is a layer of entity pages and labeled relationships that makes wiki knowledge navigable by meaning, not only by backlinks or keywords.

## Attributes

- Type: concept
- Entity classes: concepts, projects, people, files, decisions
- Relationship examples: `uses`, `depends-on`, `supports`, `contradicts`, `supersedes`

## Relationships

- Supports [[governance/schema]].
- Supports [[entities/concepts/hybrid-search]] when graph traversal is combined with other search methods.
