---
type: wiki-page
status: active
created: 2026-05-22
last_confirmed: 2026-05-22
confidence: 0.78
quality_score: 0.86
sensitivity: internal
sources:
  - "[[sources/hafner-2022-m23-braid-orbits]]"
  - "[[sources/elkies-2013-complex-m23-polynomials]]"
  - "[[wiki/m23-trinomial-minus20-20-report]]"
entities:
  - "[[entities/projects/m23-proof-factory]]"
  - "[[entities/concepts/mathieu-group-m23]]"
  - "[[entities/concepts/branch-cycle-class-vector]]"
  - "[[entities/concepts/braid-orbit]]"
  - "[[entities/concepts/belyi-map]]"
  - "[[entities/concepts/galois-candidate-search]]"
relationships:
  - target: "[[wiki/m23-trinomial-minus20-20-report]]"
    type: "supersedes"
    confidence: 0.70
    note: "Moves the search from sparse trinomials toward literature-constrained generators."
  - target: "[[entities/concepts/branch-cycle-class-vector]]"
    type: "uses"
    confidence: 0.86
  - target: "[[entities/concepts/belyi-map]]"
    type: "uses"
    confidence: 0.82
supersedes: []
superseded_by: []
review_after: 2026-06-22
---

# M23 Literature Constraint Map

## Summary

The first trinomial search shows that broad sparse-polynomial boxes are quickly filtered out. The relevant literature points to a stronger next direction: construct candidates from branch-cycle and Belyi-map constraints, then use finite-field or p-adic solving before rational reconstruction.

## Current Boundary

Hafner states that `M23/Q` remains open: no polynomial in `Z[x]` with Galois group `M23` over `Q` is known in that source. The Kluners-Malle database also lists polynomials for all transitive groups up to degree 23 except `M23`.

This means a found candidate cannot be treated as routine. It needs independent Magma/GAP verification and a written proof.

## Useful Constraints

### Hafner Braid-Orbit Constraints

- Length-3 rational class vectors have not produced a suitable `M23/Q(t)` realization in the cited searches.
- Length-4 class vectors are the natural next layer.
- `(14A,2A,2A,2A)` and `(15A,2A,2A,2A)` produce geometric `M23` realizations over `Q(sqrt(-7))(v,t)` and `Q(sqrt(-15))(v,t)`, respectively.
- Symmetric rational length-4 class vectors `(3A)^4`, `(4A)^4`, `(5A)^4`, `(6A)^4`, and `(8A)^4` are identified as potentially useful search objects, though not known to solve `M23/Q`.

### Elkies Equation-System Constraints

Elkies computes complex degree-23 polynomials with monodromy `M23` over `C(t)`. The useful computational shape is:

```text
P = P2^2 * P3 * P4^4 = P7 * P8^2 + lambda
```

where the `Pi` are coprime monic polynomials of degrees indicated by their subscripts. The branch-cycle structure uses the M23 cycle types:

- `2^8 1^7`
- `4^4 2^2 1^3`
- `23`

The derivative constraint reduces the nonlinear system. The search method is finite-field approximation, p-adic Newton iteration, lattice recognition, and exact verification.

## Implication for the Next Generator

The next generator should not be another coefficient grid. It should be an equation-system experiment:

1. Represent monic factor polynomials `P2`, `P3`, `P4`, `P7`, and `P8`.
2. Normalize by translation/scaling to remove redundant variables.
3. Build coefficient equations from `P2^2 * P3 * P4^4 - P7 * P8^2 - lambda = 0`.
4. Solve modulo small primes first.
5. Feed surviving finite-field solutions into lifting/reconstruction experiments.
6. Verify any reconstructed degree-23 polynomial with the existing local M23 filter and then Magma/GAP.

## Implemented Scaffold

The first executable scaffold is `experiments/m23/src/m23verify/belyi.py`. It currently:

- Represents monic factors `P2`, `P3`, `P4`, `P7`, and `P8` by descending non-leading coefficients.
- Computes the 24 coefficient residuals of `P2^2 * P3 * P4^4 - P7 * P8^2 - lambda` modulo a prime.
- Detects whether a supplied factor tuple solves the identity modulo that prime.

This is not yet a solver. It is the arithmetic kernel that a finite-field search or Newton-lifting experiment can call.

The next layer is now filed at [[wiki/m23-elkies-finite-field-solver]]. It adds a bounded search command that enumerates left factors over `GF(p)`, derives right factors by square-divisor factorization, verifies the identity residual, and can enforce the derivative relation away from characteristic 23.

## Confidence

Confidence is high that literature-constrained equation systems are more relevant than the completed trinomial box. Confidence is low that a first implementation will reach a rational `M23/Q` polynomial; the point is to make the next failure more mathematically informative.
