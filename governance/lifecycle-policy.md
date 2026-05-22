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
  - "[[entities/concepts/knowledge-lifecycle]]"
  - "[[entities/concepts/crystallization]]"
relationships:
  - target: "[[governance/schema]]"
    type: "supports"
    confidence: 0.90
supersedes: []
superseded_by: []
review_after: 2026-06-20
---

# Lifecycle Policy

Knowledge in this vault has a lifecycle. It can be fresh, reinforced, stale, superseded, archived, or promoted between memory tiers.

## Confidence

Confidence measures how strongly the vault should rely on a claim.

- Increase confidence when independent sources reinforce the claim.
- Increase confidence when the claim is recently confirmed.
- Decrease confidence when the claim is old, weakly sourced, or contradicted.
- Keep speculative ideas below `0.60` unless strong evidence appears.

## Review Timing

Use `review_after` to prevent quiet decay.

- Governance pages: review monthly at first, then less often once stable.
- Working memory: review within days or weeks.
- Exploratory mathematical ideas: review when new evidence or analysis appears.
- Canonical definitions: review when sources change.

## Supersession

Supersession preserves history while making the current claim clear.

When a newer claim replaces an older one:

1. Mark the older page `status: superseded` when the whole page is replaced.
2. Add `superseded_by` to the older page.
3. Add `supersedes` to the newer page.
4. Explain the change in both pages or in an audit log.

## Memory Tiers

### Working Memory

Recent observations, active explorations, and notes that are not yet consolidated.

### Episodic Memory

Session summaries, research digests, and completed chains of work.

### Semantic Memory

Stable cross-session facts and durable explanations.

### Procedural Memory

Reusable workflows, methods, checklists, and habits.

## Promotion Rules

- Working memory becomes episodic memory when a session or exploration is summarized.
- Episodic memory becomes semantic memory when repeated evidence supports a general claim.
- Semantic memory becomes procedural memory when it describes a repeatable workflow.

## Forgetting

Forgetting means deprioritizing, not erasing. Old weak claims should move toward `needs-review`, `superseded`, or `archived` rather than staying active forever.
