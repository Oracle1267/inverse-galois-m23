---
type: ingest-log
status: active
created: 2026-05-22
last_confirmed: 2026-05-22
confidence: 0.78
quality_score: 0.82
sensitivity: internal
source: "M23 literature constraint ingest"
sources:
  - "[[sources/hafner-2022-m23-braid-orbits]]"
  - "[[sources/elkies-2013-complex-m23-polynomials]]"
entities:
  - "[[entities/concepts/branch-cycle-class-vector]]"
  - "[[entities/concepts/braid-orbit]]"
  - "[[entities/concepts/belyi-map]]"
relationships:
  - target: "[[wiki/m23-literature-constraint-map]]"
    type: "supports"
    confidence: 0.86
supersedes: []
superseded_by: []
review_after: 2026-06-22
---

# M23 Literature Constraints Ingest Log

## Source

- Source: Hafner 2022 and Elkies 2013.
- Source kind: public papers.
- Sensitivity: internal synthesis from public sources.

## Actions

- Created source pages for Hafner 2022 and Elkies 2013.
- Created concept entities for branch-cycle class vectors, braid orbits, and Belyi maps.
- Created [[wiki/m23-literature-constraint-map]].
- Added machine-readable notes in `experiments/m23/data/m23_literature_constraints.json`.
- Added `experiments/m23/src/m23verify/belyi.py` as the first tested arithmetic scaffold for the Elkies-style identity.
- Added `experiments/m23/scripts/solve_belyi_modp.py` as a bounded finite-field search command.
- Added derivative residual checking and the `--require-derivative` CLI flag.
- Added translation normalization checking and the `--require-translation-normalized` CLI flag.
- Added coprime-first enumeration through the `--coprime-first` CLI flag.
- Added Belyi solver report output through the `--out`, `--markdown-out`, and `--title` CLI flags.
- Generated [[experiments/m23/reports/2026-05-22-belyi-gf5-prefix]] as the first finite-field Belyi Markdown report artifact.
- Created [[wiki/m23-elkies-finite-field-solver]].
- Created [[wiki/m23-belyi-gf5-prefix-report]].
- Updated [[index]].

## Entities Created or Updated

- [[entities/concepts/branch-cycle-class-vector]]
- [[entities/concepts/braid-orbit]]
- [[entities/concepts/belyi-map]]

## Wiki Pages Created or Updated

- [[wiki/m23-literature-constraint-map]]
- [[wiki/m23-elkies-finite-field-solver]]
- [[wiki/m23-belyi-gf5-prefix-report]]
- [[index]]

## Privacy Filtering

- No sensitive or private material was included.

## Confidence and Quality Notes

- Confidence is high for the broad direction: branch-cycle and Belyi-map constraints are more relevant than wider trinomial boxes.
- Confidence is moderate for individual normalized claims; exact computational details should be rechecked directly against the papers before proof use.

## Follow-Up

- Add stronger normalized left-factor generation and run longer report-producing searches.
- Compare equation-system survivors against the existing modular M23 filter.
