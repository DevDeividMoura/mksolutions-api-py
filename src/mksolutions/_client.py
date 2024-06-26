import os
from typing import Union, Optional
from typing_extensions import override

import httpx

from . import resources
from ._types import (
    NOT_GIVEN,
    Timeout,
    NotGiven,
)
from .__version__ import __version__
from ._exceptions import *
from ._base_client import SyncAPIClient


class MKSolutions(SyncAPIClient):
    clients: resources.Clients
    contracts: resources.Contracts
    connections: resources.Connections

    # client options
    api_key: str
    username: str
    password: str
    token: str
    ws_password: str
    service_id: str
    auth_type: str
    """
    Synchronous MKSolutions client.

    This client handles API requests to MKSolutions, managing authentication and endpoint configuration.
    """

    def __init__(
        self,
        *,
        base_url: Optional[str | httpx.URL] = None,
        timeout: Union[float, Timeout, None, NotGiven] = NOT_GIVEN,
        api_key: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        user_token: Optional[str] = None,
        ws_password: Optional[str] = None,
        service_id: Optional[int] = 9999,
        auth_type: Optional[str] = "general",
        custom_headers: Optional[dict[str, str]] = None,
        # Configure a custom httpx client.
        # We provide a `DefaultHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#client) for more details.
        http_client: httpx.Client | None = None,
    ) -> None:
        """
        Initialize a new synchronous MKSolutions client instance.

        Arguments can be automatically inferred from environment variables if not provided:
        - `base_url` from `MKS_BASE_URL`
        - `api_key` from `MKS_API_KEY`
        - `username` from `MKS_USERNAME`
        - `password` from `MKS_PASSWORD`
        - `user_token` from `MKS_USER_TOKEN`
        - `ws_password` from `MKS_WS_PASSWORD`

        :param base_url: The base URL for the API endpoints.
        :param timeout: The timeout for the HTTP requests.
        :param api_key: The API key for authentication,
        :param username: The username for specific service authentication.
        :param password: The password for specific service authentication.
        :param user_token: The eser token for general service authentication.
        :param ws_password: The password for general service authentication.
        :param service_id: The service ID for general service authentication.
        :param auth_type: The type of authentication to be used if the api_key is not passed.
        :param http_client: A custom httpx.Client instance.
        """
        self.base_url = base_url or os.environ.get("MKS_BASE_URL")
        if not self.base_url:
            raise MissingBaseUrlError(
                "The base_url client option must be set either by passing base_url to the client or by setting the MKS_BASE_URL environment variable"
            )

        self.api_key = api_key or os.environ.get("MKS_API_KEY")
        self.username = username or os.environ.get("MKS_USERNAME")
        self.password = password or os.environ.get("MKS_PASSWORD")
        self.user_token = user_token or os.environ.get("MKS_USER_TOKEN")
        self.ws_password = ws_password or os.environ.get("MKS_WS_PASSWORD")
        self.service_id = service_id or os.environ.get("MKS_SERVICE_ID")
        self.auth_type = auth_type

        super().__init__(
            version=__version__,
            base_url=self.base_url,
            timeout=timeout,
            http_client=http_client,
            custom_headers=custom_headers,
        )

        self.auths = resources.Auths(self)

        if not self.api_key:
            if self.auth_type == "general":
                if self.user_token and self.ws_password and self.service_id:
                    self.api_key = self.auths.authenticate_general()
                else:
                    raise MissingGeneralAuthParametersError(
                        "For general authentication, user_token, ws_password, and service_id must be provided."
                    )

            elif self.auth_type == "specific":
                if self.username and self.password:
                    self.api_key = self.auths.authenticate_specific()
                else:
                    raise MissingSpecificAuthParametersError(
                        "For specific authentication, username and password must be provided."
                    )
            else:
                raise InvalidAuthTypeError("Invalid auth_type specified.")

        self.clients = resources.Clients(self)
        self.contracts = resources.Contracts(self)
        self.connections = resources.Connections(self)

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        """
        Create a specific API error based on the HTTP response.

        :param err_msg: The error message.
        :param body: The response body.
        :param response: The HTTP response.
        :return: An APIStatusError instance.
        """
        if isinstance(body, dict) and body.get("status") == "ERRO":
            error_code = body.get("Num. ERRO")
            message = body.get("Mensagem", err_msg)

            error_map = {
                "001": TokenInvalidError,
                "002": InvalidFormatError,
                "003": ResultNotFoundError,
                "999": TokenExpiredError if "expirado" in message else TokenNotFoundError,
            }

            if error_code in error_map:
                return error_map[error_code](message, response.request, body=body)

        if response.status_code >= 500:
            return InternalServerError(err_msg, response=response, body=body)

        return APIStatusError(err_msg, response=response, body=body)
