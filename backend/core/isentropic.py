# backend/core/isentropic.py
"""
Isentropic flow relations for a perfect gas.

All functions here are PURE (no I/O, no API logic).
Conventions:
- gamma > 1
- Mach number M > 0
- Ratios returned are dimensionless
"""

from __future__ import annotations
import math

def _validate_gamma(gamma: float) -> None:
    if not isinstance(gamma, (int, float)) or math.isnan(gamma) or math.isinf(gamma):
        raise ValueError("gamma must be a finite number")
    if gamma <= 1.0:
        raise ValueError("gamma must be > 1.0")

def _validate_M(M: float) -> None:
    if not isinstance(M, (int, float)) or math.isnan(M) or math.isinf(M):
        raise ValueError("Mach number must be a finite number")
    if M <= 0.0:
        raise ValueError("Mach number must be > 0")

def T_T0(gamma: float, M: float) -> float:
    """Static-to-stagnation temperature ratio T/T0."""
    _validate_gamma(gamma); _validate_M(M)
    return 1.0 / (1.0 + (gamma - 1.0) * 0.5 * M * M)

def P_P0(gamma: float, M: float) -> float:
    """Static-to-stagnation pressure ratio P/P0."""
    t = T_T0(gamma, M)
    return t ** (gamma / (gamma - 1.0))

def rho_rho0(gamma: float, M: float) -> float:
    """Static-to-stagnation density ratio ρ/ρ0."""
    t = T_T0(gamma, M)
    return t ** (1.0 / (gamma - 1.0))

def A_Astar(gamma: float, M: float) -> float:
    """Area ratio A/A* for isentropic quasi-1D flow."""
    _validate_gamma(gamma); _validate_M(M)
    # Standard relation:
    # A/A* = (1/M) * [ (2/(γ+1)) * (1 + (γ-1)/2 M^2) ]^((γ+1)/(2(γ-1)))
    term = (2.0 / (gamma + 1.0)) * (1.0 + (gamma - 1.0) * 0.5 * M * M)
    exponent = (gamma + 1.0) / (2.0 * (gamma - 1.0))
    return (1.0 / M) * (term ** exponent)
