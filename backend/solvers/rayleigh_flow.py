from __future__ import annotations
import math
from backend.solvers.root_finding import solve_bracketed


def _ray_p_pstar(M: float, gamma: float) -> float:
    return (1.0 + gamma) / (1.0 + gamma * M**2)


def _ray_T_Tstar(M: float, gamma: float) -> float:
    return (M**2 * (1.0 + gamma) ** 2) / (1.0 + gamma * M**2) ** 2


def _ray_rho_rhostar(M: float, gamma: float) -> float:
    return (1.0 + gamma * M**2) / ((1.0 + gamma) * M**2)


def _ray_Tt_Ttstar(M: float, gamma: float) -> float:
    return (
        (2.0 * (1.0 + gamma) * M**2) / (1.0 + gamma * M**2) ** 2
    ) * (1.0 + 0.5 * (gamma - 1.0) * M**2)


def _ray_pt_ptstar(M: float, gamma: float) -> float:
    return _ray_p_pstar(M, gamma) * (
        (1.0 + 0.5 * (gamma - 1.0) * M**2) / ((gamma + 1.0) / 2.0)
    ) ** (gamma / (gamma - 1.0))


import math

def solve_rayleigh(gamma: float, known: str, value: float, branch: str = "subsonic") -> dict:
    if gamma <= 1.0:
        raise ValueError("gamma must be > 1")
    if value <= 0:
        raise ValueError("value must be > 0")

    def props(M: float) -> dict:
        p_pstar = _ray_p_pstar(M, gamma)
        T_Tstar = _ray_T_Tstar(M, gamma)

        # Critical entropy gain
        Smax_R = math.log(p_pstar) - (gamma / (gamma - 1.0)) * math.log(T_Tstar)

        return {
            "gamma": float(gamma),
            "M": float(M),
            "p/p*": float(p_pstar),
            "T/T*": float(T_Tstar),
            "rho/rho*": float(_ray_rho_rhostar(M, gamma)),
            "Tt/Tt*": float(_ray_Tt_Ttstar(M, gamma)),
            "pt/pt*": float(_ray_pt_ptstar(M, gamma)),
            "Smax/R": float(Smax_R),
        }

    if known == "M":
        M = float(value)
        if M <= 0:
            raise ValueError("Mach must be > 0")
        return props(M)

    if branch == "subsonic":
        bracket = (1e-6, 0.999999)
    elif branch == "supersonic":
        bracket = (1.000001, 50.0)
    else:
        raise ValueError("branch must be 'subsonic' or 'supersonic'")

    mapping = {
        "p/p*": lambda M: _ray_p_pstar(M, gamma),
        "T/T*": lambda M: _ray_T_Tstar(M, gamma),
        "rho/rho*": lambda M: _ray_rho_rhostar(M, gamma),
        "Tt/Tt*": lambda M: _ray_Tt_Ttstar(M, gamma),
        "pt/pt*": lambda M: _ray_pt_ptstar(M, gamma),
    }

    if known not in mapping:
        raise ValueError("known must be one of: M, p/p*, T/T*, rho/rho*, Tt/Tt*, pt/pt*")

    f = mapping[known]
    target = float(value)

    def root(M: float) -> float:
        return f(M) - target

    try:
        M_sol = solve_bracketed(root, bracket)
    except ValueError:
        raise ValueError(
        "No solution found in selected branch. "
        "Check branch selection or ensure value is physically valid."
    )
    return props(M_sol)

