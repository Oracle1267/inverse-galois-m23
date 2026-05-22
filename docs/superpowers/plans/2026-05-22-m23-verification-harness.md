# M23 Verification Harness Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the first executable layer of the M23 proof factory: a local Python harness that parses candidate polynomials, computes basic arithmetic fingerprints, compares good-prime cycle types against M23-compatible data, writes reports, and emits companion Magma/GAP scripts for stronger verification.

**Architecture:** Keep the harness small and auditable. Python/SymPy handles local checks that are available in this workspace; Magma/GAP files are generated as reproducible external-verification artifacts because those systems are not installed locally. Vault pages record the verification standard and known-boundary facts so computational output becomes durable knowledge.

**Tech Stack:** Python 3.12, SymPy, pytest, PyYAML, PowerShell. Optional external systems: Magma, GAP, Sage.

---

## Local Tool Facts

Checked on 2026-05-22:

- `python`: available.
- `sympy`: available.
- `pytest`: available.
- `yaml`: available.
- `magma`: missing.
- `gap`: missing.
- `sage`: missing.
- `pari-gp`: missing.

This plan does not require Magma/GAP/Sage to pass local tests. It creates scripts for later use where those tools exist.

## File Structure

- Create `experiments/m23/README.md`: project-specific experiment guide.
- Create `experiments/m23/data/m23_23t5_cycle_types.json`: seed table for M23-compatible cycle types in the degree-23 action.
- Create `experiments/m23/src/m23verify/__init__.py`: package exports.
- Create `experiments/m23/src/m23verify/polynomial.py`: parse Magma-like polynomial strings, compute coefficient sizes, irreducibility, discriminants, and modular factorization cycle types.
- Create `experiments/m23/src/m23verify/group_data.py`: load M23 cycle-type data and classify cycle compatibility.
- Create `experiments/m23/src/m23verify/report.py`: assemble verification reports.
- Create `experiments/m23/scripts/verify_candidate.py`: command-line entry point.
- Create `experiments/m23/magma/verify_candidate.m`: Magma verification script template.
- Create `experiments/m23/gap/group_fingerprints.g`: GAP script template for M23 action data.
- Create `experiments/m23/reports/README.md`: report directory guide.
- Create `experiments/m23/candidates/README.md`: candidate directory guide.
- Create `experiments/m23/tests/test_polynomial.py`: tests for parser and modular factorization.
- Create `experiments/m23/tests/test_group_data.py`: tests for cycle-type compatibility.
- Create `experiments/m23/tests/test_report.py`: tests for report assembly.
- Create `wiki/m23-verification-standard.md`: vault page describing what the harness proves and does not prove.
- Create `wiki/m23-known-boundary.md`: vault page for `23T5`, cycle fingerprints, and first boundary facts.
- Modify `index.md`: link new pages.
- Create `logs/ingest/2026-05-22-m23-verification-harness-plan.md`: plan ingest log.

## Task 1: Scaffold Experiment Workspace

**Files:**
- Create: `experiments/m23/README.md`
- Create: `experiments/m23/reports/README.md`
- Create: `experiments/m23/candidates/README.md`
- Create: `experiments/m23/src/m23verify/__init__.py`
- Create: `experiments/m23/tests/README.md`

- [ ] **Step 1: Create directories**

Run:

```powershell
$dirs = @(
  'experiments/m23',
  'experiments/m23/data',
  'experiments/m23/src/m23verify',
  'experiments/m23/scripts',
  'experiments/m23/tests',
  'experiments/m23/magma',
  'experiments/m23/gap',
  'experiments/m23/reports',
  'experiments/m23/candidates'
)
foreach ($dir in $dirs) { New-Item -ItemType Directory -Force -Path $dir | Out-Null }
```

Expected: no output and all directories exist.

- [ ] **Step 2: Add README files**

Create `experiments/m23/README.md`:

```markdown
# M23 Experiments

This directory contains reproducible experiments for the M23 proof factory.

The first phase is a verification harness. It does not prove that a candidate has Galois group M23 by itself. It filters candidates, records arithmetic fingerprints, and emits reports that can be checked later in Magma, GAP, or Sage.

## Local Workflow

Run the Python harness:

```powershell
python experiments/m23/scripts/verify_candidate.py "x^23 - x - 1" --primes 2,3,5,7,11
```

Run tests:

```powershell
python -m pytest experiments/m23/tests -q
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
```

Create `experiments/m23/reports/README.md`:

```markdown
# M23 Reports

Store generated verification reports here.

Each report should include the candidate polynomial, local Python checks, good-prime factorization data, M23 cycle-type compatibility, and the exact external commands needed for Magma or GAP verification.
```

Create `experiments/m23/candidates/README.md`:

```markdown
# M23 Candidates

Store candidate polynomial inputs here.

One candidate per line is preferred for batch files. A candidate is not credible until it passes the verification harness and receives independent group-theoretic checks.
```

Create `experiments/m23/tests/README.md`:

```markdown
# M23 Harness Tests

Tests cover local arithmetic behavior only. They do not certify an M23 polynomial.
```

Create `experiments/m23/src/m23verify/__init__.py`:

```python
"""Verification harness for M23 inverse Galois candidate polynomials."""
```

- [ ] **Step 3: Verify scaffold**

Run:

```powershell
Test-Path experiments/m23/src/m23verify/__init__.py
Test-Path experiments/m23/README.md
```

Expected:

```text
True
True
```

## Task 2: Add M23 Cycle-Type Data

**Files:**
- Create: `experiments/m23/data/m23_23t5_cycle_types.json`
- Create: `experiments/m23/tests/test_group_data.py`
- Create: `experiments/m23/src/m23verify/group_data.py`

- [ ] **Step 1: Write the failing group-data tests**

Create `experiments/m23/tests/test_group_data.py`:

```python
from pathlib import Path

from m23verify.group_data import M23CycleData, load_m23_cycle_data


DATA_PATH = Path(__file__).parents[1] / "data" / "m23_23t5_cycle_types.json"


def test_load_m23_cycle_data_has_basic_metadata():
    data = load_m23_cycle_data(DATA_PATH)

    assert data.group_label == "23T5"
    assert data.group_name == "M23"
    assert data.degree == 23
    assert data.order == 10200960


def test_m23_cycle_data_accepts_known_cycle_types():
    data = load_m23_cycle_data(DATA_PATH)

    assert data.is_allowed([23])
    assert data.is_allowed([11, 11, 1])
    assert data.is_allowed([7, 7, 7, 1, 1])
    assert data.is_allowed([5, 5, 5, 5, 1, 1, 1])


def test_m23_cycle_data_rejects_generic_s23_style_cycle_type():
    data = load_m23_cycle_data(DATA_PATH)

    assert not data.is_allowed([22, 1])
    assert not data.is_allowed([21, 2])
    assert not data.is_allowed([17, 6])


def test_m23_cycle_data_normalizes_input_order():
    data = M23CycleData(
        group_label="23T5",
        group_name="M23",
        degree=23,
        order=10200960,
        cycle_types=[(11, 11, 1)],
        source_urls=[],
    )

    assert data.is_allowed([1, 11, 11])
```

- [ ] **Step 2: Run tests to verify they fail before implementation**

Run:

```powershell
$env:PYTHONPATH = "experiments/m23/src"
python -m pytest experiments/m23/tests/test_group_data.py -q
```

Expected: FAIL with `ModuleNotFoundError` or missing `m23verify.group_data`.

- [ ] **Step 3: Add cycle-type JSON data**

Create `experiments/m23/data/m23_23t5_cycle_types.json`:

```json
{
  "group_label": "23T5",
  "group_name": "M23",
  "degree": 23,
  "order": 10200960,
  "status": "seed data for local filtering; verify against GAP or Magma before proof use",
  "source_urls": [
    "https://www.lmfdb.org/GaloisGroup/23T5",
    "https://galoisdb.math.uni-paderborn.de/",
    "https://arxiv.org/abs/2202.08222"
  ],
  "cycle_types": [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1],
    [3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1],
    [4, 4, 4, 4, 2, 2, 1, 1, 1],
    [5, 5, 5, 5, 1, 1, 1],
    [6, 6, 3, 3, 2, 2, 1],
    [7, 7, 7, 1, 1],
    [8, 8, 4, 2, 1],
    [11, 11, 1],
    [14, 7, 2],
    [15, 5, 3],
    [23]
  ]
}
```

- [ ] **Step 4: Implement `group_data.py`**

Create `experiments/m23/src/m23verify/group_data.py`:

```python
from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Iterable


def normalize_cycle_type(cycle_type: Iterable[int]) -> tuple[int, ...]:
    normalized = tuple(sorted((int(part) for part in cycle_type), reverse=True))
    if not normalized:
        raise ValueError("cycle type cannot be empty")
    if any(part <= 0 for part in normalized):
        raise ValueError(f"cycle type parts must be positive: {normalized}")
    return normalized


@dataclass(frozen=True)
class M23CycleData:
    group_label: str
    group_name: str
    degree: int
    order: int
    cycle_types: list[tuple[int, ...]]
    source_urls: list[str]

    def __post_init__(self) -> None:
        for cycle_type in self.cycle_types:
            if sum(cycle_type) != self.degree:
                raise ValueError(
                    f"cycle type {cycle_type} has degree {sum(cycle_type)}, expected {self.degree}"
                )

    @property
    def allowed_cycle_types(self) -> set[tuple[int, ...]]:
        return {normalize_cycle_type(cycle_type) for cycle_type in self.cycle_types}

    def is_allowed(self, cycle_type: Iterable[int]) -> bool:
        return normalize_cycle_type(cycle_type) in self.allowed_cycle_types


def load_m23_cycle_data(path: str | Path) -> M23CycleData:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    return M23CycleData(
        group_label=raw["group_label"],
        group_name=raw["group_name"],
        degree=int(raw["degree"]),
        order=int(raw["order"]),
        cycle_types=[normalize_cycle_type(item) for item in raw["cycle_types"]],
        source_urls=list(raw["source_urls"]),
    )
```

- [ ] **Step 5: Run tests to verify they pass**

Run:

```powershell
$env:PYTHONPATH = "experiments/m23/src"
python -m pytest experiments/m23/tests/test_group_data.py -q
```

Expected: `4 passed`.

## Task 3: Add Polynomial Parser and Arithmetic Fingerprints

**Files:**
- Create: `experiments/m23/tests/test_polynomial.py`
- Create: `experiments/m23/src/m23verify/polynomial.py`

- [ ] **Step 1: Write failing polynomial tests**

Create `experiments/m23/tests/test_polynomial.py`:

```python
import pytest

from m23verify.polynomial import (
    coefficient_digit_count,
    factor_degrees_mod_prime,
    parse_polynomial,
    summarize_polynomial,
)


def test_parse_magma_style_polynomial():
    poly = parse_polynomial("3*x^2 - 2*x + 1")

    assert poly.degree() == 2
    assert [int(c) for c in poly.all_coeffs()] == [3, -2, 1]


def test_parse_rejects_non_integer_coefficients():
    with pytest.raises(ValueError, match="integer coefficients"):
        parse_polynomial("x^2 + 1/2")


def test_coefficient_digit_count():
    assert coefficient_digit_count(0) == 1
    assert coefficient_digit_count(-12345) == 5


def test_factor_degrees_mod_prime_for_cubic():
    poly = parse_polynomial("x^3 - 2")
    factorization = factor_degrees_mod_prime(poly, 5)

    assert factorization.prime == 5
    assert factorization.cycle_type == (2, 1)
    assert factorization.is_good_prime


def test_factor_degrees_marks_bad_prime_when_discriminant_vanishes():
    poly = parse_polynomial("x^2 - 1")
    factorization = factor_degrees_mod_prime(poly, 2)

    assert factorization.prime == 2
    assert factorization.is_good_prime is False


def test_summarize_polynomial_basic_fields():
    summary = summarize_polynomial("x^3 - 2")

    assert summary.degree == 3
    assert summary.is_irreducible is True
    assert summary.coefficient_bound.ok is True
    assert summary.coefficient_bound.max_digits == 1
```

- [ ] **Step 2: Run tests to verify they fail before implementation**

Run:

```powershell
$env:PYTHONPATH = "experiments/m23/src"
python -m pytest experiments/m23/tests/test_polynomial.py -q
```

Expected: FAIL with missing `m23verify.polynomial` symbols.

- [ ] **Step 3: Implement `polynomial.py`**

Create `experiments/m23/src/m23verify/polynomial.py`:

```python
from __future__ import annotations

from dataclasses import dataclass
from math import prod

from sympy import Poly, ZZ, discriminant, factor_list, symbols
from sympy.polys.polyerrors import CoercionFailed
from sympy.parsing.sympy_parser import (
    convert_xor,
    implicit_multiplication_application,
    parse_expr,
    standard_transformations,
)


x = symbols("x")
TRANSFORMATIONS = standard_transformations + (
    implicit_multiplication_application,
    convert_xor,
)


@dataclass(frozen=True)
class CoefficientBoundResult:
    ok: bool
    max_digits: int
    bound_digits: int


@dataclass(frozen=True)
class ModularFactorization:
    prime: int
    cycle_type: tuple[int, ...]
    is_good_prime: bool
    reason: str


@dataclass(frozen=True)
class PolynomialSummary:
    input: str
    degree: int
    coefficients: tuple[int, ...]
    coefficient_bound: CoefficientBoundResult
    is_irreducible: bool
    discriminant: int


def parse_polynomial(poly_text: str) -> Poly:
    try:
        expr = parse_expr(
            poly_text,
            local_dict={"x": x},
            transformations=TRANSFORMATIONS,
            evaluate=True,
        )
        return Poly(expr, x, domain=ZZ)
    except (CoercionFailed, TypeError, ValueError) as exc:
        raise ValueError(f"polynomial must have integer coefficients in x: {poly_text}") from exc


def coefficient_digit_count(value: int) -> int:
    return len(str(abs(int(value))))


def coefficient_bound(poly: Poly, bound_digits: int = 99) -> CoefficientBoundResult:
    max_digits = max(coefficient_digit_count(int(coeff)) for coeff in poly.all_coeffs())
    return CoefficientBoundResult(
        ok=max_digits <= bound_digits,
        max_digits=max_digits,
        bound_digits=bound_digits,
    )


def _is_prime_candidate(prime: int) -> bool:
    if prime < 2:
        return False
    if prime == 2:
        return True
    if prime % 2 == 0:
        return False
    divisor = 3
    while divisor * divisor <= prime:
        if prime % divisor == 0:
            return False
        divisor += 2
    return True


def factor_degrees_mod_prime(poly: Poly, prime: int) -> ModularFactorization:
    if not _is_prime_candidate(prime):
        raise ValueError(f"not a prime: {prime}")

    leading = int(poly.LC())
    disc = int(discriminant(poly.as_expr(), x))
    is_good = leading % prime != 0 and disc % prime != 0
    reason = "good prime" if is_good else "bad prime: leading coefficient or discriminant vanishes mod p"

    _, factors = factor_list(poly.as_expr(), x, modulus=prime)
    degrees: list[int] = []
    for factor_expr, multiplicity in factors:
        factor_poly = Poly(factor_expr, x, modulus=prime)
        degrees.extend([factor_poly.degree()] * int(multiplicity))

    return ModularFactorization(
        prime=prime,
        cycle_type=tuple(sorted(degrees, reverse=True)),
        is_good_prime=is_good,
        reason=reason,
    )


def summarize_polynomial(poly_text: str, bound_digits: int = 99) -> PolynomialSummary:
    poly = parse_polynomial(poly_text)
    return PolynomialSummary(
        input=poly_text,
        degree=poly.degree(),
        coefficients=tuple(int(coeff) for coeff in poly.all_coeffs()),
        coefficient_bound=coefficient_bound(poly, bound_digits=bound_digits),
        is_irreducible=bool(poly.is_irreducible),
        discriminant=int(discriminant(poly.as_expr(), x)),
    )
```

- [ ] **Step 4: Run polynomial tests**

Run:

```powershell
$env:PYTHONPATH = "experiments/m23/src"
python -m pytest experiments/m23/tests/test_polynomial.py -q
```

Expected: `6 passed`.

## Task 4: Add Report Builder

**Files:**
- Create: `experiments/m23/tests/test_report.py`
- Create: `experiments/m23/src/m23verify/report.py`

- [ ] **Step 1: Write failing report tests**

Create `experiments/m23/tests/test_report.py`:

```python
from pathlib import Path

from m23verify.group_data import load_m23_cycle_data
from m23verify.report import build_report


DATA_PATH = Path(__file__).parents[1] / "data" / "m23_23t5_cycle_types.json"


def test_build_report_for_non_degree_23_polynomial():
    data = load_m23_cycle_data(DATA_PATH)
    report = build_report("x^3 - 2", primes=[2, 3, 5, 7], cycle_data=data)

    assert report["summary"]["degree"] == 3
    assert report["classification"] == "reject"
    assert "degree is 3, expected 23" in report["reasons"]


def test_build_report_records_cycle_compatibility():
    data = load_m23_cycle_data(DATA_PATH)
    report = build_report("x^23 - x - 1", primes=[2, 3, 5, 7, 11], cycle_data=data)

    assert "modular_factorizations" in report
    assert all("prime" in item for item in report["modular_factorizations"])
    assert all("cycle_type" in item for item in report["modular_factorizations"])
    assert all("m23_compatible" in item for item in report["modular_factorizations"])
```

- [ ] **Step 2: Run tests to verify they fail before implementation**

Run:

```powershell
$env:PYTHONPATH = "experiments/m23/src"
python -m pytest experiments/m23/tests/test_report.py -q
```

Expected: FAIL with missing `m23verify.report`.

- [ ] **Step 3: Implement `report.py`**

Create `experiments/m23/src/m23verify/report.py`:

```python
from __future__ import annotations

from typing import Iterable

from .group_data import M23CycleData
from .polynomial import factor_degrees_mod_prime, parse_polynomial, summarize_polynomial


def _classification(reasons: list[str], incompatible_good_primes: int) -> str:
    if reasons:
        return "reject"
    if incompatible_good_primes:
        return "reject"
    return "needs_external_group_verification"


def build_report(
    poly_text: str,
    primes: Iterable[int],
    cycle_data: M23CycleData,
    coefficient_bound_digits: int = 99,
) -> dict:
    poly = parse_polynomial(poly_text)
    summary = summarize_polynomial(poly_text, bound_digits=coefficient_bound_digits)

    reasons: list[str] = []
    if summary.degree != cycle_data.degree:
        reasons.append(f"degree is {summary.degree}, expected {cycle_data.degree}")
    if not summary.coefficient_bound.ok:
        reasons.append(
            f"maximum coefficient has {summary.coefficient_bound.max_digits} digits, "
            f"expected at most {summary.coefficient_bound.bound_digits}"
        )
    if not summary.is_irreducible:
        reasons.append("polynomial is reducible over Q")
    if summary.discriminant == 0:
        reasons.append("polynomial has zero discriminant")

    modular_factorizations = []
    incompatible_good_primes = 0
    for prime in primes:
        factorization = factor_degrees_mod_prime(poly, int(prime))
        compatible = cycle_data.is_allowed(factorization.cycle_type)
        if factorization.is_good_prime and not compatible:
            incompatible_good_primes += 1
        modular_factorizations.append(
            {
                "prime": factorization.prime,
                "cycle_type": list(factorization.cycle_type),
                "is_good_prime": factorization.is_good_prime,
                "reason": factorization.reason,
                "m23_compatible": compatible,
            }
        )

    if incompatible_good_primes:
        reasons.append(f"{incompatible_good_primes} good primes have cycle types not present in M23")

    return {
        "candidate": poly_text,
        "target": {
            "group_label": cycle_data.group_label,
            "group_name": cycle_data.group_name,
            "degree": cycle_data.degree,
            "order": cycle_data.order,
        },
        "summary": {
            "degree": summary.degree,
            "coefficients": list(summary.coefficients),
            "max_coefficient_digits": summary.coefficient_bound.max_digits,
            "coefficient_digit_bound": summary.coefficient_bound.bound_digits,
            "is_irreducible": summary.is_irreducible,
            "discriminant": summary.discriminant,
        },
        "modular_factorizations": modular_factorizations,
        "classification": _classification(reasons, incompatible_good_primes),
        "reasons": reasons,
        "warning": (
            "This local report is a filter, not a proof. "
            "A surviving candidate still needs Magma/GAP group verification and a written subgroup-exclusion proof."
        ),
    }
```

- [ ] **Step 4: Run report tests**

Run:

```powershell
$env:PYTHONPATH = "experiments/m23/src"
python -m pytest experiments/m23/tests/test_report.py -q
```

Expected: `2 passed`.

## Task 5: Add CLI Entrypoint

**Files:**
- Create: `experiments/m23/scripts/verify_candidate.py`
- Create: `experiments/m23/tests/test_cli.py`
- Modify: `experiments/m23/src/m23verify/__init__.py`

- [ ] **Step 1: Write failing CLI tests**

Create `experiments/m23/tests/test_cli.py`:

```python
import json
import subprocess
import sys
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "verify_candidate.py"


def test_cli_outputs_json_for_candidate():
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "x^3 - 2",
            "--primes",
            "2,3,5",
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    report = json.loads(result.stdout)
    assert report["candidate"] == "x^3 - 2"
    assert report["classification"] == "reject"
```

- [ ] **Step 2: Run CLI tests to verify they fail before implementation**

Run:

```powershell
$env:PYTHONPATH = "experiments/m23/src"
python -m pytest experiments/m23/tests/test_cli.py -q
```

Expected: FAIL because `verify_candidate.py` does not exist.

- [ ] **Step 3: Implement CLI**

Create `experiments/m23/scripts/verify_candidate.py`:

```python
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from m23verify.group_data import load_m23_cycle_data
from m23verify.report import build_report


def parse_primes(raw: str) -> list[int]:
    primes = [int(item.strip()) for item in raw.split(",") if item.strip()]
    if not primes:
        raise argparse.ArgumentTypeError("at least one prime is required")
    return primes


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify local fingerprints for an M23 candidate polynomial.")
    parser.add_argument("polynomial", help="Polynomial in Magma-like syntax, for example x^23 - x - 1")
    parser.add_argument("--primes", type=parse_primes, default=parse_primes("2,3,5,7,11,13,17,19,23,29,31"))
    parser.add_argument("--data", default=str(ROOT / "data" / "m23_23t5_cycle_types.json"))
    parser.add_argument("--out", help="Optional JSON output path")
    args = parser.parse_args()

    cycle_data = load_m23_cycle_data(args.data)
    report = build_report(args.polynomial, primes=args.primes, cycle_data=cycle_data)
    output = json.dumps(report, indent=2, sort_keys=True)

    if args.out:
        Path(args.out).write_text(output + "\n", encoding="utf-8")
    else:
        print(output)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Run CLI tests**

Run:

```powershell
$env:PYTHONPATH = "experiments/m23/src"
python -m pytest experiments/m23/tests/test_cli.py -q
```

Expected: `1 passed`.

- [ ] **Step 5: Run a manual CLI smoke test**

Run:

```powershell
python experiments/m23/scripts/verify_candidate.py "x^3 - 2" --primes 2,3,5
```

Expected: JSON output with `"classification": "reject"` and reason `"degree is 3, expected 23"`.

- [ ] **Step 6: Export public package symbols**

Update `experiments/m23/src/m23verify/__init__.py`:

```python
"""Verification harness for M23 inverse Galois candidate polynomials."""

from .polynomial import (
    CoefficientBoundResult,
    ModularFactorization,
    PolynomialSummary,
    coefficient_digit_count,
    factor_degrees_mod_prime,
    parse_polynomial,
    summarize_polynomial,
)
from .group_data import M23CycleData, load_m23_cycle_data
from .report import build_report

__all__ = [
    "CoefficientBoundResult",
    "M23CycleData",
    "ModularFactorization",
    "PolynomialSummary",
    "build_report",
    "coefficient_digit_count",
    "factor_degrees_mod_prime",
    "load_m23_cycle_data",
    "parse_polynomial",
    "summarize_polynomial",
]
```

## Task 6: Add Magma and GAP Companion Scripts

**Files:**
- Create: `experiments/m23/magma/verify_candidate.m`
- Create: `experiments/m23/gap/group_fingerprints.g`
- Create: `experiments/m23/tests/test_external_scripts.py`

- [ ] **Step 1: Write tests for script presence and key commands**

Create `experiments/m23/tests/test_external_scripts.py`:

```python
from pathlib import Path


ROOT = Path(__file__).parents[1]


def test_magma_script_contains_galois_group_checks():
    text = (ROOT / "magma" / "verify_candidate.m").read_text(encoding="utf-8")

    assert "GaloisGroup" in text
    assert "Factorization" in text
    assert "Discriminant" in text


def test_gap_script_contains_m23_action_checks():
    text = (ROOT / "gap" / "group_fingerprints.g").read_text(encoding="utf-8")

    assert "MathieuGroup(23)" in text
    assert "CycleStructurePerm" in text
    assert "TransitiveGroup(23,5)" in text
```

- [ ] **Step 2: Run tests to verify they fail before scripts exist**

Run:

```powershell
$env:PYTHONPATH = "experiments/m23/src"
python -m pytest experiments/m23/tests/test_external_scripts.py -q
```

Expected: FAIL because scripts do not exist.

- [ ] **Step 3: Add Magma script**

Create `experiments/m23/magma/verify_candidate.m`:

```magma
// M23 candidate verification helper.
// Usage inside Magma:
//   load "experiments/m23/magma/verify_candidate.m";
//   VerifyCandidate("x^23 - x - 1", [2,3,5,7,11,13,17,19,23,29,31]);

function ParseCandidate(poly_string)
    Qx<x> := PolynomialRing(Rationals());
    return eval poly_string;
end function;

procedure VerifyCandidate(poly_string, primes)
    Qx<x> := PolynomialRing(Rationals());
    f := eval poly_string;

    print "candidate:", f;
    print "degree:", Degree(f);
    print "is_irreducible:", IsIrreducible(f);
    print "discriminant:", Discriminant(f);

    for p in primes do
        Fp<t> := PolynomialRing(GF(p));
        fp := Fp!f;
        print "prime:", p;
        print "factorization:", Factorization(fp);
    end for;

    print "Attempting GaloisGroup. This may be expensive.";
    G, roots, data := GaloisGroup(f);
    print "galois_group_order:", #G;
    print "galois_group:", G;
end procedure;
```

- [ ] **Step 4: Add GAP script**

Create `experiments/m23/gap/group_fingerprints.g`:

```gap
# M23 degree-23 action fingerprint helper.
# Usage inside GAP:
#   Read("experiments/m23/gap/group_fingerprints.g");

CycleTypeFromPermutation := function(perm, degree)
    local seen, lengths, i, j, length;
    seen := [];
    lengths := [];
    for i in [1..degree] do
        seen[i] := false;
    od;
    for i in [1..degree] do
        if not seen[i] then
            j := i;
            length := 0;
            while not seen[j] do
                seen[j] := true;
                length := length + 1;
                j := j ^ perm;
            od;
            Add(lengths, length);
        fi;
    od;
    Sort(lengths);
    return Reversed(lengths);
end;

PrintM23Fingerprints := function()
    local G, H, classes, cycleTypes, c, representative, cycleType;
    G := MathieuGroup(23);
    H := TransitiveGroup(23,5);
    Print("MathieuGroup(23) order: ", Size(G), "\n");
    Print("TransitiveGroup(23,5) order: ", Size(H), "\n");
    classes := ConjugacyClasses(G);
    cycleTypes := [];
    for c in classes do
        representative := Representative(c);
        cycleType := CycleTypeFromPermutation(representative, 23);
        if not cycleType in cycleTypes then
            Add(cycleTypes, cycleType);
        fi;
    od;
    Print("Unique cycle types in MathieuGroup(23):\n");
    for cycleType in cycleTypes do
        Print(cycleType, "\n");
    od;
end;

PrintM23Fingerprints();
```

- [ ] **Step 5: Run script-content tests**

Run:

```powershell
$env:PYTHONPATH = "experiments/m23/src"
python -m pytest experiments/m23/tests/test_external_scripts.py -q
```

Expected: `2 passed`.

## Task 7: Add Vault Verification Pages

**Files:**
- Create: `wiki/m23-verification-standard.md`
- Create: `wiki/m23-known-boundary.md`
- Modify: `index.md`
- Create: `logs/ingest/2026-05-22-m23-verification-harness-plan.md`

- [ ] **Step 1: Add verification standard page**

Create `wiki/m23-verification-standard.md`:

```markdown
---
type: wiki-page
status: active
created: 2026-05-22
last_confirmed: 2026-05-22
confidence: 0.76
quality_score: 0.84
sensitivity: internal
sources:
  - "[[wiki/m23-proof-factory]]"
entities:
  - "[[entities/projects/m23-proof-factory]]"
  - "[[entities/concepts/galois-verification-pipeline]]"
  - "[[entities/concepts/mathieu-group-m23]]"
relationships:
  - target: "[[wiki/m23-proof-factory]]"
    type: "supports"
    confidence: 0.88
supersedes: []
superseded_by: []
review_after: 2026-06-22
---

# M23 Verification Standard

## Summary

The local harness is a filter, not a proof. A candidate polynomial survives phase one only when it has the right degree, coefficient bound, irreducibility, nonzero discriminant, and good-prime factorization types compatible with M23.

## Local Gates

1. Polynomial parses as an element of `Z[x]`.
2. Degree is 23.
3. Maximum coefficient length is at most 99 decimal digits.
4. Polynomial is irreducible over `Q`.
5. Discriminant is nonzero.
6. Good-prime factorizations produce cycle types present in the degree-23 action of M23.

## External Gates

1. Magma or GAP confirms the relevant group fingerprints.
2. A subgroup-exclusion argument rules out all remaining transitive subgroups.
3. The proof explains why the Galois group is exactly M23 rather than a larger or smaller group.

## Non-Claims

Passing the Python harness does not prove the Galois group is M23. It means only that the candidate deserves stronger verification.
```

- [ ] **Step 2: Add known-boundary page**

Create `wiki/m23-known-boundary.md`:

```markdown
---
type: wiki-page
status: active
created: 2026-05-22
last_confirmed: 2026-05-22
confidence: 0.72
quality_score: 0.82
sensitivity: internal
sources:
  - "[[wiki/m23-proof-factory]]"
entities:
  - "[[entities/projects/m23-proof-factory]]"
  - "[[entities/concepts/mathieu-group-m23]]"
relationships:
  - target: "[[wiki/m23-verification-standard]]"
    type: "supports"
    confidence: 0.84
supersedes: []
superseded_by: []
review_after: 2026-06-22
---

# M23 Known Boundary

## Summary

This page records the first boundary facts for the M23 inverse Galois search.

## Seed Facts

- The target group is Mathieu group M23.
- The natural action has degree 23.
- In transitive group notation, the target is `23T5`.
- The group order is `10200960`.
- Current public references checked on 2026-05-22 say `M23/Q` remains open.

## Local Cycle-Type Data

The file `experiments/m23/data/m23_23t5_cycle_types.json` seeds local M23-compatible cycle types for filtering. This table must be verified against GAP or Magma before proof use.

## Next Boundary Work

- Confirm the JSON table against `MathieuGroup(23)` in GAP.
- Record maximal subgroups relevant to degree-23 subgroup exclusion.
- Add known failed branch-cycle or braid-orbit families from Hafner.
```

- [ ] **Step 3: Update index**

Modify `index.md` by adding these entries under "Synthesized Wiki Pages":

```markdown
- [[wiki/m23-verification-standard]] - phase-one local and external verification gates for M23 candidates.
- [[wiki/m23-known-boundary]] - seed facts and first group-boundary data for the M23 search.
```

- [ ] **Step 4: Add ingest log**

Create `logs/ingest/2026-05-22-m23-verification-harness-plan.md`:

```markdown
---
type: ingest-log
status: active
created: 2026-05-22
last_confirmed: 2026-05-22
confidence: 0.76
quality_score: 0.82
sensitivity: internal
source: "[[docs/superpowers/plans/2026-05-22-m23-verification-harness]]"
sources:
  - "[[wiki/m23-proof-factory]]"
entities:
  - "[[entities/projects/m23-proof-factory]]"
  - "[[entities/concepts/galois-verification-pipeline]]"
relationships:
  - target: "[[wiki/m23-verification-standard]]"
    type: "supports"
    confidence: 0.86
supersedes: []
superseded_by: []
review_after: 2026-06-22
---

# M23 Verification Harness Plan Ingest

## Source

- Source: implementation plan for the M23 verification harness.
- Source kind: project plan.
- Sensitivity: internal.

## Actions

- Planned the Python local verification harness.
- Planned companion Magma and GAP scripts.
- Planned vault verification standard and known-boundary pages.

## Entities Created or Updated

- [[entities/projects/m23-proof-factory]]
- [[entities/concepts/galois-verification-pipeline]]

## Wiki Pages Created or Updated

- [[wiki/m23-verification-standard]]
- [[wiki/m23-known-boundary]]
- [[index]]

## Privacy Filtering

No sensitive material was involved.

## Confidence and Quality Notes

The plan is locally executable for Python checks. Full proof certification still requires external algebra systems and expert review.

## Follow-Up

- Execute the plan task by task.
- Build the verification harness before candidate search.
```

## Task 8: Full Local Verification

**Files:**
- Read all implementation files and vault pages.

- [ ] **Step 1: Run all harness tests**

Run:

```powershell
$env:PYTHONPATH = "experiments/m23/src"
python -m pytest experiments/m23/tests -q
```

Expected: all tests pass.

- [ ] **Step 2: Run CLI smoke test**

Run:

```powershell
python experiments/m23/scripts/verify_candidate.py "x^3 - 2" --primes 2,3,5
```

Expected: JSON output includes:

```json
"classification": "reject"
```

and:

```json
"degree is 3, expected 23"
```

- [ ] **Step 3: Check unresolved work markers**

Run:

```powershell
rg -n "\b(TO-DO|TO-BE-DETERMINED|FIX-ME)\b" experiments/m23 wiki/m23-verification-standard.md wiki/m23-known-boundary.md logs/ingest/2026-05-22-m23-verification-harness-plan.md
```

Expected: no matches.

- [ ] **Step 4: Check vault wikilinks**

Run:

```powershell
$files = Get-ChildItem -Path . -Recurse -Filter *.md | Where-Object { $_.FullName -notmatch '\\.obsidian\\' }
$allMd = $files | ForEach-Object { [pscustomobject]@{ FullName = $_.FullName; BaseName = $_.BaseName; Relative = (Resolve-Path -Relative $_.FullName).TrimStart('.\') -replace '\\','/' } }
$broken = @()
foreach ($file in $files) {
  $text = Get-Content -Raw -Path $file.FullName
  foreach ($match in [regex]::Matches($text, '\[\[([^\]|#]+)')) {
    $target = $match.Groups[1].Value.Trim()
    if ($target -match '^[a-zA-Z]+://') { continue }
    $normalized = $target -replace '\\','/'
    $found = $false
    if ($normalized.Contains('/')) {
      $candidate = "$normalized.md"
      $found = ($allMd.Relative -contains $candidate)
    } else {
      $found = ($allMd.BaseName -contains $normalized)
    }
    if (-not $found) { $broken += [pscustomobject]@{ File = (Resolve-Path -Relative $file.FullName); Target = $target } }
  }
}
if ($broken.Count -gt 0) { $broken | Format-Table -AutoSize; exit 1 } else { "All wikilinks resolve across $($files.Count) markdown files." }
```

Expected: all wikilinks resolve.

## Self-Review Checklist

- Spec coverage: verification harness, known-boundary tables, local reports, companion Magma/GAP scripts, and vault documentation are all covered.
- Marker scan: run the unresolved work marker command before completion.
- Type consistency: `M23CycleData`, `PolynomialSummary`, `ModularFactorization`, and `build_report` are used consistently across tests, implementation, and CLI.
- Scope: candidate generation and large search batches are deliberately outside this first implementation plan.
