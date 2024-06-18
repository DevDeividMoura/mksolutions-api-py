import pytest
import httpx
from mksolutions._base_client import BaseClient, SyncAPIClient
from mksolutions._constants import DEFAULT_TIMEOUT
from mksolutions.__version__ import __version__

# Subclasse de teste que implementa o método abstrato
# Subclasse de teste que implementa o método abstrato
class TestSyncAPIClient(SyncAPIClient):
    def _make_status_error(self, err_msg: str, *, body: object, response: httpx.Response):
        return httpx.HTTPStatusError(message=err_msg, request=response.request, response=response)


@pytest.fixture
def base_client():
    return BaseClient(
        version=__version__,
        base_url="http://example.com/api",
        timeout=DEFAULT_TIMEOUT
    )

@pytest.fixture
def sync_client():
    return TestSyncAPIClient(
        version=__version__,
        base_url="http://example.com/api",
        timeout=DEFAULT_TIMEOUT
    )