from __future__ import annotations

from .._models import Field, BaseModel

__all__ = ["ConnectionByClientID"]

class ConnectionByClientID(BaseModel):
    """
    A connection returned from the MKSolutions API.
    """

    blocked: str = Field(..., alias="bloqueada")
    registration: str = Field(..., alias="cadastro")
    postal: str = Field(..., alias="cep")
    id: int = Field(..., alias="codconexao")
    contract_id: int | str = Field(..., alias="contrato")
    address: str = Field(..., alias="endereco")
    is_reduced: str = Field(..., alias="esta_reduzida")
    latitude: str | None = Field(..., alias="latitude")
    longitude: str | None = Field(..., alias="longitude")
    mac_address: str = Field(..., alias="mac_address")
    block_reason: str | None = Field(..., alias="motivo_bloqueio")
    username: str = Field(..., alias="username")
