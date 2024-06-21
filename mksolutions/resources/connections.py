import logging
from typing import List, Optional

from .._resource import SyncAPIResource
from ..types.connections import ConnectionsByClientResponse

log = logging.getLogger(__name__)

class Connections(SyncAPIResource):

    def get_by_client_id(self, client_id: int) -> Optional[ConnectionsByClientResponse]:
        """
        Get connections by client id.

        Arguments:
            id: The client id to search for.

        Returns:
            A list of connections that match the provided client id.
        """
        response = self._get(
            "/mk/WSMKConexoesPorCliente.rule", 
            options={
                "sys": "MK0",
                "token": self._client.api_key,
                "cd_cliente": client_id
                }
        )

        data = response.json()
        # print(data)
        return ConnectionsByClientResponse.from_dict(data)

