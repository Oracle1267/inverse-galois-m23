from pathlib import Path
from uuid import uuid4

from m23verify.ledger import append_ledger_entry, entry_from_report
from m23verify.summary import render_markdown_report, summarize_ledger


TMP_ROOT = Path(__file__).parent / ".tmp"


def local_temp_path(name: str) -> Path:
    TMP_ROOT.mkdir(parents=True, exist_ok=True)
    return TMP_ROOT / f"{uuid4().hex}-{name}"


def report(
    candidate: str,
    classification: str,
    reasons: list[str],
    modular_factorizations: list[dict],
) -> dict:
    return {
        "candidate": candidate,
        "classification": classification,
        "reasons": reasons,
        "summary": {"degree": 23},
        "modular_factorizations": modular_factorizations,
    }


def test_summarize_ledger_uses_latest_entry_and_counts_rejection_patterns():
    ledger_path = local_temp_path("candidate_ledger.jsonl")
    append_ledger_entry(
        ledger_path,
        entry_from_report(
            report(
                "x^23 - 2*x - 4",
                "needs_external_group_verification",
                [],
                [{"prime": 2, "cycle_type": [23], "is_good_prime": True, "m23_compatible": True}],
            ),
            generator="weak-run",
            run_id="weak-run",
        ),
    )
    append_ledger_entry(
        ledger_path,
        entry_from_report(
            report(
                "x^23 - 2*x - 4",
                "reject",
                ["1 good primes have cycle types not present in M23"],
                [{"prime": 7, "cycle_type": [11, 8, 4], "is_good_prime": True, "m23_compatible": False}],
            ),
            generator="escalation",
            run_id="strong-run",
        ),
    )
    append_ledger_entry(
        ledger_path,
        entry_from_report(
            report(
                "x^23 + x - 1",
                "reject",
                ["polynomial is reducible over Q", "1 good primes have cycle types not present in M23"],
                [{"prime": 2, "cycle_type": [13, 8, 2], "is_good_prime": True, "m23_compatible": False}],
            ),
            generator="trinomial",
            run_id="batch-run",
        ),
    )
    append_ledger_entry(
        ledger_path,
        entry_from_report(
            report(
                "x^23 + 3*x + 5",
                "needs_external_group_verification",
                [],
                [{"prime": 23, "cycle_type": [23], "is_good_prime": True, "m23_compatible": True}],
            ),
            generator="trinomial",
            run_id="batch-run",
        ),
    )

    summary = summarize_ledger(ledger_path)

    assert summary["entry_count"] == 4
    assert summary["unique_polynomials"] == 3
    assert summary["superseded_entries"] == 1
    assert summary["latest_classifications"] == {
        "needs_external_group_verification": 1,
        "reject": 2,
    }
    assert summary["active_survivors"] == ["x^23 + 3*x + 5"]
    assert summary["rejection_reasons"] == [
        {"reason": "1 good primes have cycle types not present in M23", "count": 2},
        {"reason": "polynomial is reducible over Q", "count": 1},
    ]
    assert summary["first_rejecting_good_primes"] == [
        {"prime": 2, "count": 1},
        {"prime": 7, "count": 1},
    ]
    assert summary["incompatible_cycle_types"] == [
        {"prime": 2, "cycle_type": [13, 8, 2], "count": 1},
        {"prime": 7, "cycle_type": [11, 8, 4], "count": 1},
    ]


def test_render_markdown_report_includes_diagnosis_sections():
    summary = {
        "ledger_path": "candidate_ledger.jsonl",
        "entry_count": 4,
        "unique_polynomials": 3,
        "superseded_entries": 1,
        "latest_classifications": {"reject": 2, "needs_external_group_verification": 1},
        "generators": {"trinomial": 3, "escalation": 1},
        "active_survivors": ["x^23 + 3*x + 5"],
        "rejection_reasons": [{"reason": "polynomial is reducible over Q", "count": 1}],
        "first_rejecting_good_primes": [{"prime": 2, "count": 1}],
        "incompatible_cycle_types": [{"prime": 2, "cycle_type": [13, 8, 2], "count": 1}],
    }

    markdown = render_markdown_report(summary, title="Unit Test Ledger Report")

    assert "# Unit Test Ledger Report" in markdown
    assert "## Outcome" in markdown
    assert "| latest classification | count |" in markdown
    assert "| reject | 2 |" in markdown
    assert "## First Rejecting Good Primes" in markdown
    assert "| 2 | 1 |" in markdown
    assert "`x^23 + 3*x + 5`" in markdown
