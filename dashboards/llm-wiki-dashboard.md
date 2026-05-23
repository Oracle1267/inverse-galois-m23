---
type: dashboard
status: active
created: 2026-05-20
last_confirmed: 2026-05-23
confidence: 0.85
quality_score: 0.85
sensitivity: internal
sources:
  - "[[llm-wiki]]"
entities:
  - "[[entities/projects/riemann-vault]]"
relationships:
  - target: "[[index]]"
    type: "part-of"
    confidence: 0.90
supersedes: []
superseded_by: []
review_after: 2026-06-20
---

# LLM Wiki Dashboard

## Operating Links

- [[index]]
- [[AGENTS]]
- [[governance/schema]]
- [[governance/ingest-protocol]]
- [[governance/query-protocol]]
- [[governance/lint-protocol]]

## Current Sources

- [[llm-wiki]]
- [[Riemann Notes]]

## Current Wiki Pages

- [[wiki/llm-wiki-v2]]
- [[wiki/m23-elkies-finite-field-solver]]
- [[wiki/m23-belyi-gf7-lambda-branch-search-report]]
- [[wiki/m23-belyi-gf7-overnight-branch-runner]]

## Current Working Memory

- [[memory/working/2026-05-20-riemann-hypothesis-exploratory-notes]]

## Review Queues

### Needs Review

Search for `status: needs-review`.

### Stale

Search for pages where `review_after` is before the current date.

### Low Confidence

Search for `confidence:` values below `0.60`.

### Low Quality

Search for `quality_score:` values below `0.70`.

## Maintenance Checklist

- Run ingest for new source notes.
- Update entity pages when new concepts appear.
- Mark superseded claims instead of deleting them.
- Log substantial queries that produce reusable knowledge.
- Run lint after large edits.
- Keep [[index]] current.
