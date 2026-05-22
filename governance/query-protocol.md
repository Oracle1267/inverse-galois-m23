---
type: governance
status: active
created: 2026-05-20
last_confirmed: 2026-05-20
confidence: 0.88
quality_score: 0.88
sensitivity: internal
sources:
  - "[[llm-wiki]]"
entities:
  - "[[entities/concepts/hybrid-search]]"
  - "[[entities/concepts/typed-knowledge-graph]]"
relationships:
  - target: "[[governance/schema]]"
    type: "depends-on"
    confidence: 0.90
supersedes: []
superseded_by: []
review_after: 2026-06-20
---

# Query Protocol

Use this protocol when answering a question from the vault.

## Search Order

1. Start at [[index]].
2. Read relevant pages in `wiki/`.
3. Traverse entity pages in `entities/`.
4. Check current memory in `memory/working/`.
5. Check episodic and semantic memory when the question spans past work.
6. Check logs when provenance matters.

## Evidence Ranking

Prefer claims that are:

- Supported by multiple sources.
- Recently confirmed.
- High confidence.
- Not superseded.
- Connected through typed relationships.
- Written with clear uncertainty boundaries.

## Answering

When answering:

- Cite or link the strongest vault pages.
- Distinguish stable facts from speculation.
- Mention contradictions if they matter.
- Follow graph edges for impact questions.
- Avoid presenting low-confidence claims as settled.

## Filing Back

Create or update vault knowledge when an answer produces:

- A reusable explanation.
- A new decision.
- A clarified concept.
- A contradiction resolution.
- A workflow that should be procedural memory.

Use [[templates/query-log]] when the query changes the vault or creates a reusable answer.

## Quality Bar

A query result should be filed only when it is clear enough to be useful later. If the answer is mostly exploratory, file it as working or episodic memory instead of semantic knowledge.
