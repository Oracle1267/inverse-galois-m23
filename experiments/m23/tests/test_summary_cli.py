import json
import subprocess
import sys
from pathlib import Path
from uuid import uuid4

from m23verify.ledger import append_ledger_entry, entry_from_report


SCRIPT = Path(__file__).parents[1] / "scripts" / "ledger_summary.py"
TMP_ROOT = Path(__file__).parent / ".tmp"


def local_temp_path(name: str) -> Path:
    TMP_ROOT.mkdir(parents=True, exist_ok=True)
    return TMP_ROOT / f"{uuid4().hex}-{name}"


def test_ledger_summary_cli_outputs_json():
    ledger_path = local_temp_path("candidate_ledger.jsonl")
    append_ledger_entry(
        ledger_path,
        entry_from_report(
            {
                "candidate": "x^23 - x - 1",
                "classification": "reject",
                "reasons": ["1 good primes have cycle types not present in M23"],
                "summary": {},
                "modular_factorizations": [
                    {"prime": 2, "cycle_type": [13, 8, 2], "is_good_prime": True, "m23_compatible": False}
                ],
            },
            generator="unit-test",
            run_id="run-1",
        ),
    )

    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--ledger", str(ledger_path)],
        check=True,
        capture_output=True,
        text=True,
    )

    summary = json.loads(result.stdout)
    assert summary["entry_count"] == 1
    assert summary["latest_classifications"] == {"reject": 1}


def test_ledger_summary_cli_writes_markdown_report():
    ledger_path = local_temp_path("candidate_ledger.jsonl")
    report_path = local_temp_path("ledger-summary.md")
    append_ledger_entry(
        ledger_path,
        entry_from_report(
            {
                "candidate": "x^23 - x - 1",
                "classification": "reject",
                "reasons": ["1 good primes have cycle types not present in M23"],
                "summary": {},
                "modular_factorizations": [
                    {"prime": 2, "cycle_type": [13, 8, 2], "is_good_prime": True, "m23_compatible": False}
                ],
            },
            generator="unit-test",
            run_id="run-1",
        ),
    )

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--ledger",
            str(ledger_path),
            "--markdown-out",
            str(report_path),
            "--title",
            "Unit Test Report",
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    assert json.loads(result.stdout)["entry_count"] == 1
    markdown = report_path.read_text(encoding="utf-8")
    assert "# Unit Test Report" in markdown
    assert "| reject | 1 |" in markdown
