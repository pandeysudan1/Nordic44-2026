from pathlib import Path

import matplotlib.pyplot as plt

from nordic44_2026.structural_screening import aurora_relative_screen, no3_no4_2015_proxy


OUT = Path("docs/figures")
OUT.mkdir(parents=True, exist_ok=True)


def plot_no3_no4() -> None:
    result = no3_no4_2015_proxy()
    labels = ["Circuit 1 Rate A", "Circuit 2 Rate A", "Parallel sum", "N-1 proxy"]
    values = [800.0, 1000.0, result["parallel_rate_a_sum_mva"], result["n_minus_one_rate_a_proxy_mva"]]
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(labels, values)
    ax.set_ylabel("MVA")
    ax.set_title("Nordic44-2015 NO3-NO4 thermal screening")
    ax.text(0.01, -0.20, "Thermal branch-rating proxy only; not an AC/N-1 secure transfer limit.", transform=ax.transAxes)
    fig.tight_layout()
    fig.savefig(OUT / "no3_no4_2015_thermal_proxy.png", dpi=180)
    plt.close(fig)


def plot_aurora() -> None:
    increment = aurora_relative_screen()["fi_se_transfer_capability_increment_mw"]
    fig, ax = plt.subplots(figsize=(6, 4.5))
    ax.bar(["Aurora Line\n2026-v0 overlay"], [increment])
    ax.set_ylabel("MW")
    ax.set_title("Documented FI-SE transfer-capability increment")
    ax.text(0.01, -0.20, "+700 MW is an interface-capability increment, not a branch MVA rating.", transform=ax.transAxes)
    fig.tight_layout()
    fig.savefig(OUT / "aurora_fi_se_increment.png", dpi=180)
    plt.close(fig)


if __name__ == "__main__":
    plot_no3_no4()
    plot_aurora()
    print(f"wrote figures to {OUT}")
