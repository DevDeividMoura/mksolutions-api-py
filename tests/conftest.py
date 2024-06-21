import os
import pytest
import httpx
import logging
from unittest.mock import MagicMock
from mksolutions._base_client import BaseClient, SyncAPIClient
from mksolutions import MKSolutions
from mksolutions import DEFAULT_TIMEOUT
from mksolutions import __version__

BASE_URL = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")

# Definir o caminho para o arquivo de log
log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'temp')
log_file_path = os.path.join(log_dir, 'test_logs.log')

# Criar a pasta 'temp' se ela não existir
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Configurar o logger
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file_path),
        logging.StreamHandler()
    ]
)

# Configurar o logger específico para a biblioteca 'mksolutions'
mksolutions_logger = logging.getLogger('mksolutions')
mksolutions_logger.setLevel(logging.DEBUG)

# Desabilitar o logging para outras bibliotecas, como httpx
logging.getLogger('httpx').setLevel(logging.WARNING)
logging.getLogger('httpcore').setLevel(logging.WARNING)

# Função para garantir que o logger seja fechado corretamente
@pytest.fixture(scope='session', autouse=True)
def close_loggers():
    yield
    logging.shutdown()


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
        base_url="http://exemple.com",
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

# for the MKSolutions client test
@pytest.fixture
def client():
    return MKSolutions(
        base_url=BASE_URL,
        api_key="test_api_key"
    )