from __future__ import annotations
import math
from backend.solvers.root_finding import solve_bracketed


def _theta_beta_m_eq(beta: float, M1: float, gamma: float, delta: float) -> float:
    """
    θ–β–M relation rewritten as f(beta) = 0
    """
    left = math.tan(delta)

    right = (
        2
        * (1 / math.tan(beta))
        * (M1**2 * math.sin(beta)**2 - 1)
        / (M1**2 * (gamma + math.cos(2 * beta)) + 2)
    )

    return left - right


def solve_oblique_shock(M1: float, delta_deg: float, gamma: float = 1.4) -> dict:
    if gamma <= 1.0:
        raise ValueError("gamma must be > 1")

    if M1 <= 1.0:
        raise ValueError("Upstream Mach number must be > 1")

    if delta_deg <= 0:
        raise ValueError("Deflection angle δ must be > 0")

    delta = math.radians(delta_deg)

    # beta limits
    beta_min = math.asin(1 / M1)
    beta_max = math.pi / 2

   # Solve weak solution only
    beta_lower = beta_min + 1e-6
    beta_upper = math.radians(60)  # upper limit for weak branch

    try:
        beta = solve_bracketed(
            lambda b: _theta_beta_m_eq(b, M1, gamma, delta),
            (beta_lower, beta_upper),
        )
    except ValueError:
        raise ValueError("δ exceeds δ_max (detached shock)")


    # Normal component
    Mn1 = M1 * math.sin(beta)

    if Mn1 <= 1:
        raise ValueError("Invalid normal Mach number (no attached shock)")

    gm1 = gamma - 1.0
    gp1 = gamma + 1.0

    # Normal shock relations
    Mn2_sq = (1 + (gm1 / 2) * Mn1**2) / (gamma * Mn1**2 - gm1 / 2)
    Mn2 = math.sqrt(Mn2_sq)

    # Downstream Mach
    M2 = Mn2 / math.sin(beta - delta)

    p2_p1 = 1 + (2 * gamma / gp1) * (Mn1**2 - 1)
    rho2_rho1 = (gp1 * Mn1**2) / (gm1 * Mn1**2 + 2)
    T2_T1 = p2_p1 / rho2_rho1

    return {
        "gamma": float(gamma),
        "M1": float(M1),
        "delta_deg": float(delta_deg),
        "beta_deg": math.degrees(beta),
        "Mn1": float(Mn1),
        "Mn2": float(Mn2),
        "M2": float(M2),
        "p2/p1": float(p2_p1),
        "rho2/rho1": float(rho2_rho1),
        "T2/T1": float(T2_T1),
    }
