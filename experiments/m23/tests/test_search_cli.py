import json
import subprocess
import sys
from pathlib import Path
from uuid import uuid4


SCRIPT = Path(__file__).parents[1] / "scripts" / "search_batch.py"
TMP_ROOT = Path(__file__).parent / ".tmp"


def local_temp_path(name: str) -> Path:
    TMP_ROOT.mkdir(parents=True, exist_ok=True)
    return TMP_ROOT / f"{uuid4().hex}-{name}"


def write_cycle_data(path: Path) -> None:
    path.write_text(
        json.dumps(
            {
                "group_label": "23T5-test",
                "group_name": "M23-test",
                "degree": 23,
                "order": 10200960,
                "source_urls": [],
                "cycle_types": [[13, 8, 2]],
            }
        ),
        encoding="utf-8",
    )


def test_search_cli_runs_batch_and_writes_ledger():
    ledger_path = local_temp_path("candidate_ledger.jsonl")
    data_path = local_temp_path("cycle_data.json")
    write_cycle_data(data_path)

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--family",
            "trinomial",
            "--a-range",
            "-1:-1",
            "--b-range",
            "-1:-1",
            "--primes",
            "2",
            "--max-candidates",
            "10",
            "--ledger",
            str(ledger_path),
            "--data",
            str(data_path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    summary = json.loads(result.stdout)
    assert summary["tested"] == 1
    assert summary["survivors"] == ["x^23 - x - 1"]
    assert ledger_path.exists()


def test_search_cli_keeps_third_party_warnings_out_of_stderr():
    ledger_path = local_temp_path("candidate_ledger.jsonl")
    data_path = local_temp_path("cycle_data.json")
    write_cycle_data(data_path)

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--family",
            "trinomial",
            "--a-range",
            "-10:10",
            "--b-range",
            "-10:10",
            "--primes",
            "2,3,5",
            "--max-candidates",
            "25",
            "--ledger",
            str(ledger_path),
            "--data",
            str(data_path),
            "--continue-on-survivor",
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    assert "SymPyDeprecationWarning" not in result.stderr
