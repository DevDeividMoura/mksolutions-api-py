from .._resource import SyncAPIResource


class Auths(SyncAPIResource):
    def authenticate_general(self) -> None:
        """
        Authenticate the client using the provided general service credentials.
        """
        response = self._get(
            "/mk/WSAutenticacao.rule",
            options={
                "sys": "MK0",
                "token": self._client.user_token,
                "password": self._client.ws_password,
                "cd_servico": self._client.service_id,
            },
        )
        return response.json()["Token"]

    def authenticate_specific(self) -> None:
        """
        Authenticate the client using the provided specific service credentials.
        """
        response = self._get(
            "/mk/WSAutenticacaoOperador.rule",
            options={
                "sys": "MK0",
                "username": self._client.username,
                "password": self._client.password,
            },
        )
        return response.json()["TokenAutenticacao"]
