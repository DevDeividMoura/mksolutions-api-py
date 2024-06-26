from __future__ import annotations

from . import ConnectionByClientID
from .._models import Field, BaseModel

__all__ = ["ConnectionsByClientIDResponse"]

class ConnectionsByClientIDResponse(BaseModel):
    """
    A response for connections by client returned from the MKSolutions API.
    """

    client_id: int = Field(..., alias="CodigoPessoa")
    client_name: str = Field(..., alias="Nome")
    connections: list[ConnectionByClientID] = Field(..., alias="Conexoes")
    req_status: str = Field(..., alias="status")