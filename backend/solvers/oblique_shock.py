from __future__ import annotations
import math
from typing import Literal
from backend.solvers.root_finding import solve_bracketed


def _theta_beta_m_eq(beta: float, M1: float, gamma: float, delta: float) -> float:
    """
    θ–β–M relation rewritten as f(beta) = 0
    """
    left = math.tan(delta)

    right = (
        2
        * (1 / math.tan(beta))
        * (M1**2 * math.sin(beta) ** 2 - 1)
        / (M1**2 * (gamma + math.cos(2 * beta)) + 2)
    )

    return left - right


def solve_oblique_shock(
    M1: float,
    delta_deg: float,
    gamma: float = 1.4,
    shock_type: Literal["weak", "strong"] = "weak",
) -> dict:

    if gamma <= 1.0:
        raise ValueError("gamma must be > 1")

    if M1 <= 1.0:
        raise ValueError("Upstream Mach number must be > 1")

    if delta_deg <= 0:
        raise ValueError("Deflection angle δ must be > 0")

    delta = math.radians(delta_deg)

    # Beta limits
    beta_min = math.asin(1 / M1)          # Mach angle
    beta_max = math.pi / 2                # 90 degrees

    # Function wrapper
    def f(beta):
        return _theta_beta_m_eq(beta, M1, gamma, delta)

    # Scan beta range and collect ALL valid roots
    N = 200
    betas = [
        beta_min + (beta_max - beta_min) * i / N
        for i in range(N + 1)
    ]

    roots = []

    for i in range(N):
        if f(betas[i]) * f(betas[i + 1]) < 0:
            try:
                root = solve_bracketed(f, (betas[i], betas[i + 1]))
                roots.append(root)
            except Exception:
                continue

    if not roots:
        raise ValueError("δ exceeds δ_max (detached shock)")

    # Sort roots
    roots = sorted(roots)

    # Select weak or strong
    if shock_type == "weak":
        beta = roots[0]      # smaller beta
    else:
        beta = roots[-1]     # larger beta

    # ---------------- Compute downstream properties ----------------

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
        "shock_type": shock_type,
        "beta_deg": math.degrees(beta),
        "Mn1": float(Mn1),
        "Mn2": float(Mn2),
        "M2": float(M2),
        "p2/p1": float(p2_p1),
        "rho2/rho1": float(rho2_rho1),
        "T2/T1": float(T2_T1),
    }
