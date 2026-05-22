import json
from pathlib import Path
from uuid import uuid4

from m23verify.ledger import append_ledger_entry, entry_from_report, read_ledger
from m23verify.search import run_search_batch


TMP_ROOT = Path(__file__).parent / ".tmp"


def local_temp_path(name: str) -> Path:
    TMP_ROOT.mkdir(parents=True, exist_ok=True)
    return TMP_ROOT / f"{uuid4().hex}-{name}"


def write_cycle_data(path: Path, cycle_types: list[list[int]]) -> None:
    path.write_text(
        json.dumps(
            {
                "group_label": "23T5-test",
                "group_name": "M23-test",
                "degree": 23,
                "order": 10200960,
                "source_urls": [],
                "cycle_types": cycle_types,
            }
        ),
        encoding="utf-8",
    )


def test_search_batch_records_candidate_and_stops_on_survivor():
    ledger_path = local_temp_path("candidate_ledger.jsonl")
    data_path = local_temp_path("cycle_data.json")
    write_cycle_data(data_path, [[13, 8, 2]])

    result = run_search_batch(
        family="trinomial",
        a_range=(-1, -1),
        b_range=(-1, -1),
        primes=[2],
        max_candidates=10,
        ledger_path=ledger_path,
        data_path=data_path,
        stop_on_survivor=True,
        run_id="test-run",
    )

    assert result["tested"] == 1
    assert result["survivors"] == ["x^23 - x - 1"]
    entries = read_ledger(ledger_path)
    assert entries[0]["classification"] == "needs_external_group_verification"


def test_search_batch_skips_candidates_already_in_ledger():
    ledger_path = local_temp_path("candidate_ledger.jsonl")
    data_path = local_temp_path("cycle_data.json")
    write_cycle_data(data_path, [[13, 8, 2]])

    first = run_search_batch(
        family="trinomial",
        a_range=(-1, -1),
        b_range=(-1, -1),
        primes=[2],
        max_candidates=10,
        ledger_path=ledger_path,
        data_path=data_path,
        stop_on_survivor=False,
        run_id="first-run",
    )
    second = run_search_batch(
        family="trinomial",
        a_range=(-1, -1),
        b_range=(-1, -1),
        primes=[2],
        max_candidates=10,
        ledger_path=ledger_path,
        data_path=data_path,
        stop_on_survivor=False,
        run_id="second-run",
    )

    assert first["tested"] == 1
    assert second["tested"] == 0
    assert second["skipped_seen"] == 1


def test_search_batch_skip_count_ignores_candidates_outside_current_family():
    ledger_path = local_temp_path("candidate_ledger.jsonl")
    data_path = local_temp_path("cycle_data.json")
    write_cycle_data(data_path, [[13, 8, 2]])
    append_ledger_entry(
        ledger_path,
        entry_from_report(
            {
                "candidate": "x^3 - 2",
                "classification": "reject",
                "reasons": [],
                "summary": {},
                "modular_factorizations": [],
            },
            generator="manual",
            run_id="old-run",
        ),
    )

    result = run_search_batch(
        family="trinomial",
        a_range=(-1, -1),
        b_range=(-1, -1),
        primes=[2],
        max_candidates=10,
        ledger_path=ledger_path,
        data_path=data_path,
        stop_on_survivor=False,
        run_id="new-run",
    )

    assert result["tested"] == 1
    assert result["skipped_seen"] == 0


def test_search_batch_retests_weak_survivor_when_requested_primes_expand():
    ledger_path = local_temp_path("candidate_ledger.jsonl")
    data_path = local_temp_path("cycle_data.json")
    write_cycle_data(data_path, [[13, 8, 2]])
    append_ledger_entry(
        ledger_path,
        entry_from_report(
            {
                "candidate": "x^23 - x - 1",
                "classification": "needs_external_group_verification",
                "reasons": [],
                "summary": {},
                "modular_factorizations": [{"prime": 2, "cycle_type": [13, 8, 2]}],
            },
            generator="weak-run",
            run_id="weak-run",
        ),
    )

    result = run_search_batch(
        family="trinomial",
        a_range=(-1, -1),
        b_range=(-1, -1),
        primes=[2, 3],
        max_candidates=10,
        ledger_path=ledger_path,
        data_path=data_path,
        stop_on_survivor=False,
        run_id="stronger-run",
    )

    assert result["tested"] == 1
    assert result["skipped_seen"] == 0
