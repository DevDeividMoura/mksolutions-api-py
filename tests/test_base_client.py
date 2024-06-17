import pytest
from httpx import URL, Timeout
from mksolutions._base_client import BaseClient
from mksolutions._constants import DEFAULT_TIMEOUT
from mksolutions.__version__ import __version__


@pytest.fixture
def base_client():
    return BaseClient(
        version=__version__,
        base_url="http://example.com/api",
        timeout=DEFAULT_TIMEOUT
    )


def test_enforce_trailing_slash(base_client):
    url = URL("http://example.com/api")
    result = base_client._enforce_trailing_slash(url)
    assert str(result) == "http://example.com/api/"

    url_with_slash = URL("http://example.com/api/")
    result_with_slash = base_client._enforce_trailing_slash(url_with_slash)
    assert str(result_with_slash) == "http://example.com/api/"


def test_prepare_url(base_client):
    relative_url = "endpoint"
    full_url = base_client._prepare_url(relative_url)
    assert str(full_url) == "http://example.com/api/endpoint"

    absolute_url = "http://other.com/endpoint"
    full_absolute_url = base_client._prepare_url(absolute_url)
    assert str(full_absolute_url) == "http://other.com/endpoint"


def test_base_url_property(base_client):
    assert str(base_client.base_url) == "http://example.com/api/"

    new_base_url = "http://newexample.com/api"
    base_client.base_url = new_base_url
    assert str(base_client.base_url) == "http://newexample.com/api/"


def test_timeout_property(base_client):
    assert base_client.timeout == DEFAULT_TIMEOUT

    new_timeout = Timeout(10.0)
    base_client.timeout = new_timeout
    assert base_client.timeout == new_timeout


def test_client_initialization():
    client = BaseClient(
        version="v1",
        base_url="http://example.com/api/",
        timeout=10.0
    )
    assert client._version == "v1"
    assert str(client.base_url) == "http://example.com/api/"
    assert client.timeout == 10.0
