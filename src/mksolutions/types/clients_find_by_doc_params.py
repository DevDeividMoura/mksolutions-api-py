from typing_extensions import TypedDict

__all__ = ["ClientGetByDocParams"]


class ClientFindByDocParams(TypedDict):
    doc: str
    """Only return customers that contain exactly this document."""

