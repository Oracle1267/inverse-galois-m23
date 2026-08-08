# Inverse Galois Search for M23
	​
This repository is a Markdown-first research vault and codebase for the M23 inverse Galois project.

The short version: the project was built to organize and automate a proof-factory workflow for searching for a degree-23 polynomial over `Z[x]` whose Galois group is `M23`. It combines:

- a local verification harness for candidate polynomials,
- resumable batch search loops,
- finite-field and Belyi-style exploration,
- timeout review and external Groebner escalation,
- and a vault of durable notes, logs, and synthesized results.

## Why M23 Matters

`M23` is one of the sporadic Mathieu groups, a small set of exceptional finite simple groups that do not belong to the usual infinite families. That makes it mathematically interesting on its own.

Explicitly realizing `M23` as a Galois group over `Q` is hard because you are not just asking for an abstract group to exist in theory. You are asking for a concrete polynomial with exactly that symmetry, and then checking that the polynomial really has the right arithmetic and local behavior. The search space is large, the candidates are subtle, and many promising-looking branches fail only after fairly deep verification.

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

## Results So Far

The project has tested several connected search spaces and verification layers:

- a resumable trinomial batch search over degree-23 candidates,
- finite-field `GF(5)` and `GF(7)` Belyi-style searches,
- branch search and consistency scoring on the best `GF(7)` survivors,
- focused timeout review for Groebner-heavy branches,
- and external Sage/Singular Groebner checks on the quarantined timeout branches.

What has been eliminated:

- many candidate polynomials in the raw trinomial search,
- a number of low-scoring branch-search frontiers,
- and the idea that the three quarantined timeout branches were immediate contradictions under the exported six-equation Groebner screen.

What remains:

- no certified `M23` realization yet,
- no complete proof that the surviving `GF(7)` continuation path succeeds,
- and no resolution of the remaining partial-lift / continuation question.

The current live `GF(7)` continuation run is still a search, not a proof. It has produced partial survivors and checkpoints, but not a final exact-complete certificate.

## Current shape

The M23 work currently includes:

- candidate ledgering and resumable search,
- finite-field and Belyi-map exploration,
- Groebner-based timeout handling,
- Docker-backed Sage/Singular checks,
- and a continuous continuation runner for the `GF(7)` branch search.

The repository also keeps the surrounding vault structure used to track confidence, provenance, and supersession of results.

## My Role and Use of AI

I directed the research workflow, defined the verification architecture, evaluated the outputs, and used AI assistance to implement and maintain the tooling around the search.

That means the project reflects a human-led mathematical investigation with AI-assisted engineering support. It does not claim that I personally originated all of the underlying mathematics, but it does document how the workflow was designed, executed, and checked.

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
