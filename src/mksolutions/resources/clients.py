import logging
from .._resource import SyncAPIResource
from ..types.clients import ClientByDocResponse

log = logging.getLogger(__name__)

class Clients(SyncAPIResource):
    def find_by_doc(self, doc: str) -> ClientByDocResponse:
        """
        Find a client by document number.

        Arguments:
            doc: The document number to search for.

        Returns:
            A ClientByDocResponse object that matches the provided document number.
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

        return ClientByDocResponse(**data)
