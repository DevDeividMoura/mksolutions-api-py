from typing_extensions import TypedDict

__all__ = ["ClientFindByDocParams"]


class ClientFindByDocParams(TypedDict):
    doc: str
    """Only return customers that contain exactly this document."""

