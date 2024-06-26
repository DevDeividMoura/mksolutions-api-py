from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["ClientFindByDocParams"]


class ClientFindByDocParams(TypedDict):
    doc: str
    """Only return customers that contain exactly this document."""
    output: str
    """Output format. Possible values: 'list'. Default: 'nested'."""

