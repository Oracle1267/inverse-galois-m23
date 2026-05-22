from pathlib import Path


ROOT = Path(__file__).parents[1]


def test_magma_script_contains_galois_group_checks():
    text = (ROOT / "magma" / "verify_candidate.m").read_text(encoding="utf-8")

    assert "GaloisGroup" in text
    assert "Factorization" in text
    assert "Discriminant" in text


def test_gap_script_contains_m23_action_checks():
    text = (ROOT / "gap" / "group_fingerprints.g").read_text(encoding="utf-8")

    assert "MathieuGroup(23)" in text
    assert "CycleStructurePerm" in text
    assert "TransitiveGroup(23,5)" in text
