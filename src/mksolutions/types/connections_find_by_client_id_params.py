from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["ConnectionsFindByClientIDParams"]


class ConnectionsFindByClientIDParams(TypedDict):
    client_id: str
    """Only return connections that contain exactly this client id."""
    output: str
    """Output format. Possible values: 'list'. Default: 'nested'."""

