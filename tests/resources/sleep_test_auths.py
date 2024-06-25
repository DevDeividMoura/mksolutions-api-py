from unittest.mock import MagicMock

import pytest

from mksolutions._exceptions import *
from mksolutions.resources.auths import Auths



# def test_authenticate_on_initialization_with_missing_api_key_general():
#     mks = MKSolutions(
#         base_url=BASE_URL,
#         user_token="test_user_token",
#         ws_password="test_ws_password",
#         service_id=9999,
#         auth_type="general",
#     )

#     assert mks.api_key == "test_token_general_authentication"


# def test_authenticate_on_initialization_with_missing_api_key_specific():
#     mks = MKSolutions(base_url=BASE_URL, username="test_user", password="test_password", auth_type="specific")

#     assert mks.api_key == "test_token_specific_authentication"

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
