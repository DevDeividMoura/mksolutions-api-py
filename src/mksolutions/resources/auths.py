from __future__ import annotations

from .._resource import SyncAPIResource
from ..types.auths import AuthGeneralResponse, AuthSpecificResponse


class Auths(SyncAPIResource):
    def authenticate_general(self) -> str:
        """
        Authenticate the client using the provided general service credentials.
        """
        response = self._get(
            "/mk/WSAutenticacao.rule",
            params={
                "sys": "MK0",
                "token": self._client.user_token,
                "password": self._client.ws_password,
                "cd_servico": self._client.service_id,
            },
        )
        auth_response = AuthGeneralResponse(**response.json())
        return auth_response.token

    def authenticate_specific(self) -> str:
        """
        Authenticate the client using the provided specific service credentials.
        """
        response = self._get(
            "/mk/WSAutenticacaoOperador.rule",
            params={
                "sys": "MK0",
                "username": self._client.username,
                "password": self._client.password,
            },
        )
        auth_response = AuthSpecificResponse(**response.json())
        return auth_response.token
