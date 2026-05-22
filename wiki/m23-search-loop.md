---
type: wiki-page
status: active
created: 2026-05-22
last_confirmed: 2026-05-22
confidence: 0.74
quality_score: 0.84
sensitivity: internal
sources:
  - "[[wiki/m23-proof-factory]]"
  - "[[wiki/m23-verification-standard]]"
  - "[[experiments/m23/README]]"
entities:
  - "[[entities/projects/m23-proof-factory]]"
  - "[[entities/concepts/mathieu-group-m23]]"
  - "[[entities/concepts/galois-candidate-search]]"
  - "[[entities/concepts/galois-verification-pipeline]]"
relationships:
  - target: "[[wiki/m23-proof-factory]]"
    type: "supports"
    confidence: 0.88
    note: "Implements the iterative candidate-test-record-update loop."
  - target: "[[wiki/m23-verification-standard]]"
    type: "depends-on"
    confidence: 0.90
    note: "Uses the local verification report as the scoring and rejection gate."
  - target: "[[entities/concepts/galois-candidate-search]]"
    type: "uses"
    confidence: 0.86
supersedes: []
superseded_by: []
review_after: 2026-06-22
---

# M23 Search Loop

## Summary

The M23 search loop is a resumable batch runner for candidate polynomials. It generates candidates from a structured family, runs the local M23 verification filter, writes each result to a JSONL ledger, skips previously tested candidates, and returns the next surviving candidate for external Magma/GAP verification.

## Current Implementation

The first implemented family is the low-height trinomial family:

```text
x^23 + a*x + b
```

The runner orders candidates by small coefficient height first. It is intentionally conservative: this is a reproducible search filter, not a proof engine.

## Command

```powershell
.\.venv\Scripts\python experiments/m23/scripts/search_batch.py --family trinomial --a-range=-20:20 --b-range=-20:20 --primes 2,3,5,7,11 --max-candidates 100
```

By default, results are appended to:

```text
experiments/m23/reports/candidate_ledger.jsonl
```

## Loop Semantics

1. Read the ledger and build a set of candidates resolved for the requested prime set.
2. Generate the next unseen candidates from the selected family.
3. Run the local verification report for each candidate.
4. Append a ledger entry with classification, reasons, summary data, and modular factorization fingerprints.
5. Stop on the first `needs_external_group_verification` survivor unless `--continue-on-survivor` is supplied.
6. Use the ledger as search memory for later batches.

A rejected candidate is considered resolved even if it was rejected by a smaller prime set. A weak survivor is not considered resolved for a stronger batch unless its ledger entry already covers all requested primes. This lets the loop change verification strength without losing near misses.

Single-candidate escalation can also write to the same ledger:

```powershell
.\.venv\Scripts\python experiments/m23/scripts/verify_candidate.py "x^23 - 2*x - 4" --primes 2,3,5,7,11,13,17,19,23,29,31 --ledger experiments/m23/reports/candidate_ledger.jsonl --generator escalation
```

The ledger can be summarized with:

```powershell
.\.venv\Scripts\python experiments/m23/scripts/ledger_summary.py
```

## Meaning of a Survivor

A survivor is not a solution. It only means the candidate passed the current local filters. A survivor still needs external group computation, subgroup exclusion, and a written proof that the splitting field over `Q` has Galois group `M23`.

The first live batch on 2026-05-22 produced `x^23 - 2*x - 4` as a local survivor against primes `2,3,5`. Escalating to primes `2,3,5,7,11,13,17,19,23,29,31` rejected it because seven good primes had cycle types not present in the degree-23 action of `M23`.

The completed low-height trinomial scan over `-10 <= a <= 10`, `-10 <= b <= 10`, excluding zero `a` and `b`, resolved 400 unique candidates. By latest ledger status, all 400 are rejected under the current local filters; there are no active survivors in this range.

The expanded scan over `-20 <= a <= 20`, `-20 <= b <= 20`, excluding zero `a` and `b`, resolved 1600 unique candidates against primes `2,3,5,7,11`. By latest ledger status, all 1600 are rejected; there are no active survivors in this range. The ledger contains 1601 entries because `x^23 - 2*x - 4` first appeared as a weak survivor and was later superseded by a stronger rejection entry.

See [[wiki/m23-ledger-summary]] and [[wiki/m23-trinomial-minus20-20-report]] for the current failure-frequency snapshot.

## Next Improvements

- Add more candidate families beyond trinomials.
- Add learned scoring from rejection reasons.
- Add family-level summaries that identify dense failure zones.
- Add Magma/GAP escalation for survivors.
- Add a Markdown batch report generator for vault filing.

## Confidence

Confidence is high that the loop records and resumes local filtering correctly. Confidence is low that the current trinomial family is mathematically promising; its main value is exercising the machine-assisted search process. The `[-20,20]` batch result is a computational observation from the local harness, not a theorem about the broader trinomial family.
