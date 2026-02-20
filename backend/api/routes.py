# backend/api/routes.py
from __future__ import annotations
from fastapi import APIRouter, HTTPException

from backend.api.schemas import (
    IsentropicRequest,
    IsentropicResponse,
    NormalShockRequest,
)
from backend.solvers.isentropic_solvers import solve_isentropic
from backend.solvers.normal_shock import solve_normal_shock

from backend.solvers.oblique_shock import solve_oblique_shock
from backend.api.schemas import ObliqueShockRequest

from backend.solvers.fanno_flow import solve_fanno
from backend.solvers.rayleigh_flow import solve_rayleigh
from backend.api.schemas import FannoRequest, RayleighRequest


router = APIRouter()

@router.post("/fanno")
def fanno(req: FannoRequest):
    try:
        return solve_fanno(gamma=req.gamma, known=req.known, value=req.value, branch=req.branch)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.post("/rayleigh")
def rayleigh(req: RayleighRequest):
    try:
        return solve_rayleigh(gamma=req.gamma, known=req.known, value=req.value, branch=req.branch)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e



@router.post("/oblique-shock")
def oblique_shock(req: ObliqueShockRequest):
    """
    Oblique shock relations.
    Inputs: M1, beta (deg), gamma
    """
    try:
        return solve_oblique_shock(
            M1=req.M1,
            beta_deg=req.beta_deg,
            gamma=req.gamma,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

# -----------------------
# Isentropic endpoint
# -----------------------
@router.post("/isentropic", response_model=IsentropicResponse)
def isentropic(req: IsentropicRequest):
    try:
        result = solve_isentropic(
            gamma=req.gamma,
            known=req.known,
            value=req.value,
            branch=req.branch,
        )
        return IsentropicResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


# -----------------------
# Normal shock endpoint
# -----------------------
@router.post("/normal-shock")
def normal_shock(req: NormalShockRequest):
    """
    Normal shock relations.
    Valid for 1 < M1 < 10 (project constraint).
    """
    try:
        return solve_normal_shock(M1=req.M1, gamma=req.gamma)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
