from m23verify.timeout_review import (
    render_sage_groebner_script,
    render_singular_groebner_script,
    timeout_prefixes_from_branch_report,
    review_timeout_prefixes,
)


def test_timeout_prefixes_from_branch_report_deduplicates_in_order():
    report = {
        "history": [
            {
                "timeout_candidates": [
                    {"prefix": [1, 2], "final_lambda": 10},
                    {"prefix": [3, 4], "final_lambda": 20},
                ]
            },
            {
                "timeout_candidates": [
                    {"prefix": [1, 2], "final_lambda": 10},
                    {"prefix": [5, 6], "final_lambda": 30},
                ]
            },
        ]
    }

    assert timeout_prefixes_from_branch_report(report) == [[1, 2], [3, 4], [5, 6]]


def test_review_timeout_prefixes_classifies_conflict_timeout_and_survivor():
    reports = {
        (1,): {
            "prefix": [1],
            "groebner_conflict_count": 1,
            "groebner_timeout_count": 0,
        },
        (2,): {
            "prefix": [2],
            "groebner_conflict_count": 0,
            "groebner_timeout_count": 1,
        },
        (3,): {
            "prefix": [3],
            "groebner_conflict_count": 0,
            "groebner_timeout_count": 0,
        },
    }

    def evaluator(prefix):
        summary = reports[tuple(prefix)]
        return summary, {"lift": "ignored"}, {"reconstruction": "ignored"}

    result = review_timeout_prefixes([[1], [2], [3]], evaluator=evaluator)

    assert [entry["classification"] for entry in result["reviews"]] == [
        "reject",
        "timeout",
        "survivor",
    ]
    assert result["classification_counts"] == {
        "reject": 1,
        "timeout": 1,
        "survivor": 1,
    }


def test_render_external_groebner_scripts_use_symbols_and_equations():
    equations = [
        {"expression": "a + b - 1"},
        {"expression": "a*b - 2"},
    ]
    symbols = ["a", "b"]

    sage = render_sage_groebner_script(equations, symbols=symbols)
    singular = render_singular_groebner_script(equations, symbols=symbols)

    assert "R.<a,b> = PolynomialRing(QQ, order='lex')" in sage
    assert "ideal([a + b - 1, a*b - 2])" in sage
    assert "I.groebner_basis()" in sage
    assert "ring r = 0,(a,b),lp;" in singular
    assert "ideal I = a + b - 1, a*b - 2;" in singular
    assert "groebner(I)" in singular


def test_render_external_groebner_scripts_normalize_bracketed_symbols():
    equations = [{"expression": "p2_1 + p8_7**2"}]
    symbols = ["p2[1]", "p8[7]"]

    sage = render_sage_groebner_script(equations, symbols=symbols)
    singular = render_singular_groebner_script(equations, symbols=symbols)

    assert "R.<p2_1,p8_7>" in sage
    assert "ring r = 0,(p2_1,p8_7),lp;" in singular
