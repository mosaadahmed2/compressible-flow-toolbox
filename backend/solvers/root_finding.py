# backend/solvers/root_finding.py
"""
Robust root-finding helpers.
Prefer bracketed solvers for reliability.

Uses SciPy brentq if available; falls back to bisection.
"""

from __future__ import annotations
from typing import Callable, Tuple

def solve_bisection(
    f: Callable[[float], float],
    bracket: Tuple[float, float],
    *,
    xtol: float = 1e-10,
    maxiter: int = 200
) -> float:
    a, b = bracket
    fa, fb = f(a), f(b)
    if fa == 0: return float(a)
    if fb == 0: return float(b)
    if fa * fb > 0:
        raise ValueError("Bisection requires f(a) and f(b) to have opposite signs (valid bracket).")

    for _ in range(maxiter):
        c = 0.5 * (a + b)
        fc = f(c)
        if abs(b - a) < xtol or fc == 0:
            return float(c)
        if fa * fc < 0:
            b, fb = c, fc
        else:
            a, fa = c, fc
    return float(0.5 * (a + b))

def solve_bracketed(
    f: Callable[[float], float],
    bracket: Tuple[float, float],
    *,
    xtol: float = 1e-10,
    rtol: float = 1e-10,
    maxiter: int = 200
) -> float:
    try:
        from scipy.optimize import brentq
        a, b = bracket
        return float(brentq(f, a, b, xtol=xtol, rtol=rtol, maxiter=maxiter))
    except Exception:
        # SciPy missing or failure: fall back to bisection
        return solve_bisection(f, bracket, xtol=xtol, maxiter=maxiter)
