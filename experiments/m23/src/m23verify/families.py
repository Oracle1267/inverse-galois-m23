from __future__ import annotations

from collections.abc import Iterable, Iterator


def parse_int_range(raw: str) -> tuple[int, int]:
    left, separator, right = raw.partition(":")
    if separator != ":":
        value = int(raw)
        return value, value
    start = int(left)
    end = int(right)
    if start > end:
        raise ValueError(f"range start must be <= end: {raw}")
    return start, end


def _format_linear_term(coefficient: int) -> str:
    if coefficient == 1:
        return " + x"
    if coefficient == -1:
        return " - x"
    if coefficient > 0:
        return f" + {coefficient}*x"
    return f" - {abs(coefficient)}*x"


def _format_constant(value: int) -> str:
    if value > 0:
        return f" + {value}"
    return f" - {abs(value)}"


def format_trinomial(a: int, b: int) -> str:
    if a == 0:
        raise ValueError("a must be nonzero for the trinomial family")
    if b == 0:
        raise ValueError("b must be nonzero for the trinomial family")
    return f"x^23{_format_linear_term(a)}{_format_constant(b)}"


def _candidate_parameters(a_range: tuple[int, int], b_range: tuple[int, int]) -> list[tuple[int, int]]:
    a_values = [value for value in range(a_range[0], a_range[1] + 1) if value != 0]
    b_values = [value for value in range(b_range[0], b_range[1] + 1) if value != 0]
    return sorted(
        ((a, b) for a in a_values for b in b_values),
        key=lambda item: (abs(item[0]) + abs(item[1]), abs(item[0]), abs(item[1]), item[0], item[1]),
    )


def generate_trinomial_candidates(
    a_range: tuple[int, int],
    b_range: tuple[int, int],
    max_candidates: int,
    seen: Iterable[str] | None = None,
) -> Iterator[str]:
    if max_candidates <= 0:
        return
    seen_set = set(seen or [])
    yielded = 0
    for a, b in _candidate_parameters(a_range, b_range):
        candidate = format_trinomial(a, b)
        if candidate in seen_set:
            continue
        yield candidate
        yielded += 1
        if yielded >= max_candidates:
            return


def count_trinomial_candidates(a_range: tuple[int, int], b_range: tuple[int, int]) -> int:
    return len(_candidate_parameters(a_range, b_range))
