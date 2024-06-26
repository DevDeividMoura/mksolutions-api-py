import os
import json
import logging

import pytest

from mksolutions import MKSolutions
from mksolutions._exceptions import *
from mksolutions.types.clients import ClientByDocResponse

BASE_URL = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010/")
API_KEY = "test_api_key"

log = logging.getLogger(__name__)


class TestClients:
    client = MKSolutions(base_url= BASE_URL, api_key= API_KEY)

    def test_find_by_doc(self):
        mks = MKSolutions(base_url=BASE_URL,api_key=API_KEY)

        clients = mks.clients.find_by_doc("12345678901")

        assert isinstance(clients, ClientByDocResponse)

    def test_find_by_doc_output_list(self):
        mks = MKSolutions(base_url=BASE_URL,api_key=API_KEY)

        clients = mks.clients.find_by_doc("12345678901", output="list")

        assert len(clients) == 3


    def test_find_by_doc_with_invalid_token(self):
        mks = MKSolutions(base_url=BASE_URL, api_key="EXPIRED_API_KEY", custom_headers={"prefer": "example=invalid_token"})

        with pytest.raises(TokenInvalidError):
            mks.clients.find_by_doc("12345678901")


    def test_find_by_doc_with_invalid_document(self):
        mks = MKSolutions(base_url=BASE_URL, api_key="TEST_API_KEY", custom_headers={"prefer": "example=invalid_document"})

        with pytest.raises(InvalidFormatError):
            mks.clients.find_by_doc("Invalid_format_document")


    def test_find_by_doc_not_found(self):
        mks = MKSolutions(
            base_url=BASE_URL, api_key="TEST_API_KEY", custom_headers={"prefer": "example=document_not_found"}
        )

        with pytest.raises(ResultNotFoundError):
            mks.clients.find_by_doc("12345678901")


    def test_find_by_doc_with_expired_token(self):
        mks = MKSolutions(base_url=BASE_URL, api_key="EXPIRED_API_KEY", custom_headers={"prefer": "example=expired_token"})

        with pytest.raises(TokenExpiredError):
            mks.clients.find_by_doc("12345678901")


    def test_find_by_doc_with_token_not_found(self):
        mks = MKSolutions(
            base_url=BASE_URL, api_key="EXPIRED_API_KEY", custom_headers={"prefer": "example=token_not_found"}
        )

        with pytest.raises(TokenNotFoundError):
            mks.clients.find_by_doc("12345678901")
