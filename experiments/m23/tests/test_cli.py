import json
import subprocess
import sys
from pathlib import Path
from uuid import uuid4


SCRIPT = Path(__file__).parents[1] / "scripts" / "verify_candidate.py"
TMP_ROOT = Path(__file__).parent / ".tmp"


def local_temp_path(name: str) -> Path:
    TMP_ROOT.mkdir(parents=True, exist_ok=True)
    return TMP_ROOT / f"{uuid4().hex}-{name}"


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


def test_cli_appends_report_to_ledger_when_requested():
    ledger_path = local_temp_path("candidate_ledger.jsonl")

    subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "x^23 - x - 1",
            "--primes",
            "2",
            "--ledger",
            str(ledger_path),
            "--generator",
            "cli-test",
            "--run-id",
            "run-1",
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    entries = [json.loads(line) for line in ledger_path.read_text(encoding="utf-8").splitlines()]
    assert entries[0]["polynomial"] == "x^23 - x - 1"
    assert entries[0]["generator"] == "cli-test"
    assert entries[0]["run_id"] == "run-1"
