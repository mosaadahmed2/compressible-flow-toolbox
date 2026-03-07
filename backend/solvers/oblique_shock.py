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


def _compute_oblique_shock(
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

def solve_oblique_shock(
    gamma: float,
    known: str,
    value: float,
    delta_deg: float,
    shock_type: Literal["weak", "strong"] = "weak",
) -> dict:

    if known == "M1":

        M1 = float(value)

        if M1 <= 1:
            raise ValueError("Upstream Mach must be > 1")

        return _compute_oblique_shock(M1, delta_deg, gamma, shock_type)

    elif known == "M2":

        target_M2 = float(value)

        if target_M2 <= 0:
            raise ValueError("Downstream Mach must be > 0")

        def f(M1):
            try:
                result = _compute_oblique_shock(
                    M1, delta_deg, gamma, shock_type
                )

                return result["M2"] - target_M2

            except Exception:
                # return large positive number so solver keeps searching
                return 1e3

        # search for valid bracket first
        M_min = max(1.0001, target_M2)
        M_max = 50
        N = 200

        grid = [
            M_min + (M_max - M_min) * i / N
            for i in range(N + 1)
        ]

        bracket = None

        for i in range(N):
            try:
                f1 = f(grid[i])
                f2 = f(grid[i+1])
                if f1 * f2 < 0:
                    bracket = (grid[i], grid[i+1])
                    break
            except Exception:
                continue

        if bracket is None:
            raise ValueError("No upstream Mach solution found")

        M1 = solve_bracketed(f, bracket)

        return _compute_oblique_shock(M1, delta_deg, gamma, shock_type)

    else:
        raise ValueError("known must be 'M1' or 'M2'")
