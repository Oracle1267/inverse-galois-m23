---
type: governance
status: active
created: 2026-05-20
last_confirmed: 2026-05-20
confidence: 0.85
quality_score: 0.85
sensitivity: internal
sources:
  - "[[llm-wiki]]"
entities:
  - "[[entities/projects/riemann-vault]]"
relationships:
  - target: "[[AGENTS]]"
    type: "supports"
    confidence: 0.90
supersedes: []
superseded_by: []
review_after: 2026-06-20
---

# Templates

Use these files as starting structures for new vault content.

- [[templates/source]]
- [[templates/wiki-page]]
- [[templates/entity]]
- [[templates/decision]]
- [[templates/ingest-log]]
- [[templates/query-log]]
- [[templates/lint-log]]

When creating a page from a template, update the frontmatter fields, add source links, assign confidence and quality scores, and connect relevant entities.
