from .._models import BaseModel
from .._utils import _format_address

class ClientByDoc(BaseModel):
    """
    A client returned from the MKSolutions API.
    """
    id: int
    name: str
    email: str
    phone: str
    address: str
    cep: str
    latitude: str
    longitude: str
    status: str

    @classmethod
    def from_dict(cls, data: dict) -> "ClientByDoc":
        return cls(
            id=data["CodigoPessoa"],
            name=data["Nome"],
            email=data["Email"],
            phone=data["Fone"],
            address= _format_address(data["Endereco"]),
            cep=data["CEP"],
            latitude=data["Latitude"],
            longitude=data["Longitude"],
            status=data["Situacao"],
        )

