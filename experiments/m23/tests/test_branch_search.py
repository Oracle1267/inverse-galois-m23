import json
import subprocess
import sys
from pathlib import Path
from uuid import uuid4

from m23verify.belyi import ElkiesIdentityFactors
from m23verify.branch_search import search_lambda_branches


SCRIPT = Path(__file__).parents[1] / "scripts" / "search_lambda_branches.py"
TMP_ROOT = Path(__file__).parent / ".tmp"


def local_temp_path(name: str) -> Path:
    TMP_ROOT.mkdir(parents=True, exist_ok=True)
    return TMP_ROOT / f"{uuid4().hex}-{name}"


def degenerate_identity_factors(lam: int = 0) -> ElkiesIdentityFactors:
    return ElkiesIdentityFactors(
        p2=(0, 0),
        p3=(0, 0, 0),
        p4=(0, 0, 0, 0),
        p7=(0, 0, 0, 0, 0, 0, 0),
        p8=(0, 0, 0, 0, 0, 0, 0, 0),
        lam=lam,
    )


def test_search_lambda_branches_tracks_beam_history_for_exact_seed():
    result = search_lambda_branches(
        degenerate_identity_factors(),
        prime=2,
        levels=3,
        depth=2,
        beam_width=2,
        max_numerator=10,
        max_denominator=10,
    )

    assert result["status"] == "complete"
    assert result["evaluated_branches"] <= 6
    assert len(result["history"]) == 1
    assert result["best"]["prefix"] == [0]
    assert result["best_reconstruction"]["exact_identity"] is True


def test_search_lambda_branches_cli_writes_reports():
    out_path = local_temp_path("branch-search.json")
    markdown_path = local_temp_path("branch-search.md")

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--prime",
            "2",
            "--levels",
            "3",
            "--depth",
            "2",
            "--beam-width",
            "2",
            "--max-numerator",
            "10",
            "--max-denominator",
            "10",
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
            "--out",
            str(out_path),
            "--markdown-out",
            str(markdown_path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    report = json.loads(result.stdout)
    assert report["best"]["prefix"] == [0]
    assert out_path.exists()
    assert markdown_path.exists()
