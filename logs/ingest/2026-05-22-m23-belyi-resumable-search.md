---
type: ingest-log
status: active
created: 2026-05-22
last_confirmed: 2026-05-22
confidence: 0.84
quality_score: 0.86
sensitivity: internal
source: "M23 resumable Belyi search continuation"
sources:
  - "[[wiki/m23-elkies-finite-field-solver]]"
entities:
  - "[[entities/projects/m23-proof-factory]]"
  - "[[entities/concepts/belyi-map]]"
relationships:
  - target: "[[wiki/m23-belyi-gf5-contiguous-24000-report]]"
    type: "supports"
    confidence: 0.88
supersedes: []
superseded_by: []
review_after: 2026-06-22
---

# M23 Belyi Resumable Search Log

## Actions

- Added `start_left_factor_triples` support to the Belyi search API.
- Added the `--start-left-factor-triples` CLI flag for resumable batches.
- Added `derivative_first` support to derive `P8` from the derivative identity.
- Added the `--derivative-first` CLI flag.
- Added `derive_lambda` support to derive lambda from the remainder modulo `P8^2`.
- Added the `--derive-lambda` CLI flag.
- Added tests for the Python API and CLI behavior.
- Ran contiguous `GF(5)` batches through 24,000 tested triples.
- Created [[wiki/m23-belyi-gf5-contiguous-24000-report]].
- Updated [[wiki/m23-elkies-finite-field-solver]], [[experiments/m23/README]], and [[index]].

## Result

- Contiguous `GF(5)` coverage now spans tested left-factor triples 0 through 24,000.
- No modular equation-system survivor was found.
- Later batches failed through lambda derivation: each tested triple produced no admissible constant nonzero lambda remainder.

## Privacy Filtering

- No sensitive or private material was included.

## Follow-Up

- Continue from `--start-left-factor-triples 24000`.
- Consider a batch driver if manual checkpoint commands become cumbersome.
