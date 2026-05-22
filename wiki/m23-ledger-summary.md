---
type: wiki-page
status: active
created: 2026-05-22
last_confirmed: 2026-05-22
confidence: 0.78
quality_score: 0.84
sensitivity: internal
sources:
  - "[[wiki/m23-search-loop]]"
  - "[[experiments/m23/README]]"
entities:
  - "[[entities/projects/m23-proof-factory]]"
  - "[[entities/concepts/galois-candidate-search]]"
  - "[[entities/concepts/galois-verification-pipeline]]"
relationships:
  - target: "[[wiki/m23-search-loop]]"
    type: "supports"
    confidence: 0.88
    note: "Summarizes the search ledger produced by the loop."
  - target: "[[entities/concepts/galois-candidate-search]]"
    type: "uses"
    confidence: 0.82
supersedes: []
superseded_by: []
review_after: 2026-06-22
---

# M23 Ledger Summary

## Summary

`experiments/m23/scripts/ledger_summary.py` summarizes the M23 candidate ledger so the search can learn from failures. It reads JSONL entries, keeps only the latest status per polynomial for outcome counts, and reports active survivors, superseded entries, rejection reasons, first rejecting good primes, and incompatible cycle-type frequencies.

## Command

```powershell
.\.venv\Scripts\python experiments/m23/scripts/ledger_summary.py
```

## Current Ledger Snapshot

As of 2026-05-22, the ledger contains:

- 1601 entries.
- 1600 unique polynomial candidates.
- 1600 latest-status rejections.
- 0 active survivors.
- 1 superseded entry, from the weak-survivor then stronger-rejection sequence for `x^23 - 2*x - 4`.

The generated Markdown batch report is [[experiments/m23/reports/2026-05-22-trinomial-minus20-20-summary]]. A vault interpretation is filed at [[wiki/m23-trinomial-minus20-20-report]].

## First Rejecting Good Prime Counts

For the current `[-20,20]` trinomial sweep, the first incompatible good prime in each latest report was:

- `p = 5`: 554 candidates.
- `p = 3`: 420 candidates.
- `p = 2`: 400 candidates.
- `p = 7`: 190 candidates.
- `p = 11`: 30 candidates.

This suggests the current local filters are mostly rejecting the trinomial family very early; expanding the same family may produce many more fast rejections but little new structure unless the generator changes.

## Dominant Incompatible Cycle Types

The highest-frequency incompatible cycle types in the current ledger are:

- `p = 2`, cycle type `[13, 8, 2]`: 400 occurrences.
- `p = 3`, cycle type `[9, 7, 5, 2]`: 392 occurrences.
- `p = 11`, cycle type `[22, 1]`: 360 occurrences.
- `p = 11`, cycle type `[21, 2]`: 278 occurrences.
- `p = 5`, cycle type `[15, 6, 2]`: 256 occurrences.
- `p = 5`, cycle type `[22, 1]`: 256 occurrences.

## Interpretation

This is negative evidence for the small-height trinomial family `x^23 + a*x + b`, not for the M23 inverse Galois target in general. The next search should use the summary as a steering signal: either change candidate family or add constraints that avoid the most frequent incompatible cycle signatures.
