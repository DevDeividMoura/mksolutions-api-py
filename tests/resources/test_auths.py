import pytest
from unittest.mock import MagicMock
from mksolutions.resources.auths import Auths
from mksolutions._exceptions import *

def test_authenticate_general(mock_client):
    auths = Auths(mock_client)
    mock_response = MagicMock()
    mock_response.json.return_value = {"Token": "new_api_key"}

    mock_client.get.return_value = mock_response

    api_key = auths.authenticate_general()

    assert api_key == "new_api_key"

def test_authenticate_specific(mock_client):
    mock_client.auth_type = "specific"
    auths = Auths(mock_client)
    mock_response = MagicMock()
    mock_response.json.return_value = {"TokenAutenticacao": "new_api_key"}

    mock_client.get.return_value = mock_response

    api_key = auths.authenticate_specific()

    assert api_key == "new_api_key"

def test_authenticate_general_missing_token(mock_client):
    auths = Auths(mock_client)
    mock_response = MagicMock()
    mock_response.json.return_value = {}

    mock_client.get.return_value = mock_response

    with pytest.raises(KeyError):
        auths.authenticate_general()

def test_authenticate_specific_missing_token(mock_client):
    auths = Auths(mock_client)
    mock_response = MagicMock()
    mock_response.json.return_value = {}

    mock_client.get.return_value = mock_response

    with pytest.raises(KeyError):
        auths.authenticate_specific()