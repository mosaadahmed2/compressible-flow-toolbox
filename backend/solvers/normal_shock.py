# backend/solvers/normal_shock.py
"""
Normal shock relations (perfect gas).

Valid for upstream Mach number: 1 < M1 < 10 (per project requirement).
All formulas assume a calorically perfect gas with constant gamma.
"""

from __future__ import annotations
import math
from typing import Dict
from backend.solvers.root_finding import solve_bracketed


def _isentropic_total_pressure_ratio(M: float, gamma: float) -> float:
    """
    pt/p for isentropic flow:
    pt/p = (1 + (gamma-1)/2 * M^2)^(gamma/(gamma-1))
    """
    a = (gamma - 1.0) / 2.0
    return (1.0 + a * M * M) ** (gamma / (gamma - 1.0))


def _normal_shock_M2(M1: float, gamma: float) -> float:
    gm1 = gamma - 1.0
    gp1 = gamma + 1.0

    M2_sq = (1 + (gm1/2) * M1**2) / (gamma*M1**2 - gm1/2)
    return math.sqrt(M2_sq)


def solve_normal_shock(
    gamma: float,
    known: str,
    value: float
) -> dict:

    if gamma <= 1:
        raise ValueError("gamma must be > 1")

    # ---------------- Determine M1 ----------------
    if known == "M1":

        M1 = float(value)

        if M1 <= 1:
            raise ValueError("Upstream Mach must be > 1 for a shock")

    elif known == "M2":

        target_M2 = float(value)

        if target_M2 <= 0 or target_M2 >= 1:
            raise ValueError("Downstream Mach must be between 0 and 1")

        def f(M1):
            return _normal_shock_M2(M1, gamma) - target_M2

        M1 = solve_bracketed(f, (1.0001, 50))

    else:
        raise ValueError("known must be M1 or M2")

    # ---------------- Compute properties ----------------

    gm1 = gamma - 1
    gp1 = gamma + 1

    Mn1 = M1

    Mn2_sq = (1 + (gm1/2)*Mn1**2)/(gamma*Mn1**2 - gm1/2)
    Mn2 = math.sqrt(Mn2_sq)

    M2 = Mn2

    p2_p1 = 1 + (2*gamma/gp1)*(Mn1**2 - 1)

    rho2_rho1 = (gp1*Mn1**2)/(gm1*Mn1**2 + 2)

    T2_T1 = p2_p1 / rho2_rho1

    return {
        "gamma": gamma,
        "M1": M1,
        "M2": M2,
        "p2/p1": p2_p1,
        "rho2/rho1": rho2_rho1,
        "T2/T1": T2_T1
    }
