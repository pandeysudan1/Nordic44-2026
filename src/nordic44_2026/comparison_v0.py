from __future__ import annotations


def historical_corridor_metrics() -> dict[str, float]:
    """CI-validated DC baseline metrics from the pinned 2015 Nordic44 case."""
    no3_to_no4 = -131.17 + -181.61
    se_to_fi = -324.75 + 464.74
    return {
        "no3_to_no4_net_mw": no3_to_no4,
        "no4_to_no3_net_mw": -no3_to_no4,
        "se_to_fi_net_ac_mw": se_to_fi,
    }


def comparison_2026_v0() -> dict[str, float | str]:
    """First defensible 2015-to-2026 comparison before a 2026 dispatch snapshot.

    The 2026-v0 structural overlay does not alter the solved historical dispatch.
    It records only quantified structural capability changes. Aurora Line is a
    +700 MW FI-SE transfer-capability increment. NO3-NO4 branch parameters are
    intentionally unchanged until an equivalent-network calibration is done.
    """
    h = historical_corridor_metrics()
    return {
        **h,
        "fi_se_capability_increment_2026_mw": 700.0,
        "no3_no4_parameter_change_v0": "none-until-calibrated",
        "dispatch_change_v0": "none-structural-screen-only",
    }
