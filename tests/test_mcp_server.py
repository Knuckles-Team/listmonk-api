from unittest.mock import patch
from listmonk_api.mcp_server import get_mcp_instance


@patch("listmonk_api.mcp_server.get_client")
@patch.dict(
    "os.environ", {"LISTMONK_URL": "http://localhost:9000", "LISTMONK_TOKEN": "secret"}
)
def test_get_mcp_instance(mock_get_client):
    mcp, args, middlewares, registered_tags, imported_tools = get_mcp_instance()
    assert mcp.name == "Listmonk"
