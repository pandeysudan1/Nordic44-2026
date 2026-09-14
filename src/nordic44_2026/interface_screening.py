from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class InterfaceCase:
    name: str
    base_capacity_mw: float
    delta_capacity_mw: float = 0.0

    @property
    def capacity_mw(self) -> float:
        return self.base_capacity_mw + self.delta_capacity_mw


def transfer_margin(capacity_mw: float, scheduled_transfer_mw: float) -> float:
    """Return remaining transfer margin in MW.

    Positive means headroom remains; negative means the schedule exceeds the
    simplified interface ceiling. This is a screening metric, not AC security.
    """
    return capacity_mw - abs(scheduled_transfer_mw)


def compare_aurora_screen(base_capacity_mw: float, scheduled_transfer_mw: float) -> dict:
    """Compare historical and Aurora-updated FI-SE screening cases.

    The +700 MW value is treated as a documented transfer-capability increment,
    not as an inferred physical branch rating.
    """
    case_2015 = InterfaceCase("Nordic44-2015", base_capacity_mw)
    case_2026 = InterfaceCase("Nordic44-2026-Aurora-v0", base_capacity_mw, 700.0)

    return {
        case_2015.name: {
            "capacity_mw": case_2015.capacity_mw,
            "scheduled_transfer_mw": scheduled_transfer_mw,
            "margin_mw": transfer_margin(case_2015.capacity_mw, scheduled_transfer_mw),
        },
        case_2026.name: {
            "capacity_mw": case_2026.capacity_mw,
            "scheduled_transfer_mw": scheduled_transfer_mw,
            "margin_mw": transfer_margin(case_2026.capacity_mw, scheduled_transfer_mw),
        },
    }
