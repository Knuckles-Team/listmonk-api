import pytest
from unittest.mock import patch
from agent_connector_sdk.exceptions import AuthError
from listmonk_api.auth import get_client

# ==============================================================================
# Authentication & Singleton Client Tests
# ==============================================================================


@pytest.fixture(autouse=True)
def reset_auth_singleton():
    # Reset the cached singleton _client before and after each test
    import listmonk_api.auth

    listmonk_api.auth._client = None
    yield
    listmonk_api.auth._client = None


@patch.dict(
    "os.environ",
    {
        "LISTMONK_URL": "http://localhost:9000",
        "LISTMONK_TOKEN": "secret",
    },
)
def test_get_client_singleton():
    client1 = get_client()
    assert client1 is not None
    assert client1.base_url == "http://localhost:9000"

    # Verify it is a singleton cached instance
    client2 = get_client()
    assert client1 is client2


@patch("listmonk_api.auth.ListmonkAPI")
@patch.dict(
    "os.environ",
    {
        "LISTMONK_URL": "http://localhost:9000",
        "LISTMONK_TOKEN": "secret",
    },
)
def test_get_client_auth_error(mock_listmonk_api):
    # Mock AuthError
    mock_listmonk_api.side_effect = AuthError("Invalid username/password or token")

    with pytest.raises(RuntimeError, match="AUTHENTICATION ERROR"):
        get_client()
