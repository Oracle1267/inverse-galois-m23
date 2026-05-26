---
type: wiki-page
status: active
created: 2026-05-25
last_confirmed: 2026-05-25
confidence: 0.86
quality_score: 0.87
sensitivity: internal
sources:
  - "[[wiki/m23-belyi-timeout-branch-review-runner]]"
  - "[[experiments/m23/reports/gf7-branch-search/gf7-groebner-timeout-review-summary]]"
entities:
  - "[[entities/projects/m23-proof-factory]]"
  - "[[entities/concepts/belyi-map]]"
  - "[[entities/concepts/galois-candidate-search]]"
relationships:
  - target: "[[wiki/m23-belyi-timeout-branch-review-runner]]"
    type: "depends-on"
    confidence: 0.90
    note: "This result was produced by the focused timeout-review runner."
  - target: "[[wiki/m23-belyi-gf7-targeted-groebner6-min16-result]]"
    type: "related-to"
    confidence: 0.88
    note: "The reviewed branches were the three Groebner timeout candidates from the min16 rescore."
supersedes: []
superseded_by: []
review_after: 2026-06-25
---

# M23 Belyi GF(7) Timeout Review Result

## Summary

The focused Groebner timeout review completed with a longer `600` second timeout. It reviewed all three quarantined branches from the min16 run.

Result: all three branches still timed out. None was rejected by hard, linear, linear-system, linear-solution, or Groebner contradiction before the timeout.

## Result Table

| Classification | Count |
| --- | ---: |
| `reject` | `0` |
| `survivor` | `0` |
| `timeout` | `3` |

## Reviewed Branches

- Prefix `[3, 2, 0, 5, 0, 0, 0, 0, 2, 0, 1]`, lambda `2058046087`, reconstruction `16 / 25`.
- Prefix `[3, 2, 0, 5, 0, 0, 0, 4, 1, 2, 5, 2]`, lambda `38197583556`, reconstruction `16 / 25`.
- Prefix `[3, 2, 0, 5, 0, 0, 0, 0, 2, 0, 1, 0]`, lambda `2058046087`, reconstruction `16 / 25`.

Each branch had zero detected hard, linear-system, linear, linear-solution, and Groebner conflicts before timing out.

## Interpretation

This result does not clear the branches as survivors. It says Sympy remains unable to decide them within a much longer timeout. The next useful escalation is to export the six low-degree equations for these branches and check them with a stronger Groebner engine, such as Sage/Singular or Magma.
