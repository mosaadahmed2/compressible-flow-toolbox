from solvers.isentropic_solvers import solve_isentropic


def test_isentropic_mach_2():
    res = solve_isentropic(gamma=1.4, known="M", value=2)

    assert abs(res["P_P0"] - 0.1278) < 0.01
    assert abs(res["T_T0"] - 0.5556) < 0.01


def test_isentropic_round_trip():
    res1 = solve_isentropic(1.4, "M", 2)
    p_ratio = res1["P_P0"]

    res2 = solve_isentropic(1.4, "P_P0", p_ratio)

    assert abs(res2["M"] - 2) < 0.01