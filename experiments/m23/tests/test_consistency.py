from copy import deepcopy

import sympy as sp

from m23verify.consistency import _linear_conflicts, _linear_implication_from_expression, partial_consistency_report
from m23verify.consistency import _linear_system_report, _low_degree_groebner_report
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


def test_linear_implication_conflicts_detect_incompatible_symbolic_constraints():
    variable = sp.Symbol("a")
    implications = [
        _linear_implication_from_expression(2 * variable - 4, source="identity", index=1),
        _linear_implication_from_expression(3 * variable - 9, source="identity", index=2),
    ]

    conflicts = _linear_conflicts([item for item in implications if item is not None])

    assert len(conflicts) == 1
    assert conflicts[0]["symbol"] == "a"
    assert conflicts[0]["values"] == ["2", "3"]


def test_linear_system_report_detects_multivariate_inconsistency():
    a = sp.Symbol("a")
    b = sp.Symbol("b")
    records = [
        ("identity", 1, a + b),
        ("identity", 2, a + b - 1),
    ]

    report = _linear_system_report(records)

    assert report["linear_system_equation_count"] == 2
    assert report["linear_system_conflict_count"] == 1
    assert report["linear_system_consistent"] is False


def test_low_degree_groebner_report_detects_inconsistency():
    a = sp.Symbol("a")
    records = [
        ("identity", 1, a**2 - 1),
        ("identity", 2, a - 2),
    ]

    report = _low_degree_groebner_report(records, max_equations=2)

    assert report["groebner_equation_count"] == 2
    assert report["groebner_conflict_count"] == 1
    assert report["groebner_contains_one"] is True
