---
type: entity
entity_type: concept
status: active
created: 2026-05-20
last_confirmed: 2026-05-20
confidence: 0.78
quality_score: 0.82
sensitivity: internal
sources:
  - "[[llm-wiki]]"
aliases:
  - reciprocal search
  - graph-aware search
relationships:
  - target: "[[entities/concepts/typed-knowledge-graph]]"
    type: "depends-on"
    confidence: 0.75
supersedes: []
superseded_by: []
review_after: 2026-06-20
---

# Hybrid Search

## Definition

Hybrid search combines exact keyword matching, semantic similarity, and graph traversal. In this vault, it is represented as an intended future capability rather than an implemented search engine.

## Attributes

- Type: concept
- Components: keyword search, vector search, graph traversal
- Current implementation: manual search plus structured links

## Relationships

- Depends on [[entities/concepts/typed-knowledge-graph]] for graph traversal.

## Notes

Plain Markdown and Obsidian search are enough for the current vault size. The schema preserves a path toward richer search later.
