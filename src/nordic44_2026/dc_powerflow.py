from __future__ import annotations

from dataclasses import dataclass
from math import pi

from .raw_parser import RawCase


@dataclass(frozen=True)
class DCSolution:
    slack_bus: int
    angles_deg: dict[int, float]
    branch_flows_mw: list[dict[str, float | int | str]]
    transformer_flows_mw: list[dict[str, float | int | str]]
    specified_injection_mw: dict[int, float]
    slack_balance_mw: float


def _solve_linear(a: list[list[float]], b: list[float]) -> list[float]:
    """Small dense Gaussian elimination with partial pivoting; avoids extra solver dependencies."""
    n = len(b)
    m = [row[:] + [b[i]] for i, row in enumerate(a)]
    for k in range(n):
        pivot = max(range(k, n), key=lambda r: abs(m[r][k]))
        if abs(m[pivot][k]) < 1e-12:
            raise ValueError("DC susceptance matrix is singular; check network connectivity")
        m[k], m[pivot] = m[pivot], m[k]
        for i in range(k + 1, n):
            f = m[i][k] / m[k][k]
            if f == 0.0:
                continue
            for j in range(k, n + 1):
                m[i][j] -= f * m[k][j]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        rhs = m[i][n] - sum(m[i][j] * x[j] for j in range(i + 1, n))
        x[i] = rhs / m[i][i]
    return x


def solve_dc(case: RawCase) -> DCSolution:
    bus_ids = [b.bus_id for b in case.buses]
    idx = {bus_id: i for i, bus_id in enumerate(bus_ids)}
    slack_candidates = [b.bus_id for b in case.buses if b.bus_type == 3]
    if len(slack_candidates) != 1:
        raise ValueError(f"Expected exactly one slack bus, found {slack_candidates}")
    slack = slack_candidates[0]

    p = {bus_id: 0.0 for bus_id in bus_ids}
    for g in case.generators:
        if g.status:
            p[g.bus_id] += g.p_mw
    for load in case.loads:
        if load.status:
            p[load.bus_id] -= load.p_mw

    n = len(bus_ids)
    bmat = [[0.0 for _ in range(n)] for _ in range(n)]

    def add_link(i_bus: int, j_bus: int, x_pu: float) -> None:
        if abs(x_pu) < 1e-12:
            raise ValueError(f"Zero reactance link {i_bus}-{j_bus}")
        y = 1.0 / x_pu
        i = idx[i_bus]
        j = idx[j_bus]
        bmat[i][i] += y
        bmat[j][j] += y
        bmat[i][j] -= y
        bmat[j][i] -= y

    for br in case.branches:
        if br.status:
            add_link(br.from_bus, br.to_bus, br.x_pu)
    for tr in case.transformers:
        if tr.status:
            add_link(tr.from_bus, tr.to_bus, tr.x_pu)

    keep = [bus_id for bus_id in bus_ids if bus_id != slack]
    red = [[bmat[idx[i]][idx[j]] for j in keep] for i in keep]
    rhs = [p[i] / case.base_mva for i in keep]
    theta_red = _solve_linear(red, rhs)
    theta_rad = {slack: 0.0}
    theta_rad.update({bus_id: theta_red[k] for k, bus_id in enumerate(keep)})
    angles = {bus_id: theta * 180.0 / pi for bus_id, theta in theta_rad.items()}

    branch_flows = []
    for br in case.branches:
        if not br.status:
            continue
        flow = case.base_mva * (theta_rad[br.from_bus] - theta_rad[br.to_bus]) / br.x_pu
        branch_flows.append({
            "from_bus": br.from_bus,
            "to_bus": br.to_bus,
            "circuit": br.circuit,
            "flow_mw": flow,
            "rate_a_mva": br.rate_a_mva,
            "loading_rate_a_pct": 100.0 * abs(flow) / br.rate_a_mva if br.rate_a_mva > 0 else float("nan"),
        })

    transformer_flows = []
    for tr in case.transformers:
        if not tr.status:
            continue
        flow = case.base_mva * (theta_rad[tr.from_bus] - theta_rad[tr.to_bus]) / tr.x_pu
        transformer_flows.append({
            "from_bus": tr.from_bus,
            "to_bus": tr.to_bus,
            "circuit": tr.circuit,
            "flow_mw": flow,
        })

    slack_balance = -sum(p.values())
    return DCSolution(slack, angles, branch_flows, transformer_flows, p, slack_balance)


def angle_validation(case: RawCase, sol: DCSolution) -> dict[str, float]:
    raw = {b.bus_id: b.va_deg for b in case.buses}
    shift = raw[sol.slack_bus]
    errors = [abs(sol.angles_deg[b.bus_id] - (b.va_deg - shift)) for b in case.buses]
    return {
        "mae_deg": sum(errors) / len(errors),
        "max_abs_error_deg": max(errors),
    }
