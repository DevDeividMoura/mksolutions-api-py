from typing import Optional

from .._models import BaseModel
from .._utils import _format_address
from .connections import Connection

class ClientByDocResponse(BaseModel):
    """
    A client returned from the MKSolutions API.
    """
    id: int
    name: str
    email: str
    phone: str
    address: str
    postal: str
    latitude: str
    longitude: str
    status: str
    connections: Optional[list[Connection]] = None

    @classmethod
    def from_dict(cls, data: dict) -> "ClientByDocResponse":
        return cls(
            id=data["CodigoPessoa"],
            name=data["Nome"],
            email=data["Email"],
            phone=data["Fone"],
            address= _format_address(data["Endereco"]),
            postal=data["CEP"],
            latitude=data["Latitude"],
            longitude=data["Longitude"],
            status=data["Situacao"],
        )
