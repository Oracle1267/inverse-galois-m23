import json
import subprocess
import sys
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "lift_belyi_survivor.py"


def test_lift_belyi_survivor_cli_lifts_degenerate_seed_to_mod_4():
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--prime",
            "2",
            "--levels",
            "2",
            "--p2",
            "0,0",
            "--p3",
            "0,0,0",
            "--p4",
            "0,0,0,0",
            "--p7",
            "0,0,0,0,0,0,0",
            "--p8",
            "0,0,0,0,0,0,0,0",
            "--lambda",
            "0",
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    report = json.loads(result.stdout)
    assert report["status"] == "lifted"
    assert report["final_modulus"] == 4
    assert report["lifted"]["lam"] == 0


def test_lift_belyi_survivor_cli_accepts_lambda_corrections():
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--prime",
            "7",
            "--levels",
            "2",
            "--p2",
            "0,3",
            "--p3",
            "6,3,3",
            "--p4",
            "2,6,2,6",
            "--p7",
            "5,4,6,1,5,3,3",
            "--p8",
            "1,3,5,5,6,2,6,0",
            "--lambda",
            "6",
            "--lambda-corrections",
            "1",
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    report = json.loads(result.stdout)
    assert report["status"] == "lifted"
    assert report["lifted"]["lam"] == 13
    assert report["steps"][0]["free_values"] == {"lam": 1}
