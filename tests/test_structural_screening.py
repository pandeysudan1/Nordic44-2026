from nordic44_2026.structural_screening import aurora_relative_screen, no3_no4_2015_proxy


def test_no3_no4_thermal_proxy():
    result = no3_no4_2015_proxy()
    assert result["parallel_rate_a_sum_mva"] == 1800.0
    assert result["n_minus_one_rate_a_proxy_mva"] == 800.0


def test_aurora_increment_is_interface_metric():
    result = aurora_relative_screen()
    assert result["fi_se_transfer_capability_increment_mw"] == 700.0
