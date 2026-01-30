# backend/tests/test_isentropic.py
import pytest
from backend.solvers.isentropic_solvers import solve_isentropic


def test_mach_direct_smoke():
    out = solve_isentropic(1.4, "M", 2.0)
    assert abs(out["M"] - 2.0) < 1e-12
    assert 0 < out["P_P0"] < 1
    assert 0 < out["T_T0"] < 1
    assert out["A_Astar"] > 1

def test_area_ratio_minimum_at_m1():
    out = solve_isentropic(1.4, "M", 1.0)
    assert abs(out["A_Astar"] - 1.0) < 1e-10

def test_inverse_pressure_round_trip():
    out1 = solve_isentropic(1.4, "M", 2.0)
    out2 = solve_isentropic(1.4, "P_P0", out1["P_P0"])
    assert abs(out2["M"] - 2.0) < 1e-6

def test_invalid_inputs():
    with pytest.raises(ValueError):
        solve_isentropic(1.0, "M", 2.0)  # gamma invalid
    with pytest.raises(ValueError):
        solve_isentropic(1.4, "M", 0.0)  # M invalid
    with pytest.raises(ValueError):
        solve_isentropic(1.4, "P_P0", 1.5)  # ratio invalid
    with pytest.raises(ValueError):
        solve_isentropic(1.4, "A_Astar", 0.9)  # A/A* invalid
