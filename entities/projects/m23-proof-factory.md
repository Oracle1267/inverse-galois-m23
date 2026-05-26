---
type: entity
entity_type: project
status: active
created: 2026-05-22
last_confirmed: 2026-05-23
confidence: 0.76
quality_score: 0.85
sensitivity: internal
sources:
  - "[[wiki/m23-proof-factory]]"
  - "[[wiki/m23-search-loop]]"
  - "[[wiki/m23-belyi-gf7-targeted-linear-system-consistency-result]]"
  - "[[wiki/m23-belyi-gf7-targeted-groebner-consistency-result]]"
  - "[[wiki/m23-belyi-gf7-targeted-groebner-min18-result]]"
  - "[[wiki/m23-belyi-gf7-targeted-linear-solution-min18-result]]"
  - "[[wiki/m23-belyi-gf7-targeted-groebner6-min18-result]]"
  - "[[wiki/m23-belyi-gf7-targeted-groebner6-min16-result]]"
  - "[[wiki/m23-belyi-gf7-clean-continuation-result]]"
  - "[[wiki/m23-belyi-timeout-branch-review-runner]]"
  - "[[wiki/m23-belyi-gf7-timeout-review-result]]"
  - "[[wiki/m23-belyi-external-groebner-export-runner]]"
aliases:
  - M23 inverse Galois proof factory
  - M23 search loop
relationships:
  - target: "[[wiki/m23-proof-factory]]"
    type: "supports"
    confidence: 0.92
  - target: "[[entities/concepts/inverse-galois-problem]]"
    type: "depends-on"
    confidence: 0.88
  - target: "[[entities/concepts/mathieu-group-m23]]"
    type: "depends-on"
    confidence: 0.88
  - target: "[[wiki/m23-search-loop]]"
    type: "uses"
    confidence: 0.86
supersedes: []
superseded_by: []
review_after: 2026-06-22
---

# M23 Proof Factory

## Definition

The M23 proof factory is a vault-backed research project for generating, testing, classifying, and iterating on candidate degree-23 polynomials for the inverse Galois problem target `Gal(f/Q) = M23`.

## Attributes

- Type: project
- Status: active implementation
- Primary page: [[wiki/m23-proof-factory]]
- Runnable loop: [[wiki/m23-search-loop]]
- Target output: degree-23 polynomial in `Z[x]` plus rigorous proof

## Relationships

- Depends on [[entities/concepts/inverse-galois-problem]].
- Depends on [[entities/concepts/mathieu-group-m23]].
- Uses [[entities/concepts/galois-candidate-search]].
- Uses [[entities/concepts/galois-verification-pipeline]].

## Notes

The first implementation now has a local verification harness, known-boundary tables, and a resumable trinomial batch loop. The current loop is process infrastructure, not evidence that trinomials are a promising M23 family.

The Belyi-map line now includes finite-field search, prime-power lifting, rational reconstruction, branch search, consistency scoring, focused timeout review, and external Groebner export. The current strongest-looking `GF(7)` branches have been ruled out by progressively stronger exact-equation checks. The targeted min18 frontier has no clean scored branches under the six-equation Groebner scorer. The min16 rescore found a clean lower-unique frontier, but its one-digit continuation dropped the best reconstruction signal to 5/25. The three quarantined timeout branches remained undecided under a 600-second Groebner cap.
