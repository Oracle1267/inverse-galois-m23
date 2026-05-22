import json
import subprocess
import sys
from pathlib import Path
from uuid import uuid4


SCRIPT = Path(__file__).parents[1] / "scripts" / "run_belyi_batches.py"
TMP_ROOT = Path(__file__).parent / ".tmp"


def local_temp_dir(name: str) -> Path:
    path = TMP_ROOT / f"{uuid4().hex}-{name}"
    path.mkdir(parents=True, exist_ok=True)
    return path


def test_run_belyi_batches_cli_writes_checkpoint_reports():
    report_dir = local_temp_dir("belyi-batches")

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--modulus",
            "5",
            "--start-left-factor-triples",
            "0",
            "--stop-left-factor-triples",
            "4",
            "--batch-size",
            "2",
            "--max-solutions",
            "0",
            "--require-translation-normalized",
            "--normalized-first",
            "--report-dir",
            str(report_dir),
            "--report-prefix",
            "unit-gf5",
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    summary = json.loads(result.stdout)
    assert summary["stopped_reason"] == "target_reached"
    assert summary["next_start_left_factor_triples"] == 4
    assert summary["tested_left_factor_triples"] == 4
    assert len(summary["batches"]) == 2
    assert (report_dir / "unit-gf5-0-2.json").exists()
    assert (report_dir / "unit-gf5-0-2.md").exists()
    assert (report_dir / "unit-gf5-2-4.json").exists()
    assert (report_dir / "unit-gf5-summary.json").exists()


def test_run_belyi_batches_cli_stops_on_solution():
    report_dir = local_temp_dir("belyi-solution")

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--modulus",
            "2",
            "--start-left-factor-triples",
            "0",
            "--stop-left-factor-triples",
            "5",
            "--batch-size",
            "2",
            "--max-solutions",
            "1",
            "--fixed-p2",
            "0,0",
            "--fixed-p3",
            "0,0,0",
            "--fixed-p4",
            "0,0,0,0",
            "--report-dir",
            str(report_dir),
            "--report-prefix",
            "unit-solution",
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    summary = json.loads(result.stdout)
    assert summary["stopped_reason"] == "solution_found"
    assert summary["solutions"]
    assert len(summary["batches"]) == 1
