import os
import logging
import pytest
from mksolutions._client import MKSolutions
from mksolutions._exceptions import *

BASE_URL = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010/mk/")

# Configuração do logger para capturar logs em um arquivo
log_file_path = "test_logs.log"
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', handlers=[logging.FileHandler(log_file_path), logging.StreamHandler()])


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

def test_get_by_doc_with_invalid_token(caplog):
    mks = MKSolutions(
        base_url=BASE_URL,
        api_key="EXPIRED_API_KEY",
        custom_headers={"prefer": "example=invalid_token"}
    )

    with pytest.raises(TokenInvalidError):
        with caplog.at_level(logging.DEBUG):
            mks.clients.get_by_doc("12345678901")

def test_get_by_doc_with_invalid_document(caplog):
    mks = MKSolutions(
        base_url=BASE_URL,
        api_key="TEST_API_KEY",
        custom_headers={"prefer": "example=invalid_document"}
    )

    with pytest.raises(InvalidDocumentError):
        with caplog.at_level(logging.DEBUG):
            mks.clients.get_by_doc("Invalid_document")

def test_get_by_doc_not_found(caplog):
    mks = MKSolutions(
        base_url=BASE_URL,
        api_key="TEST_API_KEY",
        custom_headers={"prefer": "example=document_not_found"}
    )

    with pytest.raises(DocumentNotFoundError):
        with caplog.at_level(logging.DEBUG):
            mks.clients.get_by_doc("12345678901")

def test_get_by_doc_with_expired_token(caplog):
    mks = MKSolutions(
        base_url=BASE_URL,
        api_key="EXPIRED_API_KEY",
        custom_headers={"prefer": "example=expired_token"}
    )

    with pytest.raises(TokenExpiredError):
        with caplog.at_level(logging.DEBUG):
            mks.clients.get_by_doc("12345678901")

def test_get_by_doc_with_token_not_found(caplog):
    mks = MKSolutions(
        base_url=BASE_URL,
        api_key="EXPIRED_API_KEY",
        custom_headers={"prefer": "example=token_not_found"}
    )

    with pytest.raises(TokenNotFoundError):
        with caplog.at_level(logging.DEBUG):
            mks.clients.get_by_doc("12345678901")