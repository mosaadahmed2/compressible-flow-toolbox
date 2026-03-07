from solvers.fanno_flow import solve_fanno


def test_fanno_mach_2():

    res = solve_fanno(
        gamma=1.4,
        known="M",
        value=2
    )

    assert abs(res["4fL/D"] - 0.305) < 0.05


def test_fanno_entropy():

    res = solve_fanno(
        gamma=1.4,
        known="M",
        value=0.5
    )

    assert res["Smax/R"] > 0