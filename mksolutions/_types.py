from httpx import Timeout, Response

from pydantic import BaseModel

from typing import (
    Union,
    Mapping
)

from typing_extensions import TypedDict

Headers = Mapping[str, str]
Query = Mapping[str, object]
Body = object

class RequestOptions(TypedDict, total=False):
    params: Query
    headers: Headers
    timeout: Union[float, Timeout, None]

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
            address=data["Endereco"],
            cep=data["CEP"],
            latitude=data["Latitude"],
            longitude=data["Longitude"],
            status=data["Situacao"],
        )



