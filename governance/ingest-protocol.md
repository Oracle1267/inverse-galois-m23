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
  - "[[entities/concepts/knowledge-lifecycle]]"
  - "[[entities/concepts/typed-knowledge-graph]]"
relationships:
  - target: "[[governance/schema]]"
    type: "depends-on"
    confidence: 0.95
supersedes: []
superseded_by: []
review_after: 2026-06-20
---

# Ingest Protocol

Use this protocol when adding a new source, processing a root note, or crystallizing a completed exploration.

## Intake

1. Identify the source and its owner.
2. Preserve the raw source without destructive edits.
3. Create an ingest log from [[templates/ingest-log]].
4. Assign sensitivity before summarizing.
5. Record whether sensitive material was filtered.

## Extraction

1. Identify durable claims.
2. Identify uncertainty and speculation.
3. Extract entities:
   - Concepts
   - Projects
   - People
   - Files
   - Decisions
4. Extract typed relationships:
   - What uses what?
   - What depends on what?
   - What supports or contradicts what?
   - What supersedes what?

## Synthesis

1. Create or update a page in `wiki/` for stable knowledge.
2. Create or update entity pages under `entities/`.
3. Create memory pages when the source is a session, exploration, or transient observation.
4. Add source links to every synthesized page.
5. Assign confidence and quality scores.
6. Set `review_after` based on lifecycle risk.

## Supersession

When a new claim weakens or replaces an older claim:

1. Keep the older page or claim.
2. Mark the older page `status: superseded` when appropriate.
3. Add the newer page to `superseded_by`.
4. Add the older page to `supersedes` on the newer page.
5. Explain the reason in prose.

## Index Updates

Update [[index]] when the ingest adds:

- A new major source.
- A new wiki page.
- A new active project.
- A new important entity.
- A new governance or procedural pattern.

## Completion Check

An ingest is complete when:

- The raw source is preserved or linked.
- An ingest log exists.
- Durable claims are filed.
- Entities and relationships are updated.
- Confidence and quality scores are present.
- Privacy filtering has been considered.
- The index reflects important new material.
