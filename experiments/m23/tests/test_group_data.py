from pathlib import Path

from m23verify.group_data import M23CycleData, load_m23_cycle_data


DATA_PATH = Path(__file__).parents[1] / "data" / "m23_23t5_cycle_types.json"


def test_load_m23_cycle_data_has_basic_metadata():
    data = load_m23_cycle_data(DATA_PATH)

    assert data.group_label == "23T5"
    assert data.group_name == "M23"
    assert data.degree == 23
    assert data.order == 10200960


def test_m23_cycle_data_accepts_known_cycle_types():
    data = load_m23_cycle_data(DATA_PATH)

    assert data.is_allowed([23])
    assert data.is_allowed([11, 11, 1])
    assert data.is_allowed([7, 7, 7, 1, 1])
    assert data.is_allowed([5, 5, 5, 5, 1, 1, 1])


def test_m23_cycle_data_rejects_generic_s23_style_cycle_type():
    data = load_m23_cycle_data(DATA_PATH)

    assert not data.is_allowed([22, 1])
    assert not data.is_allowed([21, 2])
    assert not data.is_allowed([17, 6])


def test_m23_cycle_data_normalizes_input_order():
    data = M23CycleData(
        group_label="23T5",
        group_name="M23",
        degree=23,
        order=10200960,
        cycle_types=[(11, 11, 1)],
        source_urls=[],
    )

    assert data.is_allowed([1, 11, 11])
