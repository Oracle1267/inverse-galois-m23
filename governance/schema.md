---
type: governance
status: active
created: 2026-05-20
last_confirmed: 2026-05-20
confidence: 0.90
quality_score: 0.90
sensitivity: internal
sources:
  - "[[llm-wiki]]"
entities:
  - "[[entities/concepts/llm-wiki]]"
  - "[[entities/concepts/typed-knowledge-graph]]"
relationships:
  - target: "[[AGENTS]]"
    type: "supports"
    confidence: 0.95
supersedes: []
superseded_by: []
review_after: 2026-06-20
---

# Schema

This page defines the vault schema for pages, entities, metadata, and typed relationships.

## Page Types

- `source`: raw or lightly normalized input.
- `wiki-page`: synthesized durable knowledge.
- `entity`: typed graph node.
- `decision`: explicit choice with rationale.
- `memory`: working, episodic, semantic, or procedural memory.
- `ingest-log`: record of source intake.
- `query-log`: record of a substantial query.
- `lint-log`: record of vault maintenance.
- `dashboard`: navigational or operational view.
- `governance`: schema, protocol, or policy.

## Entity Types

- `concept`: abstract idea, theory, method, or pattern.
- `project`: ongoing body of work.
- `person`: human or agent actor.
- `file`: important file or document.
- `decision`: choice with consequences.

## Status Values

- `draft`: useful but not yet reviewed.
- `active`: currently valid and useful.
- `needs-review`: incomplete, weak, stale, or disputed.
- `superseded`: preserved but replaced by a newer claim or page.
- `archived`: retained for history with low operational value.

## Sensitivity Values

- `public`: safe to share broadly.
- `internal`: normal vault material.
- `private`: personal or restricted material.
- `secret`: credentials, private identifiers, or highly sensitive content.

## Required Fields

```yaml
type: wiki-page
status: draft
created: 2026-05-20
last_confirmed: 2026-05-20
confidence: 0.50
quality_score: 0.50
sensitivity: internal
sources: []
entities: []
relationships: []
supersedes: []
superseded_by: []
review_after:
```

## Relationship Types

Typed relationships are graph edges. Use them in frontmatter and explain important edges in prose.

- `uses`: one thing uses another.
- `depends-on`: one thing requires another.
- `supports`: evidence supports a claim.
- `contradicts`: evidence conflicts with a claim.
- `caused`: one event or factor caused another.
- `fixed`: one action fixed an issue.
- `supersedes`: a newer claim replaces an older one.
- `owned-by`: an actor owns a project, page, or decision.
- `part-of`: a component belongs to a larger system.
- `related-to`: meaningful but weaker association.

## Relationship Shape

```yaml
relationships:
  - target: "[[entities/concepts/knowledge-lifecycle]]"
    type: "uses"
    confidence: 0.85
    note: "This page depends on lifecycle scoring and retention."
```

## Scoring Rules

Use `confidence` for factual strength and `quality_score` for page quality. A page can be well-written but low-confidence if it captures speculation. A page can be high-confidence but low-quality if it lacks links, structure, or context.

## Naming Rules

- Generated files use lowercase kebab-case.
- Existing user notes keep their current names.
- Logs include dates.
- Entity names should be stable and specific.
