from nordic44_2026.dc_powerflow import solve_dc
from nordic44_2026.raw_parser import Branch, Bus, Generator, Load, RawCase


def test_two_bus_dc_flow():
    case = RawCase(
        base_mva=100.0,
        buses=(
            Bus(1, "SLACK", 230.0, 3, 1, 1.0, 0.0),
            Bus(2, "LOAD", 230.0, 1, 1, 1.0, 0.0),
        ),
        loads=(Load(2, "1", 1, 50.0, 0.0),),
        generators=(Generator(1, "1", 50.0, 0.0, 100.0, 1),),
        branches=(Branch(1, 2, "1", 0.0, 0.1, 0.0, 100.0, 1),),
        transformers=(),
    )
    sol = solve_dc(case)
    assert sol.slack_bus == 1
    assert abs(sol.angles_deg[2] + 2.86478897565) < 1e-8
    assert abs(sol.branch_flows_mw[0]["flow_mw"] - 50.0) < 1e-9


def test_out_of_service_load_is_not_counted():
    case = RawCase(
        base_mva=100.0,
        buses=(
            Bus(1, "SLACK", 230.0, 3, 1, 1.0, 0.0),
            Bus(2, "LOAD", 230.0, 1, 1, 1.0, 0.0),
        ),
        loads=(Load(2, "X", 0, 80.0, 0.0),),
        generators=(),
        branches=(Branch(1, 2, "1", 0.0, 0.1, 0.0, 100.0, 1),),
        transformers=(),
    )
    sol = solve_dc(case)
    assert sol.angles_deg[2] == 0.0
