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
relationships:
  - target: "[[governance/ingest-protocol]]"
    type: "supports"
    confidence: 0.90
supersedes: []
superseded_by: []
review_after: 2026-06-20
---

# Privacy and Governance

The vault should accumulate useful knowledge without leaking sensitive material into durable shared pages.

## Sensitivity Classes

- `public`: safe to share outside the vault.
- `internal`: normal vault material.
- `private`: personal, restricted, or context-bound material.
- `secret`: credentials, private identifiers, or highly sensitive content.

## Filtering Rule

Before ingest writes synthesized knowledge:

1. Scan the source for credential-like values, private identifiers, private conversations, and explicitly restricted material.
2. Keep sensitive details in the raw source only when appropriate.
3. Do not copy sensitive details into `wiki/`, `entities/`, dashboards, or broad indexes.
4. Record that filtering occurred in the ingest log.
5. Use a higher sensitivity class when in doubt.

## Audit Trail

Create logs for:

- Source ingest that changes the vault.
- Queries that create durable answers.
- Lint passes that repair or reclassify knowledge.
- Supersession of major claims.
- Bulk moves, merges, or archives.

Each log should state:

- What changed.
- Why it changed.
- Which sources or pages were involved.
- What remains uncertain.

## Bulk Operations

Bulk delete, merge, archive, or export operations should be reversible when practical. Before bulk changes:

1. List affected files.
2. State the reason.
3. Preserve links or redirects where needed.
4. Record the operation in an audit log.

## Shared vs Private Knowledge

Shared knowledge belongs in `wiki/`, `entities/`, and semantic or procedural memory. Private or personal context belongs in private memory pages with explicit sensitivity. Promote private material into shared knowledge only after removing personal details and preserving useful general patterns.
