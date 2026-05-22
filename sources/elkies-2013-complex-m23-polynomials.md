---
type: source
status: active
created: 2026-05-22
last_confirmed: 2026-05-22
confidence: 0.84
quality_score: 0.82
sensitivity: internal
source_kind: paper
origin: "https://msp.org/obs/2013/1-1/obs-v1-n1-p18-s.pdf"
owner: "Noam D. Elkies"
entities:
  - "[[entities/concepts/mathieu-group-m23]]"
  - "[[entities/concepts/belyi-map]]"
  - "[[entities/concepts/branch-cycle-class-vector]]"
relationships:
  - target: "[[wiki/m23-literature-constraint-map]]"
    type: "supports"
    confidence: 0.86
supersedes: []
superseded_by: []
review_after: 2026-06-22
---

# Elkies 2013 Complex M23 Polynomials

## Source Metadata

- Origin: [Open Book Series PDF](https://msp.org/obs/2013/1-1/obs-v1-n1-p18-s.pdf)
- Title: The complex polynomials `P(x)` with `Gal(P(x)-t) ~= M23`
- Author: Noam D. Elkies
- Date: 2013
- Sensitivity: public

## Normalized Content

Elkies determines the complex degree-23 polynomials `P` whose monodromy group over `C(t)` is `M23`. This is not the same as finding a polynomial in `Z[x]` whose splitting field over `Q` has Galois group `M23`, but it gives a highly structured equation system.

Key normalized claims:

- The relevant cover has branch orders `23`, `2`, and `4`.
- The degree-23 permutation action uses the `M23` cycle types `2^8 1^7`, `4^4 2^2 1^3`, and `23`.
- Up to linear equivalence, the cover can be expressed through coprime monic factors with degrees `2`, `3`, `4`, `7`, and `8`.
- A useful identity form is `P = P2^2 * P3 * P4^4 = P7 * P8^2 + lambda`.
- The derivative constraint reduces the nonlinear system and is central to making computation feasible.
- The computational strategy uses finite-field search, p-adic Newton iteration, lattice recognition, and exact verification.

## Initial Observations

- This source suggests a much more promising AI-assisted experiment than broad sparse-polynomial search: write a symbolic equation system, solve over finite fields or p-adically, lift, and verify.
- The source also warns that the equations can confuse `M23` and `A23` covers, so modular cycle testing and subgroup exclusion remain essential.

## Candidate Entities

- [[entities/concepts/belyi-map]]
- [[entities/concepts/branch-cycle-class-vector]]

## Candidate Relationships

- [[entities/concepts/belyi-map]] supports [[entities/concepts/galois-candidate-search]].
- [[entities/concepts/branch-cycle-class-vector]] constrains [[entities/concepts/galois-verification-pipeline]].
