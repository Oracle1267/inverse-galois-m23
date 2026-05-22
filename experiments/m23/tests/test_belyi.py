import pytest

from m23verify.belyi import (
    ElkiesIdentityFactors,
    derive_right_factorizations,
    elkies_derivative_residual,
    elkies_identity_residual,
    elkies_translation_normalization_residual,
    is_elkies_derivative_solution,
    is_elkies_identity_solution,
    is_elkies_translation_normalized,
    render_belyi_search_markdown,
    search_elkies_identity_mod_prime,
    monic_polynomial,
)


def degenerate_identity_factors(lam: int = 0) -> ElkiesIdentityFactors:
    return ElkiesIdentityFactors(
        p2=(0, 0),
        p3=(0, 0, 0),
        p4=(0, 0, 0, 0),
        p7=(0, 0, 0, 0, 0, 0, 0),
        p8=(0, 0, 0, 0, 0, 0, 0, 0),
        lam=lam,
    )


def test_monic_polynomial_uses_descending_nonleading_coefficients():
    poly = monic_polynomial(degree=3, coefficients=(2, 0, -1), modulus=5)

    assert str(poly.as_expr()) == "x**3 + 2*x**2 - 1"


def test_monic_polynomial_rejects_wrong_coefficient_count():
    with pytest.raises(ValueError, match="expected 3 coefficients"):
        monic_polynomial(degree=3, coefficients=(1, 2), modulus=5)


def test_elkies_identity_residual_is_zero_for_degenerate_identity():
    residual = elkies_identity_residual(degenerate_identity_factors(), modulus=5)

    assert residual == (0,) * 24
    assert is_elkies_identity_solution(degenerate_identity_factors(), modulus=5)


def test_elkies_identity_residual_detects_constant_mismatch():
    factors = degenerate_identity_factors(lam=1)

    assert elkies_identity_residual(factors, modulus=5)[-1] == 4
    assert not is_elkies_identity_solution(factors, modulus=5)


def test_elkies_derivative_residual_is_zero_for_degenerate_identity():
    residual = elkies_derivative_residual(degenerate_identity_factors(), modulus=5)

    assert residual == (0,) * 23
    assert is_elkies_derivative_solution(degenerate_identity_factors(), modulus=5)


def test_elkies_derivative_residual_rejects_raw_identity_false_positive():
    factors = ElkiesIdentityFactors(
        p2=(0, 0),
        p3=(0, 0, 0),
        p4=(0, 0, 0, 1),
        p7=(0, 0, 0, 0, 0, 0, 0),
        p8=(0, 0, 0, 0, 0, 0, 0, 1),
        lam=0,
    )

    assert is_elkies_identity_solution(factors, modulus=2)
    assert not is_elkies_derivative_solution(factors, modulus=2)


def test_translation_normalization_residual_reads_left_x22_coefficient():
    normalized = degenerate_identity_factors()
    shifted = ElkiesIdentityFactors(
        p2=(1, 0),
        p3=(0, 0, 0),
        p4=(0, 0, 0, 0),
        p7=(0, 0, 0, 0, 0, 0, 0),
        p8=(0, 0, 0, 0, 0, 0, 0, 0),
        lam=0,
    )

    assert elkies_translation_normalization_residual(normalized, modulus=5) == 0
    assert is_elkies_translation_normalized(normalized, modulus=5)
    assert elkies_translation_normalization_residual(shifted, modulus=5) == 2
    assert not is_elkies_translation_normalized(shifted, modulus=5)


def test_derive_right_factorizations_finds_degenerate_square_factor():
    left = monic_polynomial(23, (0,) * 23, modulus=2)

    derived = list(derive_right_factorizations(left, modulus=2))

    assert {
        "p7": (0, 0, 0, 0, 0, 0, 0),
        "p8": (0, 0, 0, 0, 0, 0, 0, 0),
    } in derived


def test_search_elkies_identity_mod_prime_finds_fixed_degenerate_solution():
    result = search_elkies_identity_mod_prime(
        modulus=2,
        fixed_p2=(0, 0),
        fixed_p3=(0, 0, 0),
        fixed_p4=(0, 0, 0, 0),
        max_solutions=1,
    )

    assert result["tested_left_factor_triples"] == 1
    assert result["solutions"][0]["p2"] == [0, 0]
    assert result["solutions"][0]["p7"] == [0, 0, 0, 0, 0, 0, 0]
    assert result["solutions"][0]["p8"] == [0, 0, 0, 0, 0, 0, 0, 0]


def test_search_elkies_identity_mod_prime_can_reject_non_coprime_left_factors():
    result = search_elkies_identity_mod_prime(
        modulus=2,
        fixed_p2=(0, 0),
        fixed_p3=(0, 0, 0),
        fixed_p4=(0, 0, 0, 0),
        max_solutions=1,
        require_coprime_left=True,
    )

    assert result["tested_left_factor_triples"] == 1
    assert result["skipped_left_factor_triples"] == 1
    assert result["solutions"] == []


def test_search_elkies_identity_mod_prime_can_require_derivative_constraint():
    result = search_elkies_identity_mod_prime(
        modulus=2,
        fixed_p2=(0, 0),
        fixed_p3=(0, 0, 0),
        fixed_p4=(0, 0, 0, 1),
        max_solutions=10,
        require_derivative=True,
    )

    assert result["solutions"] == []
    assert result["derivative_rejections"] == 4


def test_search_elkies_identity_mod_prime_can_require_translation_normalization():
    result = search_elkies_identity_mod_prime(
        modulus=5,
        fixed_p2=(1, 0),
        fixed_p3=(0, 0, 0),
        fixed_p4=(0, 0, 0, 0),
        max_solutions=1,
        require_translation_normalized=True,
    )

    assert result["tested_left_factor_triples"] == 1
    assert result["normalization_rejections"] == 1
    assert result["tested_lambda_values"] == 0
    assert result["solutions"] == []


def test_search_elkies_identity_mod_prime_can_enumerate_coprime_triples_first():
    result = search_elkies_identity_mod_prime(
        modulus=5,
        max_left_factor_triples=10,
        max_solutions=0,
        require_coprime_left=True,
        coprime_first=True,
    )

    assert result["tested_left_factor_triples"] == 10
    assert result["skipped_left_factor_triples"] == 0
    assert result["tested_lambda_values"] == 50


def test_search_elkies_identity_mod_prime_can_generate_normalized_triples_first():
    result = search_elkies_identity_mod_prime(
        modulus=5,
        fixed_p2=(1, 0),
        fixed_p4=(0, 0, 0, 0),
        max_left_factor_triples=3,
        max_solutions=0,
        require_translation_normalized=True,
        normalized_first=True,
    )

    assert result["search_options"]["normalized_first"] is True
    assert result["tested_left_factor_triples"] == 3
    assert result["normalization_rejections"] == 0
    assert result["tested_lambda_values"] == 15


def test_render_belyi_search_markdown_includes_options_and_solutions():
    result = {
        "modulus": 2,
        "search_options": {
            "require_coprime_left": False,
            "require_derivative": False,
            "require_nonzero_lambda": False,
            "require_translation_normalized": False,
            "coprime_first": False,
            "max_left_factor_triples": None,
            "max_solutions": 1,
        },
        "enumerated_left_factor_triples": 1,
        "tested_left_factor_triples": 1,
        "skipped_left_factor_triples": 0,
        "tested_lambda_values": 1,
        "normalization_rejections": 0,
        "derivative_rejections": 0,
        "stopped_reason": "max_solutions",
        "solutions": [
            {
                "p2": [0, 0],
                "p3": [0, 0, 0],
                "p4": [0, 0, 0, 0],
                "p7": [0, 0, 0, 0, 0, 0, 0],
                "p8": [0, 0, 0, 0, 0, 0, 0, 0],
                "lam": 0,
            }
        ],
    }

    markdown = render_belyi_search_markdown(result, title="Unit Belyi Report")

    assert "# Unit Belyi Report" in markdown
    assert "## Search Options" in markdown
    assert "| require_coprime_left | False |" in markdown
    assert "## Solutions" in markdown
    assert "`[0, 0]`" in markdown
