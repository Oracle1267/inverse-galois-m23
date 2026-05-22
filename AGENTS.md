# Riemann Vault Agent Schema

This vault follows the full LLM Wiki v2 pattern described in [[llm-wiki]]. Treat this file as the operating contract for any agent working in the vault.

## Operating Principles

- Preserve raw notes and sources. Add synthesis around them instead of rewriting them.
- Prefer durable, cited knowledge over chat-style summaries.
- Record confidence, quality, lifecycle status, and source links for every knowledge-bearing page.
- Extract typed entities and typed relationships during ingest.
- Resolve contradictions through supersession, not silent overwrite.
- Filter private or sensitive material before writing synthesized pages.
- Log operations that change the knowledge base.
- Keep the system Markdown-first and Obsidian-compatible without requiring plugins.

## Start Here

1. Read [[index]] for the vault map.
2. Read [[governance/schema]] for page types, entity types, relationship types, and frontmatter fields.
3. Use the relevant template from [[templates/README]] before creating a new knowledge-bearing page.
4. Update indexes, entities, and logs as part of the same operation.

## Page Types

Use these `type` values in frontmatter:

- `source`: raw or lightly normalized input.
- `wiki-page`: synthesized durable knowledge.
- `entity`: typed graph node.
- `decision`: explicit choice with rationale.
- `memory`: working, episodic, semantic, or procedural memory.
- `ingest-log`: record of a source ingest.
- `query-log`: record of a substantial query.
- `lint-log`: record of a vault health pass.
- `dashboard`: navigation or operational view.
- `governance`: schema, protocol, or policy.

## Required Frontmatter

Every knowledge-bearing page should include:

```yaml
---
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
---
```

Adjust `type`, `status`, and scores to match the page.

## Confidence Model

- `0.95-1.00`: canonical, repeatedly confirmed, no known contradictions.
- `0.80-0.94`: strong, sourced, and recently confirmed.
- `0.60-0.79`: plausible but limited by source count, age, or scope.
- `0.40-0.59`: exploratory or weakly supported.
- `0.00-0.39`: disputed, stale, or speculative.

Confidence increases when independent sources reinforce a claim. Confidence decreases when claims age, conflict with newer evidence, or lack traceable sources.

## Quality Model

Score pages from `0.0` to `1.0` based on:

- Clear structure.
- Traceable sources.
- Explicit confidence and uncertainty.
- Useful entity links.
- No unresolved contradictions.
- No private material leaking into shared pages.

Pages below `0.70` should be marked `needs-review`.

## Typed Relationships

Represent graph edges in frontmatter and prose. Use this shape when a page has structured relationships:

```yaml
relationships:
  - target: "[[entities/concepts/knowledge-lifecycle]]"
    type: "uses"
    confidence: 0.85
    note: "The page depends on lifecycle scoring and retention."
```

Preferred relationship types:

- `uses`
- `depends-on`
- `supports`
- `contradicts`
- `caused`
- `fixed`
- `supersedes`
- `owned-by`
- `part-of`
- `related-to`

## Ingest Workflow

Use this workflow for every new source:

1. Add or reference the raw source in `sources/` or link to the existing root note.
2. Create an ingest log in `logs/ingest/` from [[templates/ingest-log]].
3. Check sensitivity before writing synthesis.
4. Extract entities: concepts, projects, people, files, and decisions.
5. Extract typed relationships between entities.
6. Create or update pages in `wiki/`.
7. Create or update pages in `entities/`.
8. Assign confidence, quality score, lifecycle status, and `review_after`.
9. Update [[index]] and any relevant dashboard.
10. Record supersession or contradictions when newer claims weaken older claims.

## Query Workflow

Use this workflow for substantive questions:

1. Search [[index]], `wiki/`, `entities/`, `memory/`, and recent logs.
2. Prefer newer, higher-confidence, multi-source claims.
3. Follow graph edges when impact or dependency matters.
4. State uncertainty when evidence is weak or speculative.
5. If the answer produces durable knowledge, file it into `wiki/` or `memory/`.
6. Create a query log in `logs/query/` when the answer changes the vault.

## Lint Workflow

Run lint when the vault changes significantly or on a maintenance pass:

1. Check for missing frontmatter.
2. Check for broken wikilinks.
3. Check for stale pages past `review_after`.
4. Check for low quality scores.
5. Check for contradictions without supersession.
6. Check for orphaned entities.
7. Check for sensitive material outside protected notes.
8. Update `index.md` if folder contents drift from the catalog.
9. Create a lint log in `logs/lint/`.

## Lifecycle Rules

- Working memory is recent and low-confidence by default.
- Episodic memory summarizes sessions and explorations.
- Semantic memory stores cross-session facts.
- Procedural memory stores reusable workflows and patterns.
- Architecture and governance claims decay slowly.
- Exploratory mathematical claims decay faster unless reinforced.
- Superseded claims remain preserved but marked stale.

## Privacy Rules

- Treat credential-like strings, private conversations, PII, and explicitly private material as sensitive.
- Do not copy sensitive raw content into shared wiki pages.
- Use `sensitivity: private` or `sensitivity: secret` when material should not be broadly reused.
- Record redaction decisions in ingest logs.

## Naming Rules

- Use lowercase kebab-case for scaffold files and generated pages.
- Keep existing user-created note names unchanged.
- Prefer stable names over clever names.
- Include dates in logs: `YYYY-MM-DD-short-description.md`.

## Completion Rules

Before saying an ingest or maintenance pass is complete:

1. Verify expected files exist.
2. Verify links and frontmatter are coherent.
3. Verify existing user notes were not overwritten.
4. Update relevant logs.
5. Summarize what changed and what remains uncertain.
