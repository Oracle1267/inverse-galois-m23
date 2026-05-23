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
