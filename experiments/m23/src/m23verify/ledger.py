from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any, Iterable


def entry_from_report(report: dict[str, Any], generator: str, run_id: str) -> dict[str, Any]:
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "run_id": run_id,
        "generator": generator,
        "polynomial": report["candidate"],
        "classification": report["classification"],
        "reasons": list(report.get("reasons", [])),
        "summary": dict(report.get("summary", {})),
        "modular_factorizations": list(report.get("modular_factorizations", [])),
    }


def append_ledger_entry(path: str | Path, entry: dict[str, Any]) -> None:
    ledger_path = Path(path)
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    with ledger_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, sort_keys=True) + "\n")


def read_ledger(path: str | Path) -> list[dict[str, Any]]:
    ledger_path = Path(path)
    if not ledger_path.exists():
        return []
    entries: list[dict[str, Any]] = []
    for line in ledger_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped:
            entries.append(json.loads(stripped))
    return entries


def seen_candidates(path: str | Path) -> set[str]:
    return {entry["polynomial"] for entry in read_ledger(path) if "polynomial" in entry}


def resolved_candidates(path: str | Path, requested_primes: Iterable[int]) -> set[str]:
    requested = {int(prime) for prime in requested_primes}
    resolved: set[str] = set()
    for entry in read_ledger(path):
        polynomial = entry.get("polynomial")
        if not polynomial:
            continue
        if entry.get("classification") == "reject":
            resolved.add(polynomial)
            continue
        covered_primes = {
            int(item["prime"])
            for item in entry.get("modular_factorizations", [])
            if "prime" in item
        }
        if requested.issubset(covered_primes):
            resolved.add(polynomial)
    return resolved
