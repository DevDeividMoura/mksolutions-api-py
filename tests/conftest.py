import os
import pytest
import httpx
from unittest.mock import MagicMock
from mksolutions._base_client import BaseClient, SyncAPIClient
from mksolutions._client import OpenAI
from mksolutions._constants import DEFAULT_TIMEOUT
from mksolutions.__version__ import __version__

BASE_URL = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")

# Subclasse de teste que implementa o método abstrato
# Subclasse de teste que implementa o método abstrato
class TestSyncAPIClient(SyncAPIClient):
    def _make_status_error(self, err_msg: str, *, body: object, response: httpx.Response):
        return httpx.HTTPStatusError(message=err_msg, request=response.request, response=response)


@pytest.fixture
def base_client():
    return BaseClient(
        version=__version__,
        base_url=BASE_URL,
        timeout=DEFAULT_TIMEOUT
    )

@pytest.fixture
def sync_client():
    return TestSyncAPIClient(
        version=__version__,
        base_url=BASE_URL,
        timeout=DEFAULT_TIMEOUT
    )

# To test the Auths class, we need a mock client
@pytest.fixture
def mock_client():
    client = MagicMock()
    client.base_url = BASE_URL
    client.api_key = None
    client.username = "test_username"
    client.password = "test_password"
    client.token = "test_token"
    client.ws_password = "test_ws_password"
    client.service_id = 1
    client.auth_type = "general"
    return client

# for the OpenAI client test
@pytest.fixture
def client():
    return OpenAI(
        base_url=BASE_URL,
        api_key="test_api_key"
    )