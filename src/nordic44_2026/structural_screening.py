from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class Branch:
    from_bus: int
    to_bus: int
    circuit: str
    rate_a_mva: float
    rate_b_mva: float
    rate_c_mva: float


def aggregate_rate_a(branches: Iterable[Branch]) -> float:
    """Parallel-circuit Rate-A sum. Thermal proxy only; not an AC transfer limit."""
    return sum(b.rate_a_mva for b in branches)


def n_minus_one_rate_a(branches: Iterable[Branch]) -> float:
    """Worst single-circuit-outage Rate-A proxy for a pure parallel corridor."""
    rows = list(branches)
    if len(rows) < 2:
        return 0.0
    total = aggregate_rate_a(rows)
    return min(total - b.rate_a_mva for b in rows)


def no3_no4_2015_proxy() -> dict[str, float]:
    branches = [
        Branch(6500, 6700, "1", 800.0, 900.0, 950.0),
        Branch(6500, 6700, "2", 1000.0, 1200.0, 1300.0),
    ]
    return {
        "parallel_rate_a_sum_mva": aggregate_rate_a(branches),
        "n_minus_one_rate_a_proxy_mva": n_minus_one_rate_a(branches),
    }


def aurora_relative_screen() -> dict[str, float]:
    """Documented 2026 change only.

    Fingrid reports approximately +700 MW FI-SE transfer capability after
    Aurora Line. This is intentionally not converted to a branch MVA rating.
    """
    return {
        "fi_se_transfer_capability_increment_mw": 700.0,
    }


if __name__ == "__main__":
    print("NO3-NO4 2015 thermal proxy:", no3_no4_2015_proxy())
    print("Aurora 2026 relative screen:", aurora_relative_screen())
