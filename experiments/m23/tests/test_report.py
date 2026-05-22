from pathlib import Path

from m23verify.group_data import load_m23_cycle_data
from m23verify.report import build_report


DATA_PATH = Path(__file__).parents[1] / "data" / "m23_23t5_cycle_types.json"


def test_build_report_for_non_degree_23_polynomial():
    data = load_m23_cycle_data(DATA_PATH)
    report = build_report("x^3 - 2", primes=[2, 3, 5, 7], cycle_data=data)

    assert report["summary"]["degree"] == 3
    assert report["classification"] == "reject"
    assert "degree is 3, expected 23" in report["reasons"]


def test_build_report_records_cycle_compatibility():
    data = load_m23_cycle_data(DATA_PATH)
    report = build_report("x^23 - x - 1", primes=[2, 3, 5, 7, 11], cycle_data=data)

    assert "modular_factorizations" in report
    assert all("prime" in item for item in report["modular_factorizations"])
    assert all("cycle_type" in item for item in report["modular_factorizations"])
    assert all("m23_compatible" in item for item in report["modular_factorizations"])
