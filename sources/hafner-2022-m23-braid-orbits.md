---
type: source
status: active
created: 2026-05-22
last_confirmed: 2026-05-22
confidence: 0.86
quality_score: 0.82
sensitivity: internal
source_kind: paper
origin: "https://arxiv.org/abs/2202.08222"
owner: "Frank Hafner"
entities:
  - "[[entities/concepts/mathieu-group-m23]]"
  - "[[entities/concepts/branch-cycle-class-vector]]"
  - "[[entities/concepts/braid-orbit]]"
relationships:
  - target: "[[wiki/m23-literature-constraint-map]]"
    type: "supports"
    confidence: 0.88
supersedes: []
superseded_by: []
review_after: 2026-06-22
---

# Hafner 2022 M23 Braid Orbits

## Source Metadata

- Origin: [arXiv:2202.08222](https://arxiv.org/abs/2202.08222)
- Title: Braid orbits and the Mathieu group `M23` as Galois group
- Author: Frank Hafner
- Date: 2022
- Sensitivity: public

## Normalized Content

This paper surveys the state of attempts to realize `M23` as a Galois group over `Q` using rigidity and braid actions. It states that the inverse Galois problem over `Q` remains unsolved for `M23`.

Key normalized claims:

- No polynomial in `Z[x]` with Galois group `M23` over `Q` is known as of the paper.
- No suitable length-3 rational class vector for `M23/Q(t)` was found in the cited searches.
- Length-4 braid orbit searches are central to the known approach.
- The class vectors `(14A,2A,2A,2A)` and `(15A,2A,2A,2A)` yield geometric `M23` realizations over quadratic base fields `Q(sqrt(-7))(v,t)` and `Q(sqrt(-15))(v,t)`, not over `Q`.
- Symmetric rational class vectors such as `(3A,3A,3A,3A)`, `(4A,4A,4A,4A)`, `(5A,5A,5A,5A)`, `(6A,6A,6A,6A)`, and `(8A,8A,8A,8A)` are discussed as small-orbit search candidates.

## Initial Observations

- The paper is more useful as a search-boundary and constraint source than as a direct polynomial source.
- The open `Q` status means any candidate over `Q` needs unusually careful verification.
- The quadratic-field realizations may be useful for descent or specialization experiments, but are not themselves a solution to the current `Z[x]` target.

## Candidate Entities

- [[entities/concepts/branch-cycle-class-vector]]
- [[entities/concepts/braid-orbit]]
- [[entities/concepts/belyi-map]]

## Candidate Relationships

- [[entities/concepts/braid-orbit]] supports [[entities/concepts/galois-candidate-search]].
- [[entities/concepts/branch-cycle-class-vector]] constrains [[entities/concepts/galois-candidate-search]].
