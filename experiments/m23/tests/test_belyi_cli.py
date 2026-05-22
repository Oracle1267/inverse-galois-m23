import json
import subprocess
import sys
from pathlib import Path
from uuid import uuid4


SCRIPT = Path(__file__).parents[1] / "scripts" / "solve_belyi_modp.py"
TMP_ROOT = Path(__file__).parent / ".tmp"


def local_temp_path(name: str) -> Path:
    TMP_ROOT.mkdir(parents=True, exist_ok=True)
    return TMP_ROOT / f"{uuid4().hex}-{name}"


def test_solve_belyi_modp_cli_finds_fixed_degenerate_solution():
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--modulus",
            "2",
            "--fixed-p2",
            "0,0",
            "--fixed-p3",
            "0,0,0",
            "--fixed-p4",
            "0,0,0,0",
            "--max-solutions",
            "1",
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    report = json.loads(result.stdout)
    assert report["modulus"] == 2
    assert len(report["solutions"]) == 1
    assert report["solutions"][0]["lam"] == 0


def test_solve_belyi_modp_cli_accepts_derivative_flag():
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--modulus",
            "2",
            "--fixed-p2",
            "0,0",
            "--fixed-p3",
            "0,0,0",
            "--fixed-p4",
            "0,0,0,1",
            "--max-solutions",
            "10",
            "--require-derivative",
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    report = json.loads(result.stdout)
    assert report["solutions"] == []
    assert report["derivative_rejections"] == 4


def test_solve_belyi_modp_cli_accepts_translation_normalization_flag():
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--modulus",
            "5",
            "--fixed-p2",
            "1,0",
            "--fixed-p3",
            "0,0,0",
            "--fixed-p4",
            "0,0,0,0",
            "--max-solutions",
            "1",
            "--require-translation-normalized",
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    report = json.loads(result.stdout)
    assert report["normalization_rejections"] == 1
    assert report["tested_lambda_values"] == 0


def test_solve_belyi_modp_cli_accepts_coprime_first_flag():
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--modulus",
            "5",
            "--max-left-factor-triples",
            "10",
            "--max-solutions",
            "0",
            "--require-coprime-left",
            "--coprime-first",
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    report = json.loads(result.stdout)
    assert report["tested_left_factor_triples"] == 10
    assert report["skipped_left_factor_triples"] == 0


def test_solve_belyi_modp_cli_accepts_normalized_first_flag():
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--modulus",
            "5",
            "--fixed-p2",
            "1,0",
            "--fixed-p4",
            "0,0,0,0",
            "--max-left-factor-triples",
            "3",
            "--max-solutions",
            "0",
            "--require-translation-normalized",
            "--normalized-first",
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    report = json.loads(result.stdout)
    assert report["search_options"]["normalized_first"] is True
    assert report["normalization_rejections"] == 0
    assert report["tested_lambda_values"] == 15


def test_solve_belyi_modp_cli_writes_json_and_markdown_reports():
    json_path = local_temp_path("belyi-report.json")
    markdown_path = local_temp_path("belyi-report.md")

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--modulus",
            "2",
            "--fixed-p2",
            "0,0",
            "--fixed-p3",
            "0,0,0",
            "--fixed-p4",
            "0,0,0,0",
            "--max-solutions",
            "1",
            "--out",
            str(json_path),
            "--markdown-out",
            str(markdown_path),
            "--title",
            "Unit Belyi Report",
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    stdout_report = json.loads(result.stdout)
    file_report = json.loads(json_path.read_text(encoding="utf-8"))
    assert stdout_report["solutions"] == file_report["solutions"]
    assert file_report["search_options"]["max_solutions"] == 1
    markdown = markdown_path.read_text(encoding="utf-8")
    assert "# Unit Belyi Report" in markdown
    assert "## Solutions" in markdown
