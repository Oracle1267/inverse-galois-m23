---
type: wiki-page
status: active
created: 2026-05-22
last_confirmed: 2026-05-22
confidence: 0.72
quality_score: 0.86
sensitivity: internal
sources:
  - "[[wiki/riemann-hypothesis-investigation-map]]"
entities:
  - "[[entities/projects/m23-proof-factory]]"
  - "[[entities/concepts/inverse-galois-problem]]"
  - "[[entities/concepts/mathieu-group-m23]]"
  - "[[entities/concepts/galois-candidate-search]]"
  - "[[entities/concepts/galois-verification-pipeline]]"
relationships:
  - target: "[[entities/projects/m23-proof-factory]]"
    type: "supports"
    confidence: 0.90
  - target: "[[entities/concepts/galois-candidate-search]]"
    type: "uses"
    confidence: 0.86
  - target: "[[entities/concepts/galois-verification-pipeline]]"
    type: "depends-on"
    confidence: 0.90
supersedes: []
superseded_by: []
review_after: 2026-06-22
---

# M23 Proof Factory

## Summary

The M23 proof factory is a proposed AI-assisted research loop for the inverse Galois problem target: find a degree-23 polynomial in `Z[x]` whose splitting field over `Q` has Galois group `M23`, with coefficients under 100 decimal digits.

This is not a solved target. As of sources checked on 2026-05-22, `M23/Q` remains open.

## Core Loop

```text
literature map
-> candidate family
-> constraints
-> parameter search
-> verification gates
-> failure classification
-> constraint update
-> next search
```

## Why This Is AI-Shaped

A human can reason about one branch at a time. This project aims to maintain many branches:

- which families were tried
- which parameter ranges failed
- which modular signatures appeared
- which candidates collapsed to `S23`, `A23`, or smaller groups
- which failures imply new constraints
- which near misses deserve escalation

The AI role is memory, triage, script generation, and disciplined bookkeeping. The proof still has to be mathematical and mechanically checkable.

## Candidate Generation

Candidate families should be structured, not random:

- known covers related to `M24`, `M22`, Higman-Sims, or Mathieu groups
- rigidity and braid-orbit branch-cycle data
- ramification-constrained templates
- modular factorization fingerprints
- point-stabilizer and subfield constructions

## Verification Gates

For each candidate polynomial:

1. Check it is primitive, squarefree, and degree 23.
2. Check irreducibility over `Q`.
3. Compute discriminant data where feasible.
4. Factor modulo many good primes.
5. Convert modular factorization degrees to cycle types.
6. Compare cycle types against the degree-23 action of `M23`.
7. Rule out incompatible transitive subgroups.
8. Rule out `S23`, `A23`, and wrong overgroups.
9. Produce a human-readable proof note.
10. Recheck in a second system when feasible.

## Failure Ledger

Every failed candidate or family should be classified:

- reducible
- degenerate
- wrong discriminant behavior
- impossible cycle type
- group too large
- group too small
- imprimitive or wrong transitive group
- computationally inconclusive
- structurally impossible family

Failures are useful only when they update future constraints.

## Initial Experiments

### 1. Known Boundary

Build local tables:

- `M23 = 23T5`
- degree-23 conjugacy class cycle types
- maximal subgroup data
- allowable modular factorization patterns

### 2. Verification Harness

Build a Magma/GAP/Sage checker before searching:

- polynomial input
- irreducibility
- discriminant
- modular factorizations
- possible group fingerprints
- report output

### 3. Literature Reconstruction

Ingest Hafner's braid-orbit work and related references. Record known failed class vectors, branch-cycle attempts, and heuristics.

### 4. Search Batch 1

Run a small search from a single literature-guided family. The purpose is not volume; it is proving the loop works.

### 5. Search Report

Create a vault report:

- candidates generated
- gates passed
- failure distribution
- constraints learned
- next batch recommendation

## External References

- [Epoch AI: Inverse Galois](https://epoch.ai/frontiermath/open-problems/inverse-galois)
- [Kluners-Malle Galois database](https://galoisdb.math.uni-paderborn.de/)
- [Hafner, Braid orbits and the Mathieu group M23 as Galois group](https://arxiv.org/abs/2202.08222)
- [Zywina, Inverse Galois problem for small simple groups](https://pi.math.cornell.edu/~zywina/papers/smallGalois.pdf)
- [LMFDB: Galois group 23T5](https://www.lmfdb.org/GaloisGroup/23T5)

## Confidence

Confidence is moderate for the process design and low for the chance that any first search batch finds a solution. The value is in making the search reproducible, cumulative, and inspectable.
