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


class NormalShockRequest(BaseModel):
    gamma: float = Field(1.4, gt=1.0, description="Heat capacity ratio (default 1.4)")
    M1: float = Field(..., gt=0.0, description="Upstream Mach number (must be > 1 for a normal shock)")


class NormalShockResponse(BaseModel):
    M1: float
    M2: float
    p2_p1: float = Field(..., alias="p2/p1")
    rho2_rho1: float = Field(..., alias="rho2/rho1")
    T2_T1: float = Field(..., alias="T2/T1")
    pt2_pt1: float = Field(..., alias="pt2/pt1")

    class Config:
        populate_by_name = True

class ObliqueShockRequest(BaseModel):
    gamma: float = Field(1.4, gt=1.0)
    M1: float = Field(..., gt=1.0)
    beta_deg: float = Field(..., gt=0.0, lt=90.0)

class FannoRequest(BaseModel):
    gamma: float = Field(1.4, gt=1.0)
    known: Literal["M", "T/T*", "p/p*", "rho/rho*", "pt/pt*", "4fL/D"]
    value: float
    branch: Optional[Literal["subsonic", "supersonic"]] = "subsonic"

class RayleighRequest(BaseModel):
    gamma: float = Field(1.4, gt=1.0)
    known: Literal["M", "p/p*", "T/T*", "rho/rho*", "Tt/Tt*", "pt/pt*"]
    value: float
    branch: Optional[Literal["subsonic", "supersonic"]] = "subsonic"

