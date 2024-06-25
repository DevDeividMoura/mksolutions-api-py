from __future__ import annotations

import os

import httpx
import pytest
from respx import MockRouter

from mksolutions import MKSolutions
from mksolutions._models import FinalRequestOptions
from mksolutions._exceptions import (
    MissingBaseUrlError, 
    InvalidAuthTypeError, 
    MissingGeneralAuthParametersError, 
    MissingSpecificAuthParametersError
)
from mksolutions._base_client import DEFAULT_TIMEOUT, HTTPX_DEFAULT_TIMEOUT

from .utils import update_env

BASE_URL = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010/")
API_KEY = "test_api_key"

class TestMKSolutions:
    client = MKSolutions(base_url= BASE_URL, api_key= API_KEY)
    
    @pytest.mark.respx(base_url=BASE_URL)
    def test_raw_response(self, respx_mock: MockRouter) -> None:
        respx_mock.get("/test").mock(return_value=httpx.Response(200, json={"success": "true"}))

        response = self.client.get("/test")
        assert response.status_code == 200
        assert isinstance(response, httpx.Response)
        assert response.json() == {"success": "true"}

    def test_request_timeout(self) -> None:
        request = self.client._build_request(FinalRequestOptions(method="get", url="/test"))
        timeout = httpx.Timeout(**request.extensions["timeout"])  # type: ignore
        assert timeout == DEFAULT_TIMEOUT

        request = self.client._build_request(
            FinalRequestOptions(method="get", url="/test", timeout=httpx.Timeout(100.0))
        )
        timeout = httpx.Timeout(**request.extensions["timeout"])  # type: ignore
        assert timeout == httpx.Timeout(100.0)

    def test_client_timeout_option(self) -> None:
        client = MKSolutions(base_url= BASE_URL, api_key= API_KEY,timeout=httpx.Timeout(0))

        request = client._build_request(FinalRequestOptions(method="get", url="/test"))
        timeout = httpx.Timeout(**request.extensions["timeout"])  # type: ignore
        assert timeout == httpx.Timeout(0)

    def test_http_client_timeout_option(self) -> None:
        # custom timeout given to the httpx client should be used
        with httpx.Client(timeout=None) as http_client:
            client = MKSolutions(base_url=BASE_URL, api_key=API_KEY, http_client=http_client)

            request = client._build_request(FinalRequestOptions(method="get", url="/test"))
            timeout = httpx.Timeout(**request.extensions["timeout"])  # type: ignore
            assert timeout == httpx.Timeout(None)

        # no timeout given to the httpx client should not use the httpx default
        with httpx.Client() as http_client:
            client = MKSolutions(base_url=BASE_URL, api_key=API_KEY, http_client=http_client)

            request = client._build_request(FinalRequestOptions(method="get", url="/test"))
            timeout = httpx.Timeout(**request.extensions["timeout"])  # type: ignore
            assert timeout == DEFAULT_TIMEOUT

        # explicitly passing the default timeout currently results in it being ignored
        with httpx.Client(timeout=HTTPX_DEFAULT_TIMEOUT) as http_client:
            client = MKSolutions(base_url=BASE_URL, api_key=API_KEY, http_client=http_client)

            request = client._build_request(FinalRequestOptions(method="get", url="/test"))
            timeout = httpx.Timeout(**request.extensions["timeout"])  # type: ignore
            assert timeout == DEFAULT_TIMEOUT  # our default

    def test_base_url_setter(self) -> None:
        client = MKSolutions(base_url= "https://example.com/from_init", api_key=API_KEY)
        assert client.base_url == "https://example.com/from_init/"

        client.base_url = "https://example.com/from_setter"  # type: ignore[assignment]

        assert client.base_url == "https://example.com/from_setter/"

    def test_base_url_env(self) -> None:
        with update_env(MKS_BASE_URL="http://localhost:5000/from/env"):
            client = MKSolutions(api_key=API_KEY)
            assert client.base_url == "http://localhost:5000/from/env/"

    @pytest.mark.parametrize(
        "client",
        [
            MKSolutions(base_url="http://localhost:5000/custom/path/", api_key=API_KEY),
            MKSolutions(
                base_url="http://localhost:5000/custom/path/",
                api_key=API_KEY,
                http_client=httpx.Client(),
            ),
        ],
        ids=["standard", "custom http client"],
    )
    def test_base_url_trailing_slash(self, client: MKSolutions) -> None:
        request = client._build_request(
            FinalRequestOptions(
                method="post",
                url="/success",
                json_data={"success": "true"},
            ),
        )
        assert request.url == "http://localhost:5000/custom/path/success"

    @pytest.mark.parametrize(
        "client",
        [
            MKSolutions(base_url="http://localhost:5000/custom/path/", api_key=API_KEY),
            MKSolutions(
                base_url="http://localhost:5000/custom/path/",
                api_key=API_KEY,
                http_client=httpx.Client(),
            ),
        ],
        ids=["standard", "custom http client"],
    )
    def test_base_url_no_trailing_slash(self, client: MKSolutions) -> None:
        request = client._build_request(
            FinalRequestOptions(
                method="post",
                url="/success",
                json_data={"success": "true"},
            ),
        )
        assert request.url == "http://localhost:5000/custom/path/success"

    @pytest.mark.parametrize(
        "client",
        [
            MKSolutions(base_url="http://localhost:5000/custom/path/", api_key=API_KEY),
            MKSolutions(
                base_url="http://localhost:5000/custom/path/",
                api_key=API_KEY,
                http_client=httpx.Client(),
            ),
        ],
        ids=["standard", "custom http client"],
    )
    def test_absolute_request_url(self, client: MKSolutions) -> None:
        request = client._build_request(
            FinalRequestOptions(
                method="post",
                url="https://myapi.com/success",
                json_data={"success": "true"},
            ),
        )
        assert request.url == "https://myapi.com/success"

    def test_missing_params(self):
        # Missing base_url
        with pytest.raises(MissingBaseUrlError):
            MKSolutions(api_key="test_api_key")

        # Missing auths params to general autentication
        with pytest.raises(MissingGeneralAuthParametersError):
            MKSolutions(base_url=BASE_URL, auth_type="general")

        # Missing auths params to specific autentication
        with pytest.raises(MissingSpecificAuthParametersError):
            MKSolutions(base_url=BASE_URL, auth_type="specific")

        with pytest.raises(InvalidAuthTypeError):
            MKSolutions(base_url=BASE_URL, auth_type="invalid")