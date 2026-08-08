# Riemann

This repository is a Markdown-first research vault and codebase for the M23 inverse Galois project.

The short version: the project was built to organize and automate a proof-factory workflow for searching for a degree-23 polynomial over `Z[x]` whose Galois group is `M23`. It combines:

- a local verification harness for candidate polynomials,
- resumable batch search loops,
- finite-field and Belyi-style exploration,
- timeout review and external Groebner escalation,
- and a vault of durable notes, logs, and synthesized results.

## What lives here

- `experiments/m23/` holds the runnable Python tooling, scripts, tests, and experiment reports.
- `wiki/`, `entities/`, `logs/`, `sources/`, and `memory/` hold the Obsidian-style knowledge vault around those experiments.
- `docs/` contains implementation plans and other project notes.
- `index.md` is the main navigation map for the vault.

## What the project is for

The project is not just a one-off computation. It is a repeatable workflow for:

1. generating candidate M23-related objects,
2. checking them locally,
3. preserving rejects and survivors,
4. escalating ambiguous cases to stronger algebra systems,
5. and recording the result in a durable, cited knowledge graph.

That makes it useful both as an experiment log and as an engineering system for continuing the search later without losing context.

## Current shape

The M23 work currently includes:

- candidate ledgering and resumable search,
- finite-field and Belyi-map exploration,
- Groebner-based timeout handling,
- Docker-backed Sage/Singular checks,
- and a continuous continuation runner for the `GF(7)` branch search.

The repository also keeps the surrounding vault structure used to track confidence, provenance, and supersession of results.

## Getting started

From the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install --upgrade pip
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python -m pytest experiments/m23/tests -q
```

For the M23 experiment notes and workflow details, see [experiments/m23/README.md](experiments/m23/README.md).

## Notes

Some of the repository content is intentionally archival: it preserves raw results, checkpoints, and intermediate mathematical states so later runs can be compared against earlier ones instead of overwriting them.
