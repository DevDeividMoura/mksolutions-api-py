from .._models import Field, BaseModel
from .._utils._utils import _format_address


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
    latitude: str = Field(..., alias="latitude")
    longitude: str = Field(..., alias="longitude")
    mac_address: str = Field(..., alias="mac_address")
    block_reason: str = Field(..., alias="motivo_bloqueio")
    username: str = Field(..., alias="username")

class ConnectionsByClientIDResponse(BaseModel):
    """
    A response for connections by client returned from the MKSolutions API.
    """

    client_id: int = Field(..., alias="CodigoPessoa")
    client_name: str = Field(..., alias="Nome")
    connections: list[ConnectionByClientID] = Field(..., alias="Conexoes")