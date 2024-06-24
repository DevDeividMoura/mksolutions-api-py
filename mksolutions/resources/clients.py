import logging
from typing import List, Optional

from .._resource import SyncAPIResource
from ..types.clients import ClientByDocResponse
from ..types.connections import Connection

log = logging.getLogger(__name__)

class Clients(SyncAPIResource):

    def get_by_doc(self, doc: str, include_conn: bool = False) -> List[ClientByDocResponse]:
        """
        Get a client by document number.

        Arguments:
            doc: The document number to search for.
            include_conn: Whether to include connections for each client.

        Returns:
            A list of clients that match the provided document number.
        """
        response = self._get(
            "/mk/WSMKConsultaDoc.rule", 
            options={
                "sys": "MK0",
                "token": self._client.api_key,
                "doc": doc
            }
        )

        data = response.json()

        clients = [ClientByDocResponse.from_dict(data)]
        if "Outros" in data:
            clients.extend(ClientByDocResponse.from_dict(other) for other in data["Outros"])

        if include_conn:
            for client in clients:
                client.connections = self.__get_connections(client.id)

        return clients
    
    def __get_connections(self, client_id: int) -> List[Connection]:
        result = self._client.connections.get_by_client_id(client_id)
        return result.connections