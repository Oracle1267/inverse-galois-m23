import json
import subprocess
import sys
from pathlib import Path
from uuid import uuid4

from m23verify.reconstruction import (
    rational_reconstruct,
    reconstruct_lift_report,
)


SCRIPT = Path(__file__).parents[1] / "scripts" / "reconstruct_belyi_lift.py"
TMP_ROOT = Path(__file__).parent / ".tmp"


def local_temp_path(name: str) -> Path:
    TMP_ROOT.mkdir(parents=True, exist_ok=True)
    return TMP_ROOT / f"{uuid4().hex}-{name}"


def test_rational_reconstruct_recovers_integer_residue():
    result = rational_reconstruct(98, modulus=101, max_numerator=10, max_denominator=10)

    assert result["status"] == "unique"
    assert result["value"] == {"numerator": -3, "denominator": 1}


def test_rational_reconstruct_recovers_fraction_residue():
    residue = (3 * pow(4, -1, 101)) % 101

    result = rational_reconstruct(residue, modulus=101, max_numerator=10, max_denominator=10)

    assert result["status"] == "unique"
    assert result["value"] == {"numerator": 3, "denominator": 4}


def test_reconstruct_lift_report_verifies_degenerate_identity():
    report = reconstruct_lift_report(
        {
            "final_modulus": 8,
            "lifted": {
                "p2": [0, 0],
                "p3": [0, 0, 0],
                "p4": [0, 0, 0, 0],
                "p7": [0, 0, 0, 0, 0, 0, 0],
                "p8": [0, 0, 0, 0, 0, 0, 0, 0],
                "lam": 0,
            },
        },
        max_numerator=10,
        max_denominator=10,
    )

    assert report["status"] == "complete"
    assert report["exact_identity"] is True
    assert report["exact_derivative"] is True
    assert report["exact_translation_normalization"] is True


def test_reconstruct_belyi_lift_cli_reads_lift_json():
    lift_path = local_temp_path("lift.json")
    lift_path.write_text(
        json.dumps(
            {
                "final_modulus": 8,
                "lifted": {
                    "p2": [0, 0],
                    "p3": [0, 0, 0],
                    "p4": [0, 0, 0, 0],
                    "p7": [0, 0, 0, 0, 0, 0, 0],
                    "p8": [0, 0, 0, 0, 0, 0, 0, 0],
                    "lam": 0,
                },
            }
        )
        + "\n",
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--lift-json",
            str(lift_path),
            "--max-numerator",
            "10",
            "--max-denominator",
            "10",
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    report = json.loads(result.stdout)
    assert report["status"] == "complete"
    assert report["exact_identity"] is True
