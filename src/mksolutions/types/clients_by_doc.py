from __future__ import annotations

from .._models import Field, BaseModel
from .._utils._utils import _format_address  # Import utilizado para formatação de endereços, se necessário

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

    def __init__(self, **data):
        super().__init__(**data)
        # Exemplo de formatação de endereço se necessário
        self.address = _format_address(self.address)