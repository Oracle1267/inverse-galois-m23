# M23 Experiments

This directory contains reproducible experiments for the M23 proof factory.

The first phase is a verification harness. It does not prove that a candidate has Galois group M23 by itself. It filters candidates, records arithmetic fingerprints, and emits reports that can be checked later in Magma, GAP, or Sage.

## Local Workflow

Create and populate the local virtual environment from the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install --upgrade pip
.\.venv\Scripts\python -m pip install -r requirements.txt
```

Run the Python harness:

```powershell
.\.venv\Scripts\python experiments/m23/scripts/verify_candidate.py "x^23 - x - 1" --primes 2,3,5,7,11
```

Append a single-candidate verification to the ledger:

```powershell
.\.venv\Scripts\python experiments/m23/scripts/verify_candidate.py "x^23 - 2*x - 4" --primes 2,3,5,7,11,13,17,19,23,29,31 --ledger experiments/m23/reports/candidate_ledger.jsonl --generator escalation
```

Run a resumable batch search over the current trinomial family:

```powershell
.\.venv\Scripts\python experiments/m23/scripts/search_batch.py --family trinomial --a-range=-20:20 --b-range=-20:20 --primes 2,3,5,7,11 --max-candidates 100
```

The batch search writes JSONL entries to `experiments/m23/reports/candidate_ledger.jsonl` by default. Each run skips candidates that are resolved for the requested prime set, tests the next low-height trinomials `x^23 + a*x + b`, records the local verification report, and stops when a candidate survives the local filters. A rejected candidate is resolved immediately; a weak survivor is retested when later batches request additional primes. Use `--continue-on-survivor` to keep scanning after a survivor. If a survivor later fails a stronger check, append the stronger `verify_candidate.py --ledger ...` result so the ledger preserves both the near miss and the rejection.

Summarize the candidate ledger:

```powershell
.\.venv\Scripts\python experiments/m23/scripts/ledger_summary.py
```

The summary reports latest classifications, active survivors, superseded entries, rejection reason counts, first rejecting good-prime counts, and incompatible cycle-type frequencies.

Write the same diagnosis as a Markdown report:

```powershell
.\.venv\Scripts\python experiments/m23/scripts/ledger_summary.py --markdown-out experiments/m23/reports/2026-05-22-trinomial-minus20-20-summary.md --title "M23 Trinomial [-20,20] Ledger Report"
```

The next literature-guided scaffold is the Elkies-style Belyi identity helper in `src/m23verify/belyi.py`. It checks the finite-field residual of:

```text
P2^2 * P3 * P4^4 = P7 * P8^2 + lambda
```

Run a small finite-field sanity search:

```powershell
.\.venv\Scripts\python experiments/m23/scripts/solve_belyi_modp.py --modulus 2 --fixed-p2 0,0 --fixed-p3 0,0,0 --fixed-p4 0,0,0,0 --max-solutions 1
```

Run a constrained prefix search:

```powershell
.\.venv\Scripts\python experiments/m23/scripts/solve_belyi_modp.py --modulus 5 --max-left-factor-triples 50 --max-solutions 3 --require-translation-normalized --require-coprime-left --coprime-first --require-nonzero-lambda --require-derivative
```

Run the same shape of search with normalized triples generated before the prefix budget is counted:

```powershell
.\.venv\Scripts\python experiments/m23/scripts/solve_belyi_modp.py --modulus 5 --max-left-factor-triples 500 --max-solutions 3 --require-translation-normalized --normalized-first --require-coprime-left --coprime-first --require-nonzero-lambda --require-derivative
```

Write the normalized search to JSON and Markdown artifacts:

```powershell
.\.venv\Scripts\python experiments/m23/scripts/solve_belyi_modp.py --modulus 5 --max-left-factor-triples 500 --max-solutions 3 --require-translation-normalized --normalized-first --require-coprime-left --coprime-first --require-nonzero-lambda --require-derivative --out experiments/m23/reports/2026-05-22-belyi-gf5-normalized-500.json --markdown-out experiments/m23/reports/2026-05-22-belyi-gf5-normalized-500.md --title "M23 Belyi GF(5) Normalized 500 Search"
```

Run tests:

```powershell
.\.venv\Scripts\python -m pytest experiments/m23/tests -q
```

## Directories

- `candidates/`: candidate polynomial strings and batch inputs.
- `data/`: static group and fingerprint data.
- `gap/`: GAP scripts for group data.
- `magma/`: Magma scripts for full candidate verification.
- `reports/`: JSON and Markdown reports produced by the harness.
- `scripts/`: command-line entry points.
- `src/m23verify/`: Python harness package.
- `tests/`: pytest coverage.
