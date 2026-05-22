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
  - "[[entities/concepts/knowledge-lifecycle]]"
relationships:
  - target: "[[governance/schema]]"
    type: "depends-on"
    confidence: 0.90
supersedes: []
superseded_by: []
review_after: 2026-06-20
---

# Lint Protocol

Use this protocol to keep the vault healthy.

## Structural Checks

- Knowledge-bearing pages have frontmatter.
- `type`, `status`, `confidence`, `quality_score`, and `sensitivity` are present.
- Generated page names use lowercase kebab-case.
- Existing user note names remain unchanged.
- Empty operational folders have README files.

## Link Checks

- Important pages are linked from [[index]].
- Entity pages link back to relevant wiki pages.
- Logs link to the sources or pages they changed.
- Superseded pages link to their replacements.
- Replacements link back to the superseded material.

## Lifecycle Checks

- Pages past `review_after` are reviewed.
- Old weak claims are marked `needs-review` or `superseded`.
- Frequently reinforced claims have updated `last_confirmed`.
- Working memory is promoted, summarized, or archived.

## Quality Checks

- Pages below `quality_score: 0.70` are reviewed.
- Pages below `confidence: 0.60` clearly state uncertainty.
- Important claims have sources.
- Contradictions are represented with typed relationships.

## Privacy Checks

- Sensitive source material has not been copied into shared synthesis.
- Pages with restricted content use `sensitivity: private` or `sensitivity: secret`.
- Logs record filtering decisions without exposing the sensitive content itself.

## Index Checks

- New major wiki pages appear in [[index]].
- Important entities appear in [[index]] or a relevant dashboard.
- Governance pages are reachable from [[index]].

## Lint Log

Record each maintenance pass in `logs/lint/` using [[templates/lint-log]] when changes are made or when a useful health snapshot is taken.
