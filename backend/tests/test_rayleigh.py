from solvers.rayleigh_flow import solve_rayleigh


def test_rayleigh_mach_half():

    res = solve_rayleigh(
        gamma=1.4,
        known="M",
        value=0.5
    )

    assert abs(res["p/p*"] - 1.78) < 0.1


def test_rayleigh_entropy_positive():

    res = solve_rayleigh(
        gamma=1.4,
        known="M",
        value=2
    )

    assert res["Smax/R"] > 0