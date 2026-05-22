---
type: wiki-page
status: active
created: 2026-05-20
last_confirmed: 2026-05-20
confidence: 0.86
quality_score: 0.88
sensitivity: internal
sources:
  - "[[llm-wiki]]"
entities:
  - "[[entities/concepts/llm-wiki]]"
  - "[[entities/concepts/knowledge-lifecycle]]"
  - "[[entities/concepts/typed-knowledge-graph]]"
  - "[[entities/concepts/hybrid-search]]"
  - "[[entities/concepts/crystallization]]"
relationships:
  - target: "[[entities/concepts/knowledge-lifecycle]]"
    type: "uses"
    confidence: 0.90
    note: "The v2 pattern adds lifecycle-aware confidence, review, and forgetting."
  - target: "[[entities/concepts/typed-knowledge-graph]]"
    type: "uses"
    confidence: 0.90
    note: "The v2 pattern augments pages with entities and typed relationships."
  - target: "[[entities/concepts/hybrid-search]]"
    type: "uses"
    confidence: 0.82
    note: "The v2 pattern recommends search that combines keyword, vector, and graph traversal methods at scale."
supersedes: []
superseded_by: []
review_after: 2026-06-20
---

# LLM Wiki v2

## Summary

LLM Wiki v2 is a pattern for turning an Obsidian-style note vault into a durable knowledge system. It keeps raw sources, synthesized wiki pages, a typed entity graph, memory tiers, quality controls, privacy rules, and audit logs in one Markdown-first structure.

## Core Claims

- A useful LLM wiki should compile durable knowledge instead of repeatedly retrieving and forgetting context.
- Raw sources, wiki pages, and schema docs are the minimum useful structure.
- Full v2 adds lifecycle management, confidence scoring, supersession, forgetting, typed relationships, hybrid search, automated maintenance hooks, privacy filtering, and audit trails.
- The schema is the central product because it teaches future agents how to maintain the vault.

## Why It Matters

The pattern shifts agent work from ad hoc note-taking to repeatable knowledge operations. Ingest creates durable synthesis, query turns answers back into reusable knowledge when useful, and lint keeps the vault from decaying into disconnected notes.

## Uncertainty

The current vault scaffold is operational but not automated. Hybrid search, vector indexes, and automatic hooks are represented as governance and structure, not executable code.

## Related

- [[AGENTS]]
- [[governance/schema]]
- [[governance/ingest-protocol]]
- [[governance/lifecycle-policy]]
- [[entities/projects/riemann-vault]]
