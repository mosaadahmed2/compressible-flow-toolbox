# backend/api/schemas.py
from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Literal, Optional

Known = Literal["M", "P_P0", "T_T0", "A_Astar"]
Branch = Literal["subsonic", "supersonic"]

class IsentropicRequest(BaseModel):
    gamma: float = Field(1.4, gt=1.0, description="Specific heat ratio γ (> 1).")
    known: Known = Field(..., description="Which variable is provided.")
    value: float = Field(..., description="Value of the known variable.")
    branch: Optional[Branch] = Field(None, description="Used only when known='A_Astar'.")

class IsentropicResponse(BaseModel):
    gamma: float
    M: float
    T_T0: float
    P_P0: float
    rho_rho0: float
    A_Astar: float
