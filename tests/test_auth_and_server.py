import os
import pytest
from unittest.mock import Mock, patch
from agent_utilities.core.exceptions import AuthError
from listmonk_api.auth import get_client
from listmonk_api.agent_server import agent_server

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


# ==============================================================================
# Agent Server Launcher CLI Tests
# ==============================================================================


@patch("agent_utilities.initialize_workspace")
@patch("agent_utilities.load_identity")
@patch("agent_utilities.create_agent_parser")
@patch("agent_utilities.create_agent_server")
def test_agent_server_cli(
    mock_create_server, mock_create_parser, mock_load_identity, mock_init_workspace
):
    # Set up mock parser arguments
    mock_args = Mock()
    mock_args.mcp_url = "http://mcp:8000"
    mock_args.mcp_config = "mcp_config.json"
    mock_args.host = "127.0.0.1"
    mock_args.port = 8500
    mock_args.provider = "openai"
    mock_args.model_id = "gpt-4o"
    mock_args.base_url = "http://api.openai.com"
    mock_args.api_key = "op-key"
    mock_args.custom_skills_directory = "/skills"
    mock_args.web = True
    mock_args.otel = False
    mock_args.otel_endpoint = None
    mock_args.otel_headers = None
    mock_args.otel_public_key = None
    mock_args.otel_secret_key = None
    mock_args.otel_protocol = None
    mock_args.debug = True

    mock_parser = Mock()
    mock_parser.parse_args.return_value = mock_args
    mock_create_parser.return_value = mock_parser

    # Set up identity metadata
    mock_load_identity.return_value = {
        "name": "Listmonk Agent",
        "description": "AI manager for listmonk",
        "content": "You are a Listmonk manager AI helper.",
    }

    # Execute server launcher
    agent_server()

    # Verify calls
    mock_init_workspace.assert_called_once()
    mock_load_identity.assert_called_once()
    mock_create_server.assert_called_once_with(
        mcp_url="http://mcp:8000",
        mcp_config="mcp_config.json",
        host="127.0.0.1",
        port=8500,
        provider="openai",
        model_id="gpt-4o",
        router_model="gpt-4o",
        agent_model="gpt-4o",
        base_url="http://api.openai.com",
        api_key="op-key",
        custom_skills_directory="/skills",
        enable_web_ui=True,
        enable_otel=False,
        otel_endpoint=None,
        otel_headers=None,
        otel_public_key=None,
        otel_secret_key=None,
        otel_protocol=None,
        debug=True,
    )
