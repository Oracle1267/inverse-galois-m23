---
type: ingest-log
status: active
created: 2026-05-22
last_confirmed: 2026-05-22
confidence: 0.78
quality_score: 0.82
sensitivity: internal
source: "local implementation session"
sources:
  - "[[wiki/m23-proof-factory]]"
  - "[[wiki/m23-verification-standard]]"
entities:
  - "[[entities/projects/m23-proof-factory]]"
  - "[[entities/concepts/galois-candidate-search]]"
  - "[[entities/concepts/galois-verification-pipeline]]"
relationships:
  - target: "[[wiki/m23-search-loop]]"
    type: "supports"
    confidence: 0.86
supersedes: []
superseded_by: []
review_after: 2026-06-22
---

# M23 Search Loop Ingest Log

## Source

- Source: local implementation and test session on 2026-05-22.
- Source kind: code and process synthesis.
- Sensitivity: internal.

## Actions

- Added a JSONL candidate ledger API.
- Added a deterministic trinomial candidate family generator.
- Added a resumable batch search runner.
- Added `experiments/m23/scripts/search_batch.py` for PowerShell-driven batches.
- Extended `experiments/m23/scripts/verify_candidate.py` so stronger single-candidate checks can append to the same JSONL ledger.
- Added tests for the ledger, candidate family generation, search loop, and CLI.
- Updated `experiments/m23/README.md` with the batch command.
- Created [[wiki/m23-search-loop]].
- Ran live batches over the low-height trinomial range `-10 <= a,b <= 10` with nonzero `a,b`.
- Recorded `x^23 - 2*x - 4` as a near miss that was rejected by wider prime checks.
- Resolved 400 unique candidates in that range; latest ledger status has no active survivors.
- Expanded the scan to `-20 <= a,b <= 20` with nonzero `a,b` against primes `2,3,5,7,11`.
- Resolved 1600 unique candidates in the expanded range; latest ledger status has no active survivors.
- Added `experiments/m23/scripts/ledger_summary.py` and `m23verify.summary`.
- Created [[wiki/m23-ledger-summary]] with the current failure-frequency snapshot.
- Generated [[experiments/m23/reports/2026-05-22-trinomial-minus20-20-summary]] as a Markdown batch report.
- Created [[wiki/m23-trinomial-minus20-20-report]] as the durable vault interpretation of the generated report.

## Entities Created or Updated

- Updated [[entities/projects/m23-proof-factory]] by implication through the new runnable workflow.
- Reused [[entities/concepts/galois-candidate-search]].
- Reused [[entities/concepts/galois-verification-pipeline]].

## Wiki Pages Created or Updated

- Created [[wiki/m23-search-loop]].
- Created [[wiki/m23-ledger-summary]].
- Created [[wiki/m23-trinomial-minus20-20-report]].
- Updated [[index]].

## Privacy Filtering

- No private or credential-like data was copied into the wiki page.

## Confidence and Quality Notes

- The implementation is tested locally as a deterministic search loop.
- The current trinomial family is exploratory and should not be treated as a likely path to M23 without stronger mathematical justification.
- The completed `[-10,10]` trinomial scan is only a local-filter result, not an exhaustive claim about all trinomials or a replacement for Magma/GAP proof work.
- The completed `[-20,20]` trinomial scan strengthens the negative evidence for this small-height trinomial region, but it is still only local filtering.

## Follow-Up

- Add family-level reports and external Magma/GAP escalation for survivors.
- Use the ledger summary to choose the next candidate family instead of only expanding trinomial height.
