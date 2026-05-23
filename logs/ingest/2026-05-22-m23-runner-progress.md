---
type: ingest-log
status: active
created: 2026-05-22
last_confirmed: 2026-05-22
confidence: 0.88
quality_score: 0.84
sensitivity: internal
source: "M23 Belyi batch runner progress indicator"
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

# M23 Runner Progress Log

## Actions

- Added per-batch progress output to `experiments/m23/scripts/run_belyi_batches.py`.
- Kept the final machine-readable summary on stdout.
- Printed progress lines to stderr so PowerShell shows activity during long local runs.
- Added `--quiet` to suppress progress output for scripted runs.
- Added CLI tests for visible progress and quiet mode.
- Updated [[experiments/m23/README]], [[wiki/m23-elkies-finite-field-solver]], and [[index]].

## Privacy Filtering

- No sensitive or private material was included.
