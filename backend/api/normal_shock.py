# backend/api/normal_shock.py
from __future__ import annotations
from fastapi import APIRouter, HTTPException

from backend.solvers.normal_shock import solve_normal_shock
from backend.api.schemas import NormalShockRequest

router = APIRouter(tags=["Normal Shock"])


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
