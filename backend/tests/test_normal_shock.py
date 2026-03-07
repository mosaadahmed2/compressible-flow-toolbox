from solvers.normal_shock import solve_normal_shock


def test_normal_shock_mach_2():

    res = solve_normal_shock(
        gamma=1.4,
        known="M1",
        value=2
    )

    assert abs(res["M2"] - 0.577) < 0.01
    assert abs(res["p2/p1"] - 4.5) < 0.1


def test_normal_shock_inverse():

    res = solve_normal_shock(
        gamma=1.4,
        known="M2",
        value=0.577
    )

    assert abs(res["M1"] - 2) < 0.05