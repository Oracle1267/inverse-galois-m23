# LLM Wiki v2 Vault Design

## Goal

Set up this Obsidian vault as a full v2 LLM wiki: a Markdown-first, agent-readable knowledge system with raw sources, synthesized wiki pages, typed entities, memory tiers, lifecycle policy, privacy controls, audit logs, and reusable templates.

## Current Context

The vault currently contains:

- `llm-wiki.md`: the source note describing the LLM wiki v2 schema and operating philosophy.
- `Riemann Notes.md`: an exploratory note about Riemann Hypothesis variants and related mathematical ideas.
- `.obsidian/`: local Obsidian configuration.

There is no existing repository metadata, ingest script, schema document, or vault index. The setup must preserve existing notes and add structure around them.

## Architecture

The vault will use plain Markdown files and Obsidian wikilinks as the primary interface. Every future agent should be able to follow `AGENTS.md` to ingest sources, query the vault, lint knowledge, and maintain audit trails without requiring an Obsidian plugin.

The system is organized into four knowledge layers:

- Raw evidence in `sources/`
- Synthesized durable pages in `wiki/`
- Typed graph nodes in `entities/`
- Memory consolidation tiers in `memory/`

Governance lives in `governance/`, reusable note patterns live in `templates/`, and operating records live in `logs/`.

## Folder Layout

Create these folders:

```text
sources/
wiki/
entities/
entities/concepts/
entities/projects/
entities/people/
entities/files/
entities/decisions/
memory/
memory/working/
memory/episodic/
memory/semantic/
memory/procedural/
logs/
logs/ingest/
logs/query/
logs/lint/
templates/
governance/
dashboards/
docs/superpowers/specs/
docs/superpowers/plans/
```

## Core Documents

Create:

- `AGENTS.md`: the central operating schema for agents.
- `index.md`: the human-readable vault index.
- `dashboards/llm-wiki-dashboard.md`: a compact operating dashboard.
- `governance/schema.md`: metadata fields, page types, entity types, and relationship types.
- `governance/ingest-protocol.md`: source intake workflow.
- `governance/query-protocol.md`: query and answer filing workflow.
- `governance/lint-protocol.md`: health checks and repair rules.
- `governance/privacy-and-governance.md`: filtering, sensitivity, audit, and reversible bulk operations.
- `governance/lifecycle-policy.md`: confidence, supersession, retention, forgetting, and consolidation.
- `templates/*.md`: reusable templates for sources, wiki pages, entities, decisions, and logs.

## Metadata Model

All knowledge-bearing files should use frontmatter with fields appropriate to the file type. Core fields:

- `type`: source, wiki-page, entity, decision, memory, ingest-log, query-log, lint-log
- `status`: draft, active, needs-review, superseded, archived
- `confidence`: number from 0.0 to 1.0
- `quality_score`: number from 0.0 to 1.0
- `sensitivity`: public, internal, private, secret
- `sources`: list of source note links
- `entities`: list of entity links
- `relationships`: list of typed relationships
- `created`: ISO date
- `last_confirmed`: ISO date
- `review_after`: ISO date or empty when not applicable
- `supersedes`: list of stale claims or pages
- `superseded_by`: list of newer claims or pages

The model must stay readable in plain Markdown and useful to Dataview or scripts later.

## Ingest Flow

For every new source:

1. Place or link the raw material in `sources/`.
2. Create an ingest log in `logs/ingest/`.
3. Filter sensitive content before summarizing.
4. Extract entities and typed relationships.
5. Create or update synthesized pages in `wiki/`.
6. Create or update entity pages in `entities/`.
7. Update `index.md` and `dashboards/llm-wiki-dashboard.md` when useful.
8. Mark confidence, quality score, lifecycle status, and review date.
9. Record unresolved contradictions or supersession decisions.

## Query Flow

For every substantial query:

1. Search `index.md`, `wiki/`, `entities/`, and relevant logs.
2. Prefer claims with higher confidence, newer confirmation, and more sources.
3. Flag uncertainty instead of flattening weak claims into certainty.
4. File durable new insights into `wiki/` or `memory/`.
5. Log the query in `logs/query/` when it changes the knowledge base or produces a reusable answer.

## Lint Flow

Lint should check:

- Missing frontmatter on knowledge-bearing pages.
- Broken wikilinks.
- Orphan entity pages.
- Stale claims past `review_after`.
- Low quality pages below threshold.
- Contradictions without supersession.
- Sensitive values appearing outside protected or private notes.
- Index drift between `index.md` and folder contents.

## Existing Notes

Preserve `llm-wiki.md` as the source/design inspiration and link it from the new index and governance docs.

Preserve `Riemann Notes.md` as an existing exploratory note and index it as active working memory. Do not rewrite its content during scaffold setup.

## Verification

After scaffold creation:

- Confirm every expected file exists.
- Confirm no scaffold file contains unresolved work markers.
- Confirm existing notes still exist unchanged.
- Confirm `index.md` links to `llm-wiki.md`, `Riemann Notes.md`, governance docs, templates, logs, entities, and memory folders.
- Confirm lint/search commands can find the schema terms: confidence, supersession, lifecycle, privacy, audit, typed relationships.

## Constraints

- Plain Markdown first.
- No plugin dependency.
- No destructive changes to existing notes.
- No git commit, because the vault is not currently a git repository.
