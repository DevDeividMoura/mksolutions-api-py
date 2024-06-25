import os

import pytest

from mksolutions import MKSolutions
from mksolutions._exceptions import *

BASE_URL = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010/")


def test_get_by_doc():
    mks = MKSolutions(
        base_url=BASE_URL,
        api_key="TEST_API_KEY",
    )

    clients = mks.clients.get_by_doc("12345678901")

    assert len(clients) == 3
    assert clients[0].name == "JOÃO SILVA"
    assert clients[1].name == "JOÃO SILVA 2"
    assert clients[2].name == "JOÃO SILVA 3"


def test_get_by_doc_with_connections():
    mks = MKSolutions(
        base_url=BASE_URL,
        api_key="TEST_API_KEY",
    )

    clients = mks.clients.get_by_doc("12345678901", include_conn=True)

    assert len(clients) == 3
    assert len(clients[0].connections) == 2


def test_get_by_doc_with_invalid_token():
    mks = MKSolutions(base_url=BASE_URL, api_key="EXPIRED_API_KEY", custom_headers={"prefer": "example=invalid_token"})

    with pytest.raises(TokenInvalidError):
        mks.clients.get_by_doc("12345678901")


def test_get_by_doc_with_invalid_document():
    mks = MKSolutions(base_url=BASE_URL, api_key="TEST_API_KEY", custom_headers={"prefer": "example=invalid_document"})

    with pytest.raises(InvalidFormatError):
        mks.clients.get_by_doc("Invalid_format_document")


def test_get_by_doc_not_found():
    mks = MKSolutions(
        base_url=BASE_URL, api_key="TEST_API_KEY", custom_headers={"prefer": "example=document_not_found"}
    )

    with pytest.raises(ResultNotFoundError):
        mks.clients.get_by_doc("12345678901")


def test_get_by_doc_with_expired_token():
    mks = MKSolutions(base_url=BASE_URL, api_key="EXPIRED_API_KEY", custom_headers={"prefer": "example=expired_token"})

    with pytest.raises(TokenExpiredError):
        mks.clients.get_by_doc("12345678901")


def test_get_by_doc_with_token_not_found():
    mks = MKSolutions(
        base_url=BASE_URL, api_key="EXPIRED_API_KEY", custom_headers={"prefer": "example=token_not_found"}
    )

    with pytest.raises(TokenNotFoundError):
        mks.clients.get_by_doc("12345678901")
