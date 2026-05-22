from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Iterable


def normalize_cycle_type(cycle_type: Iterable[int]) -> tuple[int, ...]:
    normalized = tuple(sorted((int(part) for part in cycle_type), reverse=True))
    if not normalized:
        raise ValueError("cycle type cannot be empty")
    if any(part <= 0 for part in normalized):
        raise ValueError(f"cycle type parts must be positive: {normalized}")
    return normalized


@dataclass(frozen=True)
class M23CycleData:
    group_label: str
    group_name: str
    degree: int
    order: int
    cycle_types: list[tuple[int, ...]]
    source_urls: list[str]

    def __post_init__(self) -> None:
        for cycle_type in self.cycle_types:
            if sum(cycle_type) != self.degree:
                raise ValueError(
                    f"cycle type {cycle_type} has degree {sum(cycle_type)}, expected {self.degree}"
                )

    @property
    def allowed_cycle_types(self) -> set[tuple[int, ...]]:
        return {normalize_cycle_type(cycle_type) for cycle_type in self.cycle_types}

    def is_allowed(self, cycle_type: Iterable[int]) -> bool:
        return normalize_cycle_type(cycle_type) in self.allowed_cycle_types


def load_m23_cycle_data(path: str | Path) -> M23CycleData:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    return M23CycleData(
        group_label=raw["group_label"],
        group_name=raw["group_name"],
        degree=int(raw["degree"]),
        order=int(raw["order"]),
        cycle_types=[normalize_cycle_type(item) for item in raw["cycle_types"]],
        source_urls=list(raw["source_urls"]),
    )
