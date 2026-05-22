---
type: ingest-log
status: active
created: 2026-05-22
last_confirmed: 2026-05-22
confidence: 0.86
quality_score: 0.84
sensitivity: internal
source: "M23 local Belyi batch runner"
sources:
  - "[[wiki/m23-elkies-finite-field-solver]]"
entities:
  - "[[entities/projects/m23-proof-factory]]"
  - "[[entities/concepts/belyi-map]]"
relationships:
  - target: "[[wiki/m23-elkies-finite-field-solver]]"
    type: "supports"
    confidence: 0.86
supersedes: []
superseded_by: []
review_after: 2026-06-22
---

# M23 Local Batch Runner Log

## Actions

- Added `experiments/m23/scripts/run_belyi_batches.py`.
- Added tests for checkpoint report generation and stopping on a solution.
- Documented a local command for continuing the current `GF(5)` line from tested-triple offset 32,000 to 212,636.
- Updated [[wiki/m23-elkies-finite-field-solver]], [[experiments/m23/README]], and [[index]].

## Result

The Belyi search can now run locally without chat supervision. The runner writes one JSON and one Markdown report per interval, writes a summary JSON file, reuses existing interval reports by default, and stops on solution, target reached, finite exhaustion, or no progress.

## Follow-Up

- Use the runner to finish the remaining `GF(5)` interval.
- Consider a faster single-pass or multiprocessing runner if `GF(7)` needs deeper coverage.
