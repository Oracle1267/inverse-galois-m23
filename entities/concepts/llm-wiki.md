---
type: entity
entity_type: concept
status: active
created: 2026-05-20
last_confirmed: 2026-05-20
confidence: 0.88
quality_score: 0.86
sensitivity: internal
sources:
  - "[[llm-wiki]]"
aliases:
  - LLM Wiki
  - durable agent wiki
relationships:
  - target: "[[wiki/llm-wiki-v2]]"
    type: "supports"
    confidence: 0.90
  - target: "[[entities/concepts/knowledge-lifecycle]]"
    type: "uses"
    confidence: 0.86
supersedes: []
superseded_by: []
review_after: 2026-06-20
---

# LLM Wiki

## Definition

An LLM wiki is a knowledge base designed for agents to ingest sources, synthesize durable pages, query prior work, and lint the resulting knowledge over time.

## Attributes

- Type: concept
- Scope: agent-readable knowledge management
- Primary source: [[llm-wiki]]

## Relationships

- Supports [[wiki/llm-wiki-v2]].
- Uses [[entities/concepts/knowledge-lifecycle]] in the v2 pattern.
- Uses [[entities/concepts/typed-knowledge-graph]] for structured navigation.
