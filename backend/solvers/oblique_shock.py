# backend/solvers/oblique_shock.py
from __future__ import annotations
import math


def solve_oblique_shock(M1: float, beta_deg: float, gamma: float = 1.4) -> dict:
    if gamma <= 1.0:
        raise ValueError("gamma must be > 1")

    if M1 <= 1.0:
        raise ValueError("Upstream Mach number must be > 1")

    if not (0.0 < beta_deg < 90.0):
        raise ValueError("Shock angle beta must be between 0 and 90 degrees")

    beta = math.radians(beta_deg)

    # Normal component of Mach
    Mn1 = M1 * math.sin(beta)
    if Mn1 <= 1.0:
        raise ValueError("Normal Mach number must be > 1 for a shock")

    gm1 = gamma - 1.0
    gp1 = gamma + 1.0

    # Normal shock relations
    Mn2_sq = (1 + (gm1 / 2) * Mn1**2) / (gamma * Mn1**2 - gm1 / 2)
    if Mn2_sq <= 0:
        raise ValueError("Invalid downstream normal Mach number")

    Mn2 = math.sqrt(Mn2_sq)

    # Flow deflection angle theta
    tan_theta = (
        2 * (Mn1**2 - 1)
        / (math.tan(beta) * (M1**2 * (gamma + math.cos(2 * beta)) + 2))
    )
    theta = math.atan(tan_theta)

    # Downstream Mach number
    M2 = Mn2 / math.sin(beta - theta)

    # Ratios
    p2_p1 = 1 + (2 * gamma / gp1) * (Mn1**2 - 1)
    rho2_rho1 = (gp1 * Mn1**2) / (gm1 * Mn1**2 + 2)
    T2_T1 = p2_p1 / rho2_rho1

    return {
        "M1": float(M1),
        "beta_deg": float(beta_deg),
        "Mn1": float(Mn1),
        "Mn2": float(Mn2),
        "M2": float(M2),
        "p2/p1": float(p2_p1),
        "rho2/rho1": float(rho2_rho1),
        "T2/T1": float(T2_T1),
    }
