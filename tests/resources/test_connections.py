import os
import pytest
from mksolutions import MKSolutions
from mksolutions._exceptions import *

BASE_URL = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010/")


def test_get_by_clinet_id(client):

    result = client.connections.get_by_client_id(123456)

    assert len(result.connections) == 2

