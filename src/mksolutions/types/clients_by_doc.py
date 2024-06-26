from __future__ import annotations

from .._models import Field, BaseModel

__all__ = ["ClientByDocResponse"]

class ClientByDoc(BaseModel):
    """
    A sub-client returned from the MKSolutions API.
    """
    id: int = Field(..., alias="CodigoPessoa")
    name: str = Field(..., alias="Nome")
    email: str = Field(..., alias="Email")
    phone: str = Field(..., alias="Fone")
    address: str = Field(..., alias="Endereco")
    postal: str = Field(..., alias="CEP")
    latitude: str = Field(..., alias="Latitude")
    longitude: str = Field(..., alias="Longitude")
    status: str = Field(..., alias="Situacao")