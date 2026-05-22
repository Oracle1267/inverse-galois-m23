---
type: entity
entity_type: project
status: active
created: 2026-05-20
last_confirmed: 2026-05-20
confidence: 0.92
quality_score: 0.88
sensitivity: internal
sources:
  - "[[llm-wiki]]"
  - "[[Riemann Notes]]"
aliases:
  - Riemann Obsidian vault
relationships:
  - target: "[[AGENTS]]"
    type: "depends-on"
    confidence: 0.94
  - target: "[[wiki/llm-wiki-v2]]"
    type: "uses"
    confidence: 0.90
  - target: "[[entities/decisions/full-v2-markdown-first-vault]]"
    type: "uses"
    confidence: 0.92
supersedes: []
superseded_by: []
review_after: 2026-06-20
---

# Riemann Vault

## Definition

The Riemann Vault is this Obsidian workspace configured as a full v2 LLM wiki for exploratory mathematical notes and future knowledge work.

## Attributes

- Type: project
- Location: `C:\Projects\Riemann`
- Operating schema: [[AGENTS]]
- Index: [[index]]

## Relationships

- Uses [[wiki/llm-wiki-v2]] as the design pattern.
- Depends on [[AGENTS]] for agent behavior.
- Uses [[entities/decisions/full-v2-markdown-first-vault]] as the setup decision.
