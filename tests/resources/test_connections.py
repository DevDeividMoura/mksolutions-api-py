import os

from mksolutions import MKSolutions
from mksolutions._exceptions import *

BASE_URL = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010/")
API_KEY = "test_api_key"

class TestConnections:
    client = MKSolutions(base_url= BASE_URL, api_key= API_KEY)
                         
    def test_find_by_clinet_id(self, client: MKSolutions):
        result = client.connections.find_by_client_id(123456)

        assert len(result.connections) == 2


    def test_find_by_client_doc(self, client: MKSolutions):
        result = client.connections.find_by_client_doc("123456789")

        assert len(result) == 6
