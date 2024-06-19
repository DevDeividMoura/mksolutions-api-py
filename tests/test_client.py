import os
import logging
import pytest
from unittest.mock import patch, MagicMock
from mksolutions._client import OpenAI
from mksolutions._exceptions import *

BASE_URL = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010") + "/"

# Configuração do logger para capturar logs em um arquivo
log_file_path = "test_logs.log"
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', handlers=[logging.FileHandler(log_file_path), logging.StreamHandler()])


def test_initialization_with_env_vars(monkeypatch):
    monkeypatch.setenv("MKS_BASE_URL", BASE_URL)
    monkeypatch.setenv("MKS_API_KEY", "test_api_key")

    client = OpenAI()

    assert client.base_url == BASE_URL
    assert client.api_key == "test_api_key"

def test_initialization_with_parameters():
    client = OpenAI(
        base_url=BASE_URL,
        api_key="test_api_key"
    )

    assert client.base_url == BASE_URL
    assert client.api_key == "test_api_key"

def test_missing_base_url():
    with pytest.raises(MissingBaseUrlError):
        OpenAI(api_key="test_api_key")


def test_missing_general_auths_params():
    with pytest.raises(MissingGeneralAuthParametersError):
        OpenAI(
            base_url=BASE_URL,
            auth_type="general"
        )

def test_missing_specific_auths_params():

    with pytest.raises(MissingSpecificAuthParametersError):
        OpenAI(
            base_url=BASE_URL,
            auth_type="specific" 
        )

def test_authenticate_on_initialization_with_missing_api_key_general(caplog):
    mks = OpenAI(
        base_url=BASE_URL,
        token="test_token",
        ws_password="test_ws_password",
        service_id=9999,
        auth_type="general"
    )

    assert mks.api_key == "test_token_general_autenticacao"

def test_authenticate_on_initialization_with_missing_api_key_specific(caplog):
    with caplog.at_level(logging.DEBUG):
        mks = OpenAI(
            base_url=BASE_URL,
            username="test_user",
            password="test_password",
            auth_type="specific"
        )

    assert mks.api_key is not "test_token_specific_autenticacao"


def test_invalid_auth_type():
    with pytest.raises(InvalidAuthTypeError):
        OpenAI(
            base_url=BASE_URL,
            auth_type="invalid"
        )


