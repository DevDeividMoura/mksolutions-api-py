from __future__ import annotations


import os
import logging
from typing import Iterator

import pytest

from mksolutions import MKSolutions

pytest.register_assert_rewrite("tests.utils")

logging.getLogger("mksolutions").setLevel(logging.DEBUG)

BASE_URL = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010/")
API_KEY = "test_api_key"

@pytest.fixture(scope="session")
def client() -> Iterator[MKSolutions]:
    with MKSolutions(base_url= BASE_URL, api_key= API_KEY) as client:
        yield client