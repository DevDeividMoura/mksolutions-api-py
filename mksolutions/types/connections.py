from .._models import BaseModel
from .._utils import _format_address

class Connection(BaseModel):
    """
    A connection returned from the MKSolutions API.
    """
    blocked: str
    registration: str
    postal: str
    id: int
    contract_id: int | str
    address: str
    is_reduced: str
    latitude: str
    longitude: str
    mac_address: str
    block_reason: str
    username: str

    @classmethod
    def from_dict(cls, data: dict) -> "Connection":
        return cls(
            blocked=data["bloqueada"],
            registration=data["cadastro"],
            postal=data["cep"] or "",
            id=data["codconexao"],
            contract_id=data["contrato"] or "",
            address=_format_address(data["endereco"]),
            is_reduced=data["esta_reduzida"],
            latitude=data["latitude"] or "",
            longitude=data["longitude"] or "",
            mac_address=data["mac_address"],
            block_reason=data["motivo_bloqueio"] or "",
            username=data["username"],
        )

class ConnectionsByClientResponse(BaseModel):
    """
    A response for connections by client returned from the MKSolutions API.
    """
    client_id: int
    client_name: str
    connections: list[Connection]
    

    @classmethod
    def from_dict(cls, data: dict) -> "ConnectionsByClientResponse":
        return cls(
            client_id=data["CodigoPessoa"],
            client_name=data["Nome"],
            connections=[Connection.from_dict(conexao) for conexao in data["Conexoes"]],
            
        )
