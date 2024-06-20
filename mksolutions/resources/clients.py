import logging
from typing import List, Optional

from .._resource import SyncAPIResource

from .._types import ClientByDoc

log = logging.getLogger(__name__)

class Clients(SyncAPIResource):

    def get_by_doc(self, doc: str) -> List[Optional[ClientByDoc]]:
        """
        Get a client by document number.

        Arguments:
            doc: The document number to search for.

        Returns:
            A list of clients that match the provided document number.
        """
        response = self._get(
            "/WSMKConsultaDoc.rule", 
            options={
                "sys": "MK0",
                "token": self._client.api_key,
                "doc": doc
                }
        )

        data = response.json()

        first_client = ClientByDoc.from_dict(data)
        all_clients = [first_client]
        if "Outros" in data:
            for other in data["Outros"]:
                all_clients.append(ClientByDoc.from_dict(other))
        return all_clients
