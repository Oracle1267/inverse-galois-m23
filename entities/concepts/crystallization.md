---
type: entity
entity_type: concept
status: active
created: 2026-05-20
last_confirmed: 2026-05-20
confidence: 0.84
quality_score: 0.84
sensitivity: internal
sources:
  - "[[llm-wiki]]"
aliases:
  - knowledge crystallization
  - session crystallization
relationships:
  - target: "[[memory/episodic/README]]"
    type: "supports"
    confidence: 0.82
  - target: "[[memory/semantic/README]]"
    type: "supports"
    confidence: 0.76
supersedes: []
superseded_by: []
review_after: 2026-06-20
---

# Crystallization

## Definition

Crystallization is the process of distilling a completed chain of work into a structured digest, then promoting durable lessons into the wiki or memory tiers.

## Attributes

- Type: concept
- Inputs: research threads, debugging sessions, exploratory notes, query results
- Outputs: episodic summaries, semantic claims, procedural workflows

## Relationships

- Supports [[memory/episodic/README]].
- Supports [[memory/semantic/README]] when repeated evidence produces stable facts.
