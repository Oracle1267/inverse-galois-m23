# M23 Proof Factory Design

## Goal

Design a reproducible research process for the inverse Galois problem target:

```text
Find f(x) in Z[x], deg(f) = 23, Gal(f/Q) = M23,
with all coefficients shorter than 100 decimal digits.
```

This design does not claim a solution. As of sources checked on 2026-05-22, M23 over Q remains an open case.

## Research Premise

The useful AI leverage is not brute force over all degree-23 polynomials. The useful leverage is a memory-backed proof factory:

```text
literature map
-> candidate family
-> constraints
-> parameter search
-> Galois fingerprint tests
-> failure classification
-> updated constraints
-> repeat
```

The process should either produce a verified M23 polynomial or a publishable failed-search atlas that narrows the search.

## Current Evidence

- Epoch AI lists the exact prompt as an unsolved FrontierMath open problem and notes that M23 is the last sporadic simple group for which no polynomial is known.
- The Kluners-Malle number field database says it contains polynomials for all transitive groups up to degree 23 except M23.
- Hafner's 2022 paper says M23/Q remains open after braid-orbit and rigidity investigations.
- Zywina's 2025 small simple groups note lists M23 among small simple groups still not known to occur over Q.

## Scope

In scope:

- Build a search process.
- Reconstruct known attempts.
- Define candidate-generation families.
- Define verification gates in Magma/GAP/Sage/PARI.
- Maintain a failure ledger.
- Produce reproducible scripts and notes in later implementation.

Out of scope for this design:

- Claiming a new polynomial without proof.
- Blind random search over all degree-23 polynomials.
- Publishing or submitting anything without expert review.
- Treating computational evidence alone as proof.

## Architecture

### 1. Research Map

Purpose: avoid repeating known dead branches.

Inputs:

- Hafner on braid orbits and rigidity for M23.
- Kluners-Malle database coverage.
- Known M22, M24, and related sporadic realizations.
- Group-theoretic data for M23 and transitive group 23T5.

Output:

- A vault page listing known approaches, branch-cycle patterns, failures, near misses, and reusable constraints.

### 2. Candidate Family Generator

Purpose: produce structured polynomial families instead of random polynomials.

Initial family sources:

- Specializations of known covers related to M24, M22, Higman-Sims, or Mathieu groups.
- Rigidity or braid-orbit branch cycle classes.
- Polynomials with prescribed ramification patterns.
- Low-height templates constrained by modular factorization fingerprints.
- Subfield or point-stabilizer constructions where a larger group contains M23-like stabilizers.

Output:

- Parameterized polynomial families with metadata.

### 3. Constraint Engine

Purpose: translate desired M23 behavior into search filters.

Constraint types:

- Degree 23 and irreducible over Q.
- Coefficient digit bound under 100 digits.
- Modular factorization types matching cycle types present in M23.
- Exclusion signatures that rule out S23, A23, and other transitive subgroups.
- Discriminant constraints.
- Ramification patterns compatible with selected branch cycles.
- Avoidance of degenerations and repeated roots.

Output:

- Search jobs with explicit parameter ranges and acceptance filters.

### 4. Verification Pipeline

Purpose: separate plausible candidates from noise.

Verification gates:

1. Primitive integer polynomial.
2. Squarefree and irreducible over Q.
3. Degree 23.
4. Discriminant computed and factored when feasible.
5. Factorization modulo many good primes.
6. Cycle-type fingerprint compatible with M23.
7. Candidate group contained in or equal to 23T5 where possible.
8. Other transitive degree-23 groups ruled out.
9. Independent verification in at least two systems when feasible.
10. Proof note written with exact primes, factorization types, and subgroup exclusions.

Output:

- Candidate status: rejected, needs more tests, strong candidate, or proof-ready.

### 5. Failure Classifier

Purpose: turn failed computation into knowledge.

Failure classes:

- Wrong degree or reducible.
- Degenerate specialization.
- Wrong discriminant behavior.
- Modular factorization shows impossible cycle type.
- Galois group too large, usually S23 or A23.
- Galois group too small or imprimitive.
- Family structurally cannot produce M23.
- Inconclusive due to computational limits.

Output:

- Failure ledger entries that update constraints and prevent repeated work.

### 6. Constraint Updater

Purpose: use failures to improve future searches.

Actions:

- Tighten parameter ranges.
- Add forbidden congruence classes.
- Promote promising local signatures.
- Retire unproductive families.
- Split an over-broad family into subfamilies.
- Escalate theoretical questions when computation repeatedly hits the same wall.

Output:

- Next search batch.

## Data Flow

```text
source literature
-> research map
-> candidate family page
-> search job
-> raw candidate list
-> verification report
-> failure ledger or proof note
-> updated constraints
-> next search job
```

## Proof Standard

A final candidate must be accompanied by:

- The polynomial in Magma syntax.
- A proof of irreducibility.
- A proof that the Galois group embeds into the degree-23 action of M23 or otherwise cannot exceed M23.
- Modular factorization data showing required cycle types.
- A subgroup exclusion argument proving no proper transitive subgroup remains possible.
- A proof excluding A23/S23 and other larger candidates.
- Reproducible Magma/GAP scripts.
- A human-readable proof note.

## Initial Experiment Sequence

### Experiment 1: Rebuild the Known Boundary

Reproduce known database facts:

- Confirm M23 is transitive group 23T5 in LMFDB/GAP/Magma naming.
- List conjugacy classes and cycle types in the degree-23 action.
- List maximal subgroups relevant to subgroup exclusion.
- Create a local table of allowable factorization patterns modulo good primes.

### Experiment 2: Verification Harness

Before generating new candidates, build the checker:

- Input: polynomial string.
- Output: irreducibility, discriminant, modular factorization table, cycle types, and possible transitive groups.
- Test on known M22 or other nearby examples to ensure the harness catches expected groups.

### Experiment 3: Literature Family Reconstruction

Reconstruct candidate families from Hafner and related work:

- Encode branch-cycle class vectors.
- Identify families that failed and why.
- Extract constraints worth reusing.

### Experiment 4: Search Batch 1

Run a small, reproducible parameter search from one literature-guided family.

Acceptance criteria:

- Degree 23.
- Irreducible.
- Coefficients under 100 digits.
- At least three distinct good-prime cycle types compatible with M23.
- No immediate evidence for S23 or A23.

### Experiment 5: Failure Atlas

Summarize the batch:

- How many candidates generated.
- How many passed each gate.
- Most common failure class.
- New constraints learned.
- Next recommended family or parameter adjustment.

## Artifacts

Planned vault artifacts:

- `wiki/m23-proof-factory.md`
- `wiki/m23-known-attempts-map.md`
- `wiki/m23-verification-standard.md`
- `entities/projects/m23-proof-factory.md`
- `memory/working/YYYY-MM-DD-m23-search-batch-*.md`
- `logs/ingest/YYYY-MM-DD-m23-*.md`
- `logs/query/YYYY-MM-DD-m23-*.md`

Planned code artifacts for later implementation:

- `experiments/m23/README.md`
- `experiments/m23/candidates/`
- `experiments/m23/reports/`
- `experiments/m23/magma/verify_candidate.m`
- `experiments/m23/gap/group_fingerprints.g`
- `experiments/m23/search/`

## Risks

- The problem may require theory not captured by search.
- Candidate families may mostly produce S23/A23.
- Full Galois group computation in degree 23 can be expensive.
- Published claims require expert review.
- AI can generate plausible but invalid algebraic arguments, so verification must be mechanical and redundant.

## Success Criteria

Minimum useful success:

- A reproducible verification harness.
- A sourced known-attempts map.
- A failure ledger that prevents duplicate search.
- At least one completed search batch with interpretable results.

Major success:

- A candidate polynomial that passes all computational filters and has a credible proof strategy.

Ultimate success:

- A degree-23 polynomial in Z[x] with coefficients under 100 digits, plus a rigorous proof that its splitting field over Q has Galois group M23.

## Review Notes

This design should be reviewed before implementation. The first implementation plan should focus on building the verification harness and known-boundary tables before any large search.
