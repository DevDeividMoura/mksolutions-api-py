class Auths:
    def __init__(self, client) -> None:
        self.client = client
        
    def authenticate_general(self) -> None:
        """
        Authenticate the client using the provided general service credentials.
        """
        response = self.client.get(
            "/WSAutenticacao.rule",
            options={
                "sys": "MK0",
                "token": self.client.token,
                "password": self.client.ws_password,
                "cd_servico": self.client.service_id,
            },
        )
        return response.json()["Token"]


    def authenticate_specific(self) -> None:
        """
        Authenticate the client using the provided specific service credentials.
        """
        response = self.client.get(
            "/WSAutenticacaoOperador.rule",
            options={
                "sys": "MK0",
                "username": self.client.username,
                "password": self.client.password,
            },
        )
        return response.json()["TokenAutenticacao"]