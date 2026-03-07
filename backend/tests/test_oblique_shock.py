from solvers.oblique_shock import solve_oblique_shock


def test_oblique_shock_weak():

    res = solve_oblique_shock(
        gamma=1.4,
        known="M1",
        value=2.5,
        delta_deg=10,
        shock_type="weak"
    )

    assert res["M2"] > 1


def test_oblique_shock_strong():

    res = solve_oblique_shock(
        gamma=1.4,
        known="M1",
        value=2.5,
        delta_deg=10,
        shock_type="strong"
    )

    assert res["M2"] < 1