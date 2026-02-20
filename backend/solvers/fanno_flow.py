from __future__ import annotations
import math
from backend.solvers.root_finding import solve_bracketed


def _fanno_T_Tstar(M: float, gamma: float) -> float:
    # T/T* = 1 / [(2/(g+1))*(1 + (g-1)/2 * M^2)]
    return 1.0 / ((2.0 / (gamma + 1.0)) * (1.0 + 0.5 * (gamma - 1.0) * M**2))


def _fanno_p_pstar(M: float, gamma: float) -> float:
    # p/p* = (1/M) / sqrt[(2/(g+1))*(1 + (g-1)/2 * M^2)]
    denom = math.sqrt((2.0 / (gamma + 1.0)) * (1.0 + 0.5 * (gamma - 1.0) * M**2))
    return (1.0 / M) * (1.0 / denom)


def _fanno_rho_rhostar(M: float, gamma: float) -> float:
    # rho/rho* = (1/M) * sqrt[(2/(g+1))*(1 + (g-1)/2 * M^2)]
    factor = math.sqrt((2.0 / (gamma + 1.0)) * (1.0 + 0.5 * (gamma - 1.0) * M**2))
    return (1.0 / M) * factor


def _fanno_pt_ptstar(M: float, gamma: float) -> float:
    # pt/pt* = (1/M) * [(2/(g+1))*(1 + (g-1)/2 M^2)]^{(g+1)/(2(g-1))}
    base = (2.0 / (gamma + 1.0)) * (1.0 + 0.5 * (gamma - 1.0) * M**2)
    exp = (gamma + 1.0) / (2.0 * (gamma - 1.0))
    return (1.0 / M) * (base ** exp)


def _fanno_4fL_D(M: float, gamma: float) -> float:
    # 4fL*/D = (1 - M^2)/(g M^2) + (g+1)/(2g) ln[ M^2 / ((2/(g+1))*(1+(g-1)/2 M^2)) ]
    term1 = (1.0 - M**2) / (gamma * M**2)
    inside = (M**2) / ((2.0 / (gamma + 1.0)) * (1.0 + 0.5 * (gamma - 1.0) * M**2))
    term2 = (gamma + 1.0) / (2.0 * gamma) * math.log(inside)
    return term1 + term2


def solve_fanno(gamma: float, known: str, value: float, branch: str = "subsonic") -> dict:
    if gamma <= 1.0:
        raise ValueError("gamma must be > 1")
    if value <= 0 and known != "4fL/D":
        raise ValueError("value must be > 0")

    def props(M: float) -> dict:
        return {
            "gamma": float(gamma),
            "M": float(M),
            "T/T*": float(_fanno_T_Tstar(M, gamma)),
            "p/p*": float(_fanno_p_pstar(M, gamma)),
            "rho/rho*": float(_fanno_rho_rhostar(M, gamma)),
            "pt/pt*": float(_fanno_pt_ptstar(M, gamma)),
            "4fL/D": float(_fanno_4fL_D(M, gamma)),
        }

    if known == "M":
        M = float(value)
        if M <= 0:
            raise ValueError("Mach must be > 0")
        return props(M)

    # Choose bracket based on branch
    if branch == "subsonic":
        bracket = (1e-6, 0.999999)
    elif branch == "supersonic":
        bracket = (1.000001, 50.0)
    else:
        raise ValueError("branch must be 'subsonic' or 'supersonic'")

    # map known -> function(M)
    mapping = {
        "T/T*": lambda M: _fanno_T_Tstar(M, gamma),
        "p/p*": lambda M: _fanno_p_pstar(M, gamma),
        "rho/rho*": lambda M: _fanno_rho_rhostar(M, gamma),
        "pt/pt*": lambda M: _fanno_pt_ptstar(M, gamma),
        "4fL/D": lambda M: _fanno_4fL_D(M, gamma),
    }
    if known not in mapping:
        raise ValueError("known must be one of: M, T/T*, p/p*, rho/rho*, pt/pt*, 4fL/D")

    f = mapping[known]
    target = float(value)

    def root(M: float) -> float:
        return f(M) - target

    M_sol = solve_bracketed(root, bracket)
    return props(M_sol)
