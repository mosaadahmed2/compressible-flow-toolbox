# backend/api/routes.py
from __future__ import annotations
from fastapi import APIRouter, HTTPException

from backend.api.schemas import IsentropicRequest, IsentropicResponse

from backend.solvers.isentropic_solvers import solve_isentropic


router = APIRouter()

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
