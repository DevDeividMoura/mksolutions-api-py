from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ._client import MKSolutions


class SyncAPIResource:
    _client: "MKSolutions"

    def __init__(self, client: "MKSolutions") -> None:
        self._client = client
        self._get = client.get
