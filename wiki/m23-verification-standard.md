---
type: wiki-page
status: active
created: 2026-05-22
last_confirmed: 2026-05-22
confidence: 0.76
quality_score: 0.84
sensitivity: internal
sources:
  - "[[wiki/m23-proof-factory]]"
entities:
  - "[[entities/projects/m23-proof-factory]]"
  - "[[entities/concepts/galois-verification-pipeline]]"
  - "[[entities/concepts/mathieu-group-m23]]"
relationships:
  - target: "[[wiki/m23-proof-factory]]"
    type: "supports"
    confidence: 0.88
supersedes: []
superseded_by: []
review_after: 2026-06-22
---

# M23 Verification Standard

## Summary

The local harness is a filter, not a proof. A candidate polynomial survives phase one only when it has the right degree, coefficient bound, irreducibility, nonzero discriminant, and good-prime factorization types compatible with M23.

## Local Gates

1. Polynomial parses as an element of `Z[x]`.
2. Degree is 23.
3. Maximum coefficient length is at most 99 decimal digits.
4. Polynomial is irreducible over `Q`.
5. Discriminant is nonzero.
6. Good-prime factorizations produce cycle types present in the degree-23 action of M23.

## External Gates

1. Magma or GAP confirms the relevant group fingerprints.
2. A subgroup-exclusion argument rules out all remaining transitive subgroups.
3. The proof explains why the Galois group is exactly M23 rather than a larger or smaller group.

## Non-Claims

Passing the Python harness does not prove the Galois group is M23. It means only that the candidate deserves stronger verification.
