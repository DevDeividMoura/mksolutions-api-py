import logging
from typing import List, Optional

from .._resource import SyncAPIResource
from ..types.connections import Connection, ConnectionsByClientIDResponse

log = logging.getLogger(__name__)

class Connections(SyncAPIResource):

    def get_by_client_id(self, client_id: int) -> Optional[ConnectionsByClientIDResponse]:
        """
        Get connections by client id.

        Arguments:
            client_id: The client id to search for.

        Returns:
            The connections that match the provided client id.
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
        return ConnectionsByClientIDResponse.from_dict(data)

    def get_by_client_doc(self, doc: str) -> List[Connection]:
        """
        Get connections by client document number.

        Arguments:
            doc: The document number to search for.

        Returns:
            A list of connections that match the provided document number.
        """
        clients = self._client.clients.get_by_doc(doc, include_conn=True)
        connections = []

        for client in clients:
            
            if client.connections:
                for con in client.connections:
                    con.client_name = client.name
                    con.client_id = client.id
                connections.extend(client.connections)

        log.debug(f"Found {len(connections)} connections for document {doc}")
        log.debug(f"Connections: {connections}")

        return connections
