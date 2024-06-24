from typing_extensions import TypedDict

__all__ = ["ClientGetByDocParams"]


class ClientGetByDocParams(TypedDict):
    doc: str
    """Only return customers that contain exactly this document."""
    include_conn: bool
    """Return the connections associated with each client entity."""