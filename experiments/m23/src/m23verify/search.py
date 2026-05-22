from __future__ import annotations

from pathlib import Path
from typing import Iterable
from uuid import uuid4

from .families import count_trinomial_candidates, generate_trinomial_candidates
from .group_data import load_m23_cycle_data
from .ledger import append_ledger_entry, entry_from_report, resolved_candidates
from .report import build_report


def _candidate_stream(
    family: str,
    a_range: tuple[int, int],
    b_range: tuple[int, int],
    max_candidates: int,
    seen: set[str],
) -> list[str]:
    if family != "trinomial":
        raise ValueError(f"unsupported family: {family}")
    return list(
        generate_trinomial_candidates(
            a_range=a_range,
            b_range=b_range,
            max_candidates=max_candidates,
            seen=seen,
        )
    )


def _count_seen_in_family(
    family: str,
    a_range: tuple[int, int],
    b_range: tuple[int, int],
    seen: set[str],
) -> int:
    if family != "trinomial":
        raise ValueError(f"unsupported family: {family}")
    total_possible = count_trinomial_candidates(a_range, b_range)
    return sum(
        1
        for candidate in generate_trinomial_candidates(
            a_range=a_range,
            b_range=b_range,
            max_candidates=total_possible,
            seen=None,
        )
        if candidate in seen
    )


def run_search_batch(
    family: str,
    a_range: tuple[int, int],
    b_range: tuple[int, int],
    primes: Iterable[int],
    max_candidates: int,
    ledger_path: str | Path,
    data_path: str | Path,
    stop_on_survivor: bool = True,
    run_id: str | None = None,
) -> dict:
    run_id = run_id or str(uuid4())
    ledger_path = Path(ledger_path)
    primes = list(primes)
    already_seen = resolved_candidates(ledger_path, requested_primes=primes)
    cycle_data = load_m23_cycle_data(data_path)
    candidates = _candidate_stream(
        family=family,
        a_range=a_range,
        b_range=b_range,
        max_candidates=max_candidates,
        seen=already_seen,
    )

    tested = 0
    survivors: list[str] = []
    for candidate in candidates:
        report = build_report(candidate, primes=primes, cycle_data=cycle_data)
        append_ledger_entry(ledger_path, entry_from_report(report, generator=family, run_id=run_id))
        tested += 1
        if report["classification"] == "needs_external_group_verification":
            survivors.append(candidate)
            if stop_on_survivor:
                break

    total_possible = count_trinomial_candidates(a_range, b_range) if family == "trinomial" else 0
    skipped_seen = _count_seen_in_family(family, a_range, b_range, already_seen)
    return {
        "run_id": run_id,
        "family": family,
        "tested": tested,
        "survivors": survivors,
        "ledger_path": str(ledger_path),
        "skipped_seen": skipped_seen,
        "remaining_unseen_estimate": max(0, total_possible - skipped_seen - tested),
    }
