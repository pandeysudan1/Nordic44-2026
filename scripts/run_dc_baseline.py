from __future__ import annotations

import csv
from pathlib import Path
from urllib.request import urlopen

from nordic44_2026.dc_powerflow import angle_validation, solve_dc
from nordic44_2026.raw_parser import parse_raw

RAW_URL = (
    "https://raw.githubusercontent.com/ALSETLab/Nordic44-Nordpool/"
    "49d467a017afb8f70a6ed9f60ac1cb278c35f282/"
    "nordic44/models/N44_BC.raw"
)


def _corridor_rows(rows: list[dict], a: int, b: int) -> list[dict]:
    return [r for r in rows if {int(r["from_bus"]), int(r["to_bus"])} == {a, b}]


def main() -> None:
    text = urlopen(RAW_URL, timeout=30).read().decode("utf-8")
    case = parse_raw(text)
    sol = solve_dc(case)
    validation = angle_validation(case, sol)

    print(f"base_mva={case.base_mva:g}")
    print(f"buses={len(case.buses)} loads={len(case.loads)} generators={len(case.generators)} branches={len(case.branches)} transformers={len(case.transformers)}")
    print(f"slack_bus={sol.slack_bus}")
    print(f"specified_injection_sum_mw={sum(sol.specified_injection_mw.values()):.3f}")
    print(f"slack_balance_mw={sol.slack_balance_mw:.3f}")
    print(f"dc_vs_raw_angle_mae_deg={validation['mae_deg']:.4f}")
    print(f"dc_vs_raw_angle_max_abs_error_deg={validation['max_abs_error_deg']:.4f}")

    no34 = _corridor_rows(sol.branch_flows_mw, 6500, 6700)
    print("NO3-NO4 6500-6700 branch flows:")
    for row in no34:
        print(
            f"  ckt={row['circuit']} flow_mw={row['flow_mw']:.2f} "
            f"rateA_mva={row['rate_a_mva']:.0f} loading_pct={row['loading_rate_a_pct']:.1f}"
        )

    fi_se1 = _corridor_rows(sol.branch_flows_mw, 3115, 7100)
    fi_se2 = _corridor_rows(sol.branch_flows_mw, 3249, 7100)
    print("FI-SE AC tie branch flows in historical reduced model:")
    for row in fi_se1 + fi_se2:
        print(
            f"  {row['from_bus']}-{row['to_bus']} ckt={row['circuit']} "
            f"flow_mw={row['flow_mw']:.2f} loading_pct={row['loading_rate_a_pct']:.1f}"
        )

    out = Path("artifacts")
    out.mkdir(exist_ok=True)
    raw_angles = {b.bus_id: b.va_deg for b in case.buses}
    raw_shift = raw_angles[sol.slack_bus]
    with (out / "dc_baseline_bus_angles.csv").open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["bus_id", "raw_angle_shifted_deg", "dc_angle_deg", "abs_error_deg"])
        for b in case.buses:
            raw_angle = b.va_deg - raw_shift
            dc_angle = sol.angles_deg[b.bus_id]
            w.writerow([b.bus_id, raw_angle, dc_angle, abs(raw_angle - dc_angle)])

    with (out / "dc_baseline_branch_flows.csv").open("w", newline="") as fh:
        fields = ["from_bus", "to_bus", "circuit", "flow_mw", "rate_a_mva", "loading_rate_a_pct"]
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(sol.branch_flows_mw)


if __name__ == "__main__":
    main()
