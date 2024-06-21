import os
import pytest
from mksolutions import MKSolutions
from mksolutions._exceptions import *

BASE_URL = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010/")

def test_initialization_with_env_vars(monkeypatch):
    monkeypatch.setenv("MKS_BASE_URL", BASE_URL)
    monkeypatch.setenv("MKS_API_KEY", "test_api_key")

    client = MKSolutions()

    assert client.base_url == BASE_URL
    assert client.api_key == "test_api_key"

def test_initialization_with_parameters():
    client = MKSolutions(
        base_url=BASE_URL,
        api_key="test_api_key"
    )

    assert client.base_url == BASE_URL
    assert client.api_key == "test_api_key"

def test_missing_base_url():
    with pytest.raises(MissingBaseUrlError):
        MKSolutions(api_key="test_api_key")


def test_missing_general_auths_params():
    with pytest.raises(MissingGeneralAuthParametersError):
        MKSolutions(
            base_url=BASE_URL,
            auth_type="general"
        )

def test_missing_specific_auths_params():

    with pytest.raises(MissingSpecificAuthParametersError):
        MKSolutions(
            base_url=BASE_URL,
            auth_type="specific" 
        )

def test_authenticate_on_initialization_with_missing_api_key_general():
    mks = MKSolutions(
        base_url=BASE_URL,
        token="test_token",
        ws_password="test_ws_password",
        service_id=9999,
        auth_type="general"
    )

    assert mks.api_key == "test_token_general_authentication"

def test_authenticate_on_initialization_with_missing_api_key_specific():
    mks = MKSolutions(
        base_url=BASE_URL,
        username="test_user",
        password="test_password",
        auth_type="specific"
    )

    assert mks.api_key == "test_token_specific_authentication"


def test_invalid_auth_type():
    with pytest.raises(InvalidAuthTypeError):
        MKSolutions(
            base_url=BASE_URL,
            auth_type="invalid"
        )


