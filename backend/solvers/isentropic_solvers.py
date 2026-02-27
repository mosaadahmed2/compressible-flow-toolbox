# backend/solvers/isentropic_solvers.py
from __future__ import annotations

import math
from typing import Dict, Literal

from backend.core.isentropic import T_T0, P_P0, rho_rho0, A_Astar
from backend.solvers.root_finding import solve_bracketed


Known = Literal["M", "P_P0", "T_T0", "A_Astar"]

def _finite(x: float, name: str) -> None:
    if not isinstance(x, (int, float)) or math.isnan(x) or math.isinf(x):
        raise ValueError(f"{name} must be a finite number")

def _validate_gamma(gamma: float) -> None:
    _finite(gamma, "gamma")
    if gamma <= 1.0:
        raise ValueError("gamma must be > 1.0")

def solve_mach_from_pressure_ratio(gamma: float, target: float) -> float:
    _validate_gamma(gamma)
    _finite(target, "P/P0")
    if not (0.0 < target < 1.0):
        raise ValueError("P/P0 must be in (0, 1) for isentropic flow")

    def f(M: float) -> float:
        return P_P0(gamma, M) - target

    # P/P0 decreases monotonically with M for M>0
    return solve_bracketed(f, (1e-8, 50.0))

def solve_mach_from_temperature_ratio(gamma: float, target: float) -> float:
    _validate_gamma(gamma)
    _finite(target, "T/T0")
    if not (0.0 < target < 1.0):
        raise ValueError("T/T0 must be in (0, 1) for isentropic flow")

    def f(M: float) -> float:
        return T_T0(gamma, M) - target

    # T/T0 decreases monotonically with M for M>0
    return solve_bracketed(f, (1e-8, 50.0))

def solve_mach_from_area_ratio(
    gamma: float,
    target: float,
    branch: Literal["subsonic", "supersonic"] = "subsonic",
) -> float:
    _validate_gamma(gamma)
    _finite(target, "A/A*")
    if target < 1.0:
        raise ValueError("A/A* must be >= 1.0 (minimum occurs at M=1)")
    if abs(target - 1.0) < 1e-12:
        return 1.0

    def f(M: float) -> float:
        return A_Astar(gamma, M) - target

    # A/A* has two solutions when target > 1:
    # subsonic: M in (0,1)
    # supersonic: M in (1,∞)
    if branch == "subsonic":
        return solve_bracketed(f, (1e-8, 1.0 - 1e-8))
    elif branch == "supersonic":
        return solve_bracketed(f, (1.0 + 1e-8, 50.0))
    else:
        raise ValueError("branch must be 'subsonic' or 'supersonic'")

def solve_isentropic(
    gamma: float,
    known: Known,
    value: float,
    *,
    branch: Literal["subsonic", "supersonic"] | None = None
) -> Dict[str, float]:
    """
    Returns all standard isentropic outputs given one known value.
    - known: "M", "P_P0", "T_T0", "A_Astar"
    - branch is only used when known="A_Astar"
    """

    _validate_gamma(gamma)
    _finite(value, "value")
    known = known.strip()

    # ---------------- Determine Mach number ----------------
    if known == "M":
        M = float(value)
        if M <= 0:
            raise ValueError("Mach number must be > 0")

    elif known == "P_P0":
        M = solve_mach_from_pressure_ratio(gamma, float(value))

    elif known == "T_T0":
        M = solve_mach_from_temperature_ratio(gamma, float(value))

    elif known == "A_Astar":
        if branch is None:
            branch = "subsonic"
        M = solve_mach_from_area_ratio(gamma, float(value), branch=branch)

    else:
        raise ValueError("known must be one of: M, P_P0, T_T0, A_Astar")

    # ---------------- Standard isentropic properties ----------------
    T_ratio = T_T0(gamma, M)
    P_ratio = P_P0(gamma, M)
    rho_ratio = rho_rho0(gamma, M)
    A_ratio = A_Astar(gamma, M)

    # ---------------- Supersonic-only properties ----------------
    if M > 1:
        # Mach angle (μ)
        mu = math.degrees(math.asin(1 / M))

        # Prandtl-Meyer function (ν)
        term1 = math.sqrt((gamma + 1) / (gamma - 1))
        term2 = math.atan(
            math.sqrt((gamma - 1) / (gamma + 1) * (M**2 - 1))
        )
        term3 = math.atan(math.sqrt(M**2 - 1))

        nu = math.degrees(term1 * term2 - term3)
    else:
        mu = None
        nu = None

    # ---------------- Return all results ----------------
    return {
        "gamma": float(gamma),
        "M": float(M),
        "T_T0": float(T_ratio),
        "P_P0": float(P_ratio),
        "rho_rho0": float(rho_ratio),
        "A_Astar": float(A_ratio),
        "mu_deg": mu,
        "nu_deg": nu,
    }
