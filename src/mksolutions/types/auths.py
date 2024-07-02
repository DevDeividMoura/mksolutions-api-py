from __future__ import annotations

from typing import List

from .._models import Field, BaseModel

__all__ = ["AuthSpecificResponse", "AuthGeneralResponse"]


class AuthSpecificResponse(BaseModel):
    adm: str = Field(..., alias="Adm")
    email: str = Field(..., alias="Email")
    fone: str = Field(..., alias="Fone")
    operador: str = Field(..., alias="Operador")
    token: str = Field(..., alias="TokenAutenticacao")
    status: str = Field(..., alias="status")

class AuthGeneralResponse(BaseModel):
    expire: str = Field(..., alias="Expire")
    rate_limit: int = Field(..., alias="LimiteUso")
    auth_services: List[int] = Field(..., alias="ServicosAutorizados")
    token: str = Field(..., alias="Token")
    status: str = Field(..., alias="status")
