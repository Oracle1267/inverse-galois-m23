import json
import subprocess
import sys
from pathlib import Path
from uuid import uuid4

from m23verify.belyi import ElkiesIdentityFactors
from m23verify.branch_search import search_lambda_branches, search_lambda_branches_checkpointed


SCRIPT = Path(__file__).parents[1] / "scripts" / "search_lambda_branches.py"
TMP_ROOT = Path(__file__).parent / ".tmp"


def local_temp_path(name: str) -> Path:
    TMP_ROOT.mkdir(parents=True, exist_ok=True)
    return TMP_ROOT / f"{uuid4().hex}-{name}"


def local_temp_dir(name: str) -> Path:
    path = TMP_ROOT / f"{uuid4().hex}-{name}"
    path.mkdir(parents=True, exist_ok=True)
    return path


def degenerate_identity_factors(lam: int = 0) -> ElkiesIdentityFactors:
    return ElkiesIdentityFactors(
        p2=(0, 0),
        p3=(0, 0, 0),
        p4=(0, 0, 0, 0),
        p7=(0, 0, 0, 0, 0, 0, 0),
        p8=(0, 0, 0, 0, 0, 0, 0, 0),
        lam=lam,
    )


def gf7_survivor_factors() -> ElkiesIdentityFactors:
    return ElkiesIdentityFactors(
        p2=(0, 3),
        p3=(6, 3, 3),
        p4=(2, 6, 2, 6),
        p7=(5, 4, 6, 1, 5, 3, 3),
        p8=(1, 3, 5, 5, 6, 2, 6, 0),
        lam=6,
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


def test_checkpointed_lambda_branch_search_writes_depth_checkpoint():
    checkpoint_dir = local_temp_dir("branch-checkpoints")

    result = search_lambda_branches_checkpointed(
        degenerate_identity_factors(),
        prime=2,
        levels=3,
        depth=2,
        beam_width=2,
        max_numerator=10,
        max_denominator=10,
        score_levels=2,
        score_max_numerator=5,
        score_max_denominator=5,
        refine_multiplier=2,
        checkpoint_dir=checkpoint_dir,
        checkpoint_prefix="unit",
    )

    checkpoint = checkpoint_dir / "unit-depth-0.json"
    assert result["status"] == "complete"
    assert result["score_levels"] == 2
    assert result["history"][0]["refined"] <= 4
    assert checkpoint.exists()
    data = json.loads(checkpoint.read_text(encoding="utf-8"))
    assert data["position"] == 0
    assert data["kept"][0]["prefix"] == [0]


def test_search_lambda_branches_cli_supports_checkpointed_mode():
    checkpoint_dir = local_temp_dir("branch-cli-checkpoints")
    out_path = local_temp_path("branch-checkpointed.json")

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
            "--score-levels",
            "2",
            "--score-max-numerator",
            "5",
            "--score-max-denominator",
            "5",
            "--checkpoint-dir",
            str(checkpoint_dir),
            "--checkpoint-prefix",
            "unit-cli",
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
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    report = json.loads(result.stdout)
    assert report["status"] == "complete"
    assert "depth 1/2" in result.stderr
    assert (checkpoint_dir / "unit-cli-depth-0.json").exists()
    assert out_path.exists()


def test_checkpointed_lambda_branch_search_allows_score_levels_below_depth():
    checkpoint_dir = local_temp_dir("branch-low-score-levels")

    result = search_lambda_branches_checkpointed(
        gf7_survivor_factors(),
        prime=7,
        levels=3,
        depth=2,
        beam_width=1,
        max_numerator=0,
        max_denominator=1,
        score_levels=1,
        score_max_numerator=0,
        score_max_denominator=1,
        refine_multiplier=1,
        checkpoint_dir=checkpoint_dir,
        checkpoint_prefix="gf7-unit",
        digits=(0, 1),
    )

    assert result["status"] == "partial"
    assert len(result["history"]) == 2
    assert (checkpoint_dir / "gf7-unit-depth-1.json").exists()


def test_checkpointed_lambda_branch_resume_uses_highest_numeric_depth():
    checkpoint_dir = local_temp_dir("branch-resume-order")
    base_checkpoint = {
        "prime": 2,
        "levels": 12,
        "depth": 11,
        "beam_width": 1,
        "score_levels": 2,
        "max_numerator": 10,
        "max_denominator": 10,
        "score_max_numerator": 5,
        "score_max_denominator": 5,
        "refine_multiplier": 2,
        "digit_options": [0, 1],
        "kept": [{"prefix": []}],
    }
    for position in (9, 10):
        checkpoint = {
            **base_checkpoint,
            "position": position,
            "evaluated_branches": position,
            "history": [{"position": position, "kept": [{"prefix": []}]}],
        }
        (checkpoint_dir / f"unit-depth-{position}.json").write_text(
            json.dumps(checkpoint),
            encoding="utf-8",
        )

    result = search_lambda_branches_checkpointed(
        degenerate_identity_factors(),
        prime=2,
        levels=12,
        depth=11,
        beam_width=1,
        max_numerator=10,
        max_denominator=10,
        score_levels=2,
        score_max_numerator=5,
        score_max_denominator=5,
        checkpoint_dir=checkpoint_dir,
        checkpoint_prefix="unit",
        resume=True,
    )

    assert result["evaluated_branches"] == 10
    assert result["history"][0]["position"] == 10


def test_checkpointed_lambda_branch_resume_rejects_mismatched_parameters():
    checkpoint_dir = local_temp_dir("branch-resume-mismatch")
    checkpoint = {
        "position": 0,
        "prime": 2,
        "levels": 4,
        "depth": 2,
        "beam_width": 1,
        "score_levels": 2,
        "max_numerator": 10,
        "max_denominator": 10,
        "score_max_numerator": 5,
        "score_max_denominator": 5,
        "refine_multiplier": 1,
        "digit_options": [0, 1],
        "evaluated_branches": 2,
        "history": [{"position": 0, "kept": [{"prefix": [0]}]}],
        "kept": [{"prefix": [0]}],
    }
    (checkpoint_dir / "unit-depth-0.json").write_text(json.dumps(checkpoint), encoding="utf-8")

    try:
        search_lambda_branches_checkpointed(
            degenerate_identity_factors(),
            prime=2,
            levels=4,
            depth=2,
            beam_width=2,
            max_numerator=10,
            max_denominator=10,
            score_levels=2,
            score_max_numerator=5,
            score_max_denominator=5,
            refine_multiplier=1,
            checkpoint_dir=checkpoint_dir,
            checkpoint_prefix="unit",
            resume=True,
        )
    except ValueError as exc:
        assert "beam_width" in str(exc)
    else:
        raise AssertionError("expected incompatible checkpoint to be rejected")
