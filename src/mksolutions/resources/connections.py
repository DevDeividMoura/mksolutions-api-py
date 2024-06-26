from __future__ import annotations

import logging
from typing import List

from ..types import ConnectionByClientID, ConnectionsByClientIDResponse
from .._resource import SyncAPIResource
from ..types.clients_by_doc import ClientByDoc

log = logging.getLogger(__name__)

class Connections(SyncAPIResource):
    def find_by_client_id(self, client_id: int) -> ConnectionsByClientIDResponse:
        """
        Get connections by client id.

        Arguments:
            client_id: The client id to search for.

        Returns:
            ConnectionsByClientIDResponse: The connections that match the provided client id.
        """
        response = self._get(
            "/mk/WSMKConexoesPorCliente.rule",
            params={
                "sys": "MK0", 
                "token": self._client.api_key, 
                "cd_cliente": client_id
            }
        )

        data = response.json()
        return ConnectionsByClientIDResponse(**data)

    def find_by_client_doc(self, client_doc: str) -> List[ConnectionByClientID]:
        """
        Get connections by client document number.

        Arguments:
            doc: The document number to search for.

        Returns:
            A list of connections that match the provided document number.
        """
        clients_response = self._client.clients.find_by_doc(client_doc)
        main_client = {k: v for k, v in clients_response.to_dict().items() if k not in ["Outros", "status"]}
        clients = [ClientByDoc(**main_client)]
        clients.extend(client for client in clients_response.others)

        connections = []

        for client in clients:
            result = self.find_by_client_id(client.id)
            if result.connections:
                for conn in result.connections:
                    conn.client_name = client.name
                    conn.client_id = client.id
                connections.extend(result.connections)

        log.debug(f"Found {len(connections)} connections for document {client_doc}")
        log.debug(f"Connections: {connections}")

        return connections
