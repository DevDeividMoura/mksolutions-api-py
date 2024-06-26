import os

from mksolutions import MKSolutions

BASE_URL = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010/")
API_KEY = "test_api_key"

class TestAuths:
    client = MKSolutions(base_url= BASE_URL, api_key= API_KEY)

    def test_authenticate_on_initialization_with_missing_api_key_specific(self):
        mks = MKSolutions(base_url=BASE_URL, username="test_user", password="test_password", auth_type="specific")

        assert mks.api_key == "test_token_specific_authentication"

    def test_authenticate_on_initialization_with_missing_api_key_general(self):
        mks = MKSolutions(
            base_url=BASE_URL,
            user_token="test_user_token",
            ws_password="test_ws_password",
            service_id=9999,
            auth_type="general",
        )

        assert mks.api_key == "test_token_general_authentication"
