import pytest
import httpx
from httpx import URL, Timeout, Response
from mksolutions._base_client import BaseClient, SyncAPIClient
from mksolutions._constants import DEFAULT_TIMEOUT
from mksolutions.__version__ import __version__

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

def test_sync_client_initialization(sync_client):
    assert sync_client._version == __version__
    assert str(sync_client.base_url) == "http://example.com/api/"
    assert sync_client.timeout == DEFAULT_TIMEOUT

def test_sync_client_get(sync_client, mocker):
    response_mock = mocker.Mock(spec=Response)
    response_mock.status_code = 200
    response_mock.json.return_value = {"status": "OK"}
    response_mock.headers = {'Content-Type': 'text/html'}
    mocker.patch.object(sync_client._client, 'send', return_value=response_mock)

    response = sync_client.get("test_endpoint")
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}

def test_sync_client_get_with_error_500(sync_client, mocker):
    response_mock = mocker.Mock(spec=Response)
    response_mock.status_code = 500
    response_mock.is_closed = True
    response_mock.text = """
    <!doctype html>
    <html lang="pt">
    <head></head>
    <body>
    <p><b>Type</b> Exception Report</p>
    <p><b>Message</b> This is the error message received</p>
    </body></html>
    """
    response_mock.headers = {'Content-Type': 'text/html'}
    
    # Configurando a exceção raise_for_status para levantar HTTPStatusError
    mocker.patch.object(response_mock, 'raise_for_status', side_effect=httpx.HTTPStatusError(message="Error", request=httpx.Request(method='GET', url='http://example.com/api/test_endpoint'), response=response_mock))
    
    mocker.patch.object(sync_client._client, 'send', return_value=response_mock)

    with pytest.raises(httpx.HTTPStatusError, match="This is the error message received"):
        sync_client.get("test_endpoint")
