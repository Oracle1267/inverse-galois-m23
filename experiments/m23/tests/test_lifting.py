from m23verify.belyi import ElkiesIdentityFactors
from m23verify.lifting import lift_elkies_solution_mod_prime_power


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


def test_lift_elkies_solution_lifts_exact_degenerate_seed_to_mod_8():
    report = lift_elkies_solution_mod_prime_power(
        degenerate_identity_factors(),
        prime=2,
        levels=3,
    )

    assert report["status"] == "lifted"
    assert report["final_modulus"] == 8
    assert len(report["steps"]) == 2
    assert all(step["status"] == "lifted" for step in report["steps"])
    assert report["lifted"]["p2"] == [0, 0]
    assert report["lifted"]["lam"] == 0


def test_lift_elkies_solution_reports_invalid_seed():
    report = lift_elkies_solution_mod_prime_power(
        degenerate_identity_factors(lam=1),
        prime=2,
        levels=2,
    )

    assert report["status"] == "invalid_seed"
    assert report["steps"] == []
    assert report["final_modulus"] == 2


def test_lift_elkies_solution_lifts_gf7_survivor_to_mod_49():
    report = lift_elkies_solution_mod_prime_power(
        gf7_survivor_factors(),
        prime=7,
        levels=2,
    )

    assert report["status"] == "lifted"
    assert report["final_modulus"] == 49
    assert report["steps"][0]["rank"] == 24
    assert report["steps"][0]["residual_mod_target_all_zero"] is True
    assert report["lifted"]["p2"] == [21, 24]
    assert report["lifted"]["lam"] == 6
