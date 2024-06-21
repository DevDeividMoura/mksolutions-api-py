import logging
from typing import List, Optional

from .._resource import SyncAPIResource
from ..types.clients import ClientByDocResponse
from ..types.connections import Connection

log = logging.getLogger(__name__)

class Clients(SyncAPIResource):

    def get_by_doc(self, doc: str, include_conn: bool = False) -> List[Optional[ClientByDocResponse]]:
        """
        Get a client by document number.

        Arguments:
            doc: The document number to search for.

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

        first_client = ClientByDocResponse.from_dict(data)
        all_clients = [first_client]
        if "Outros" in data:
            for other in data["Outros"]:
                all_clients.append(ClientByDocResponse.from_dict(other))

        if include_conn:
            for client in all_clients:
                client.connections = self.__get_connections(client.id)

        return all_clients
    
    def __get_connections(self, client_id: int) -> List[Optional[Connection]]:
        result = self._client.connections.get_by_client_id(client_id)
        return result.connections