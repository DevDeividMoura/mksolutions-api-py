from __future__ import annotations

import logging

from ..types import ClientByDoc, ClientByDocResponse
from .._resource import SyncAPIResource

log = logging.getLogger(__name__)

class Clients(SyncAPIResource):
    def find_by_doc(self, doc: str, output: str = "nested") -> ClientByDocResponse | list[ClientByDoc]:
        """
        Find a client by document number.

        Arguments:
            doc: The document number to search for.

        Returns:
            A ClientByDocResponse object that matches the provided document number.
        """
        response = self._get(
            "/mk/WSMKConsultaDoc.rule",
            params={
                "sys": "MK0", 
                "token": self._client.api_key, 
                "doc": doc
            }
        )

        data = response.json()


        if output == "list":
            clients = [ClientByDoc(**{k: v for k, v in data.items() if k not in ["Outros", "status"]})]
            clients.extend([ClientByDoc(**item) for item in data.get("Outros", [])])
            return clients
        else:
            return ClientByDocResponse(**data)
