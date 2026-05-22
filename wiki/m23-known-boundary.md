---
type: wiki-page
status: active
created: 2026-05-22
last_confirmed: 2026-05-22
confidence: 0.72
quality_score: 0.82
sensitivity: internal
sources:
  - "[[wiki/m23-proof-factory]]"
entities:
  - "[[entities/projects/m23-proof-factory]]"
  - "[[entities/concepts/mathieu-group-m23]]"
relationships:
  - target: "[[wiki/m23-verification-standard]]"
    type: "supports"
    confidence: 0.84
supersedes: []
superseded_by: []
review_after: 2026-06-22
---

# M23 Known Boundary

## Summary

This page records the first boundary facts for the M23 inverse Galois search.

## Seed Facts

- The target group is Mathieu group M23.
- The natural action has degree 23.
- In transitive group notation, the target is `23T5`.
- The group order is `10200960`.
- Current public references checked on 2026-05-22 say `M23/Q` remains open.

## Local Cycle-Type Data

The file `experiments/m23/data/m23_23t5_cycle_types.json` seeds local M23-compatible cycle types for filtering. This table must be verified against GAP or Magma before proof use.

## Next Boundary Work

- Confirm the JSON table against `MathieuGroup(23)` in GAP.
- Record maximal subgroups relevant to degree-23 subgroup exclusion.
- Add known failed branch-cycle or braid-orbit families from Hafner.
