from copy import deepcopy

from m23verify.consistency import partial_consistency_report
from m23verify.reconstruction import reconstruct_lift_report


def degenerate_reconstruction():
    return reconstruct_lift_report(
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


def test_partial_consistency_accepts_exact_reconstruction():
    report = partial_consistency_report(degenerate_reconstruction())

    assert report["hard_contradiction_count"] == 0
    assert report["symbolic_constraint_count"] == 0
    assert report["unknown_count"] == 0


def test_partial_consistency_detects_hard_contradiction():
    reconstruction = degenerate_reconstruction()
    reconstruction["reconstructed"]["p2"][0]["value"] = {"numerator": 1, "denominator": 1}

    report = partial_consistency_report(reconstruction)

    assert report["hard_contradiction_count"] > 0
    assert "identity" in {item["source"] for item in report["hard_contradictions"]}


def test_partial_consistency_keeps_symbolic_unknowns_out_of_hard_contradictions():
    reconstruction = deepcopy(degenerate_reconstruction())
    reconstruction["reconstructed"]["p8"][7] = {
        "candidate_count": 0,
        "candidates": [],
        "status": "none",
        "value": None,
    }

    report = partial_consistency_report(reconstruction)

    assert report["unknown_count"] == 1
    assert report["unknowns"] == ["p8[7]"]
    assert report["hard_contradiction_count"] == 0
    assert report["symbolic_constraint_count"] > 0
