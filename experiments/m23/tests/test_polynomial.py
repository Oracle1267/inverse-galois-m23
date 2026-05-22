import pytest

from m23verify.polynomial import (
    coefficient_digit_count,
    factor_degrees_mod_prime,
    parse_polynomial,
    summarize_polynomial,
)


def test_parse_magma_style_polynomial():
    poly = parse_polynomial("3*x^2 - 2*x + 1")

    assert poly.degree() == 2
    assert [int(c) for c in poly.all_coeffs()] == [3, -2, 1]


def test_parse_rejects_non_integer_coefficients():
    with pytest.raises(ValueError, match="integer coefficients"):
        parse_polynomial("x^2 + 1/2")


def test_coefficient_digit_count():
    assert coefficient_digit_count(0) == 1
    assert coefficient_digit_count(-12345) == 5


def test_factor_degrees_mod_prime_for_cubic():
    poly = parse_polynomial("x^3 - 2")
    factorization = factor_degrees_mod_prime(poly, 5)

    assert factorization.prime == 5
    assert factorization.cycle_type == (2, 1)
    assert factorization.is_good_prime


def test_factor_degrees_marks_bad_prime_when_discriminant_vanishes():
    poly = parse_polynomial("x^2 - 1")
    factorization = factor_degrees_mod_prime(poly, 2)

    assert factorization.prime == 2
    assert factorization.is_good_prime is False


def test_summarize_polynomial_basic_fields():
    summary = summarize_polynomial("x^3 - 2")

    assert summary.degree == 3
    assert summary.is_irreducible is True
    assert summary.coefficient_bound.ok is True
    assert summary.coefficient_bound.max_digits == 1
