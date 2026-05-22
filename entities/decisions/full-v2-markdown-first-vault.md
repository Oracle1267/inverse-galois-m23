---
type: decision
entity_type: decision
status: active
created: 2026-05-20
last_confirmed: 2026-05-20
confidence: 0.92
quality_score: 0.86
sensitivity: internal
sources:
  - "[[llm-wiki]]"
decision_status: accepted
options_considered:
  - Markdown-first schema scaffold
  - Obsidian plugin-heavy vault
  - Script-backed knowledge system
relationships:
  - target: "[[entities/projects/riemann-vault]]"
    type: "supports"
    confidence: 0.92
  - target: "[[AGENTS]]"
    type: "supports"
    confidence: 0.90
supersedes: []
superseded_by: []
review_after: 2026-06-20
---

# Full v2 Markdown-First Vault

## Decision

Set up the vault as a full v2 Markdown-first LLM wiki scaffold.

## Context

The source note [[llm-wiki]] calls for lifecycle management, typed entities, privacy rules, audit trails, quality controls, and automation-ready operations.

## Options Considered

- Markdown-first schema scaffold.
- Obsidian plugin-heavy vault.
- Script-backed knowledge system.

## Rationale

Markdown-first setup gives the vault a strong operating schema without requiring plugins or custom code. It remains portable and easy for future agents to follow.

## Consequences

- The vault is immediately usable.
- Automation is represented by protocols and logs rather than executable hooks.
- Future scripts or plugins can build on the frontmatter and folder structure.

## Review Trigger

Review this decision if the vault grows past what manual search and structured Markdown can comfortably support.
