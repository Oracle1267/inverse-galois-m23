from pathlib import Path
from uuid import uuid4

from m23verify.ledger import (
    append_ledger_entry,
    entry_from_report,
    read_ledger,
    resolved_candidates,
    seen_candidates,
)


TMP_ROOT = Path(__file__).parent / ".tmp"


def local_temp_path(name: str) -> Path:
    TMP_ROOT.mkdir(parents=True, exist_ok=True)
    return TMP_ROOT / f"{uuid4().hex}-{name}"


def test_ledger_appends_and_reads_jsonl_entries():
    ledger_path = local_temp_path("candidate_ledger.jsonl")
    report = {
        "candidate": "x^23 - x - 1",
        "classification": "reject",
        "reasons": ["cycle type rejected"],
        "summary": {"degree": 23},
        "modular_factorizations": [{"prime": 2, "cycle_type": [13, 8, 2]}],
    }

    entry = entry_from_report(report, generator="unit-test", run_id="run-1")
    append_ledger_entry(ledger_path, entry)

    entries = read_ledger(ledger_path)
    assert len(entries) == 1
    assert entries[0]["polynomial"] == "x^23 - x - 1"
    assert entries[0]["generator"] == "unit-test"
    assert entries[0]["classification"] == "reject"


def test_seen_candidates_reads_prior_polynomials():
    ledger_path = local_temp_path("candidate_ledger.jsonl")
    report = {
        "candidate": "x^23 + x + 1",
        "classification": "reject",
        "reasons": [],
        "summary": {"degree": 23},
        "modular_factorizations": [],
    }

    append_ledger_entry(ledger_path, entry_from_report(report, generator="unit-test", run_id="run-1"))

    assert seen_candidates(ledger_path) == {"x^23 + x + 1"}


def test_resolved_candidates_skips_rejections_even_with_fewer_primes():
    ledger_path = local_temp_path("candidate_ledger.jsonl")
    report = {
        "candidate": "x^23 - x - 1",
        "classification": "reject",
        "reasons": ["cycle type rejected"],
        "summary": {},
        "modular_factorizations": [{"prime": 2, "cycle_type": [13, 8, 2]}],
    }
    append_ledger_entry(ledger_path, entry_from_report(report, generator="unit-test", run_id="run-1"))

    assert resolved_candidates(ledger_path, requested_primes=[2, 3]) == {"x^23 - x - 1"}


def test_resolved_candidates_keeps_weak_survivors_open_for_stronger_prime_sets():
    ledger_path = local_temp_path("candidate_ledger.jsonl")
    weak_survivor = {
        "candidate": "x^23 - 2*x - 4",
        "classification": "needs_external_group_verification",
        "reasons": [],
        "summary": {},
        "modular_factorizations": [{"prime": 2, "cycle_type": [23]}],
    }
    append_ledger_entry(ledger_path, entry_from_report(weak_survivor, generator="unit-test", run_id="run-1"))

    assert resolved_candidates(ledger_path, requested_primes=[2, 3]) == set()
    assert resolved_candidates(ledger_path, requested_primes=[2]) == {"x^23 - 2*x - 4"}
