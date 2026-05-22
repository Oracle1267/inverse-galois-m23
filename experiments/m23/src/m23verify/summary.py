from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any

from .ledger import read_ledger


def _markdown_table(headers: list[str], rows: list[list[str]]) -> list[str]:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    lines.extend("| " + " | ".join(row) + " |" for row in rows)
    return lines


def _counter_items(counter: Counter) -> list[dict[str, Any]]:
    return [
        {"reason": key, "count": count}
        for key, count in sorted(counter.items(), key=lambda item: (-item[1], str(item[0])))
    ]


def _prime_counter_items(counter: Counter[int]) -> list[dict[str, int]]:
    return [
        {"prime": prime, "count": count}
        for prime, count in sorted(counter.items(), key=lambda item: (-item[1], item[0]))
    ]


def _cycle_counter_items(counter: Counter[tuple[int, tuple[int, ...]]]) -> list[dict[str, Any]]:
    return [
        {"prime": prime, "cycle_type": list(cycle_type), "count": count}
        for (prime, cycle_type), count in sorted(
            counter.items(),
            key=lambda item: (-item[1], item[0][0], item[0][1]),
        )
    ]


def _latest_entries(entries: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    latest: dict[str, dict[str, Any]] = {}
    for entry in entries:
        polynomial = entry.get("polynomial")
        if polynomial:
            latest[polynomial] = entry
    return latest


def summarize_ledger(path: str | Path) -> dict[str, Any]:
    entries = read_ledger(path)
    latest = _latest_entries(entries)
    latest_entries = list(latest.values())

    classifications = Counter(str(entry.get("classification", "unknown")) for entry in latest_entries)
    generators = Counter(str(entry.get("generator", "unknown")) for entry in entries)
    rejection_reasons: Counter[str] = Counter()
    first_rejecting_good_primes: Counter[int] = Counter()
    incompatible_cycle_types: Counter[tuple[int, tuple[int, ...]]] = Counter()

    for entry in latest_entries:
        if entry.get("classification") == "reject":
            rejection_reasons.update(str(reason) for reason in entry.get("reasons", []))

        first_rejecting_prime: int | None = None
        for factorization in entry.get("modular_factorizations", []):
            if not factorization.get("is_good_prime"):
                continue
            if factorization.get("m23_compatible", False):
                continue
            prime = int(factorization["prime"])
            cycle_type = tuple(int(item) for item in factorization.get("cycle_type", []))
            incompatible_cycle_types[(prime, cycle_type)] += 1
            if first_rejecting_prime is None:
                first_rejecting_prime = prime
        if first_rejecting_prime is not None:
            first_rejecting_good_primes[first_rejecting_prime] += 1

    active_survivors = sorted(
        polynomial
        for polynomial, entry in latest.items()
        if entry.get("classification") == "needs_external_group_verification"
    )

    return {
        "ledger_path": str(Path(path)),
        "entry_count": len(entries),
        "unique_polynomials": len(latest),
        "superseded_entries": len(entries) - len(latest),
        "latest_classifications": dict(sorted(classifications.items())),
        "generators": dict(sorted(generators.items())),
        "active_survivors": active_survivors,
        "rejection_reasons": _counter_items(rejection_reasons),
        "first_rejecting_good_primes": _prime_counter_items(first_rejecting_good_primes),
        "incompatible_cycle_types": _cycle_counter_items(incompatible_cycle_types),
    }


def render_markdown_report(summary: dict[str, Any], title: str = "M23 Ledger Summary") -> str:
    lines: list[str] = [
        f"# {title}",
        "",
        "## Outcome",
        "",
        f"- Ledger: `{summary['ledger_path']}`",
        f"- Entries: {summary['entry_count']}",
        f"- Unique polynomials: {summary['unique_polynomials']}",
        f"- Superseded entries: {summary['superseded_entries']}",
        f"- Active survivors: {len(summary['active_survivors'])}",
        "",
    ]

    lines.extend(
        _markdown_table(
            ["latest classification", "count"],
            [
                [str(classification), str(count)]
                for classification, count in summary["latest_classifications"].items()
            ],
        )
    )

    lines.extend(["", "## Generators", ""])
    lines.extend(
        _markdown_table(
            ["generator", "entries"],
            [[str(generator), str(count)] for generator, count in summary["generators"].items()],
        )
    )

    lines.extend(["", "## Rejection Reasons", ""])
    lines.extend(
        _markdown_table(
            ["reason", "count"],
            [[str(item["reason"]), str(item["count"])] for item in summary["rejection_reasons"]],
        )
    )

    lines.extend(["", "## First Rejecting Good Primes", ""])
    lines.extend(
        _markdown_table(
            ["prime", "count"],
            [[str(item["prime"]), str(item["count"])] for item in summary["first_rejecting_good_primes"]],
        )
    )

    lines.extend(["", "## Incompatible Cycle Types", ""])
    lines.extend(
        _markdown_table(
            ["prime", "cycle type", "count"],
            [
                [str(item["prime"]), "`" + str(item["cycle_type"]) + "`", str(item["count"])]
                for item in summary["incompatible_cycle_types"][:20]
            ],
        )
    )

    lines.extend(["", "## Active Survivors", ""])
    if summary["active_survivors"]:
        lines.extend(f"- `{candidate}`" for candidate in summary["active_survivors"])
    else:
        lines.append("- None.")

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "This report is a local-filter diagnosis. A rejection records an incompatibility observed by the current harness; a survivor would still require external Magma/GAP verification and a written subgroup-exclusion proof.",
            "",
        ]
    )
    return "\n".join(lines)
