from m23verify.families import generate_trinomial_candidates, parse_int_range


def test_parse_int_range_supports_negative_bounds():
    assert parse_int_range("-2:3") == (-2, 3)


def test_trinomial_generator_formats_small_candidates_and_skips_seen():
    candidates = list(
        generate_trinomial_candidates(
            a_range=(-1, 1),
            b_range=(-1, 1),
            max_candidates=4,
            seen={"x^23 - x - 1"},
        )
    )

    assert "x^23 - x - 1" not in candidates
    assert candidates == [
        "x^23 - x + 1",
        "x^23 + x - 1",
        "x^23 + x + 1",
    ]


def test_trinomial_generator_respects_zero_candidate_limit():
    candidates = list(
        generate_trinomial_candidates(
            a_range=(-1, 1),
            b_range=(-1, 1),
            max_candidates=0,
        )
    )

    assert candidates == []
