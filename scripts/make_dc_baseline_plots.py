from __future__ import annotations

from pathlib import Path
from urllib.request import urlopen

import matplotlib.pyplot as plt

from nordic44_2026.dc_powerflow import solve_dc
from nordic44_2026.raw_parser import parse_raw

RAW_URL = (
    "https://raw.githubusercontent.com/ALSETLab/Nordic44-Nordpool/"
    "49d467a017afb8f70a6ed9f60ac1cb278c35f282/"
    "nordic44/models/N44_BC.raw"
)

OUT = Path("artifacts/figures")


def load_case():
    text = urlopen(RAW_URL, timeout=30).read().decode("utf-8")
    case = parse_raw(text)
    return case, solve_dc(case)


def plot_angles(case, sol):
    OUT.mkdir(parents=True, exist_ok=True)
    raw = {b.bus_id: b.va_deg for b in case.buses}
    shift = raw[sol.slack_bus]
    bus_ids = [b.bus_id for b in case.buses]
    raw_angles = [raw[i] - shift for i in bus_ids]
    dc_angles = [sol.angles_deg[i] for i in bus_ids]

    fig, ax = plt.subplots(figsize=(10, 4.8))
    ax.plot(range(len(bus_ids)), raw_angles, marker="o", markersize=3, label="Historical RAW angle")
    ax.plot(range(len(bus_ids)), dc_angles, marker="x", markersize=3, label="DC reconstruction")
    ax.set_xlabel("Nordic44 bus index")
    ax.set_ylabel("Angle relative to slack (deg)")
    ax.set_title("Nordic44-2015: historical vs DC bus-angle validation")
    ax.legend()
    ax.grid(True, alpha=0.25)
    fig.tight_layout()
    fig.savefig(OUT / "dc_vs_raw_bus_angles.png", dpi=180)
    plt.close(fig)


def plot_key_loading(sol):
    key = []
    wanted = {(6500, 6700), (3115, 7100), (3249, 7100)}
    for row in sol.branch_flows_mw:
        pair = (int(row["from_bus"]), int(row["to_bus"]))
        if pair in wanted:
            key.append(row)

    labels = [f"{r['from_bus']}-{r['to_bus']} c{r['circuit']}" for r in key]
    values = [float(r["loading_rate_a_pct"]) for r in key]
    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    ax.bar(labels, values)
    ax.set_ylabel("|DC flow| / Rate A (%)")
    ax.set_title("Nordic44-2015 key corridor loading proxies")
    ax.grid(True, axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(OUT / "key_corridor_loading.png", dpi=180)
    plt.close(fig)


def plot_2026_schematic():
    fig, ax = plt.subplots(figsize=(9, 5.5))
    pos = {
        "NO3\n6500": (0.15, 0.65),
        "NO4\n6700": (0.15, 0.90),
        "SE1\n3115": (0.55, 0.88),
        "SE2\n3249": (0.55, 0.65),
        "FI\n7100": (0.86, 0.76),
        "NO5\n5301": (0.15, 0.30),
    }
    for name, (x, y) in pos.items():
        ax.scatter([x], [y], s=600)
        ax.text(x, y, name, ha="center", va="center", fontsize=9)

    def edge(a, b, text, style="-"):
        x1, y1 = pos[a]
        x2, y2 = pos[b]
        ax.plot([x1, x2], [y1, y2], linestyle=style, linewidth=2)
        ax.text((x1 + x2) / 2, (y1 + y2) / 2, text, fontsize=8, ha="center", va="bottom")

    edge("NO3\n6500", "NO4\n6700", "2015: two circuits\n2026-v0: unchanged until calibrated")
    edge("SE1\n3115", "FI\n7100", "2015 AC tie")
    edge("SE2\n3249", "FI\n7100", "2015 AC tie")
    edge("SE1\n3115", "FI\n7100", "Aurora overlay: +700 MW interface capability", style="--")
    edge("NO5\n5301", "NO3\n6500", "physical reinforcements screened;\nreduction pending", style=":")

    ax.set_xlim(0, 1)
    ax.set_ylim(0.15, 1.02)
    ax.axis("off")
    ax.set_title("Nordic44 2015 → 2026-v0 structural-screening schematic")
    fig.tight_layout()
    fig.savefig(OUT / "nordic44_2026_v0_corridor_schematic.png", dpi=180)
    plt.close(fig)


if __name__ == "__main__":
    case, sol = load_case()
    plot_angles(case, sol)
    plot_key_loading(sol)
    plot_2026_schematic()
    print(f"wrote figures to {OUT}")
