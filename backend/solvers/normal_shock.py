# backend/solvers/normal_shock.py
"""
Normal shock relations (perfect gas).

Valid for upstream Mach number: 1 < M1 < 10 (per project requirement).
All formulas assume a calorically perfect gas with constant gamma.
"""

from __future__ import annotations
import math
from typing import Dict


def _isentropic_total_pressure_ratio(M: float, gamma: float) -> float:
    """
    pt/p for isentropic flow:
    pt/p = (1 + (gamma-1)/2 * M^2)^(gamma/(gamma-1))
    """
    a = (gamma - 1.0) / 2.0
    return (1.0 + a * M * M) ** (gamma / (gamma - 1.0))


def solve_normal_shock(M1: float, gamma: float = 1.4) -> Dict[str, float]:
    """
    Compute normal shock downstream Mach and key ratios:
    - M2
    - p2/p1
    - rho2/rho1
    - T2/T1
    - pt2/pt1 (total pressure loss)

    Raises ValueError for invalid inputs.
    """
    if not (gamma > 1.0):
        raise ValueError("gamma must be > 1.0")

    # Project-defined validity range (matches Davis note)
    if not (1.0 < M1 < 10.0):
        raise ValueError("Normal shock is valid for upstream Mach number 1 < M1 < 10.")

    M1_sq = M1 * M1
    gm1 = gamma - 1.0
    gp1 = gamma + 1.0

    # Downstream Mach number (M2)
    denom = gamma * M1_sq - gm1 / 2.0
    if denom <= 0:
        raise ValueError("Invalid state: downstream Mach computation denominator <= 0.")
    M2_sq = (1.0 + (gm1 / 2.0) * M1_sq) / denom
    if M2_sq <= 0:
        raise ValueError("Invalid state: computed M2^2 <= 0.")
    M2 = math.sqrt(M2_sq)

    # Pressure ratio p2/p1
    p2_p1 = 1.0 + (2.0 * gamma / gp1) * (M1_sq - 1.0)
    if p2_p1 <= 0:
        raise ValueError("Invalid state: computed p2/p1 <= 0.")

    # Density ratio rho2/rho1
    rho2_rho1 = (gp1 * M1_sq) / (gm1 * M1_sq + 2.0)
    if rho2_rho1 <= 0:
        raise ValueError("Invalid state: computed rho2/rho1 <= 0.")

    # Temperature ratio T2/T1
    T2_T1 = p2_p1 / rho2_rho1
    if T2_T1 <= 0:
        raise ValueError("Invalid state: computed T2/T1 <= 0.")

    # Total pressure ratio pt2/pt1
    # pt = p * (pt/p)
    pt1_p1 = _isentropic_total_pressure_ratio(M1, gamma)
    pt2_p2 = _isentropic_total_pressure_ratio(M2, gamma)
    pt2_pt1 = (p2_p1 * pt2_p2) / pt1_p1
    if pt2_pt1 <= 0:
        raise ValueError("Invalid state: computed pt2/pt1 <= 0.")

    return {
        "M1": float(M1),
        "M2": float(M2),
        "p2/p1": float(p2_p1),
        "rho2/rho1": float(rho2_rho1),
        "T2/T1": float(T2_T1),
        "pt2/pt1": float(pt2_pt1),
    }
