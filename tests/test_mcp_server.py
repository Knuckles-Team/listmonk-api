import json
import pytest
from unittest.mock import Mock, patch, mock_open
from fastmcp import FastMCP
from listmonk_api.mcp_server import (
    get_mcp_instance,
    mcp_server,
    register_listmonk_subscribers_tools,
    register_listmonk_lists_tools,
    register_listmonk_imports_tools,
    register_listmonk_campaigns_tools,
    register_listmonk_media_tools,
    register_listmonk_templates_tools,
    register_listmonk_tx_tools,
)


@pytest.fixture
def mock_client():
    return Mock()


@pytest.fixture
def mock_ctx():
    return Mock()


def get_tool(mcp: FastMCP, name: str):
    for comp in mcp._local_provider._components.values():
        if comp.name == name:
            return comp
    raise ValueError(f"Tool {name} not found")


# ==============================================================================
# FastMCP Tools Routing Tests
# ==============================================================================


def test_listmonk_subscribers_tool(mock_client, mock_ctx):
    mcp = FastMCP("test")
    register_listmonk_subscribers_tools(mcp)
    tool = get_tool(mcp, "listmonk_subscribers")

    # Invalid JSON
    res = tool.fn(
        action="get_subscriber",
        params_json="{invalid}",
        client=mock_client,
        ctx=mock_ctx,
    )
    assert "error" in res
    assert "Invalid params_json" in res["error"]

    # get_subscribers
    mock_client.get_subscribers.return_value = [{"id": 1}]
    res = tool.fn(
        action="get_subscribers",
        params_json='{"per_page": 50}',
        client=mock_client,
        ctx=mock_ctx,
    )
    assert res == {"results": [{"id": 1}]}
    mock_client.get_subscribers.assert_called_with(per_page=50)

    # get_subscriber
    mock_client.get_subscriber.return_value = {"id": 1}
    res = tool.fn(
        action="get_subscriber",
        params_json='{"subscriber_id": 1}',
        client=mock_client,
        ctx=mock_ctx,
    )
    assert res == {"id": 1}
    mock_client.get_subscriber.assert_called_with(subscriber_id=1)

    # get_subscribers_from_list
    mock_client.get_subscribers_from_list.return_value = [{"id": 1}]
    res = tool.fn(
        action="get_subscribers_from_list",
        params_json='{"list_id": 2}',
        client=mock_client,
        ctx=mock_ctx,
    )
    assert res == [{"id": 1}]
    mock_client.get_subscribers_from_list.assert_called_with(list_id=2)

    # create_subscriber
    mock_client.create_subscriber.return_value = {"id": 10}
    res = tool.fn(
        action="create_subscriber",
        params_json='{"email": "a@b.com", "name": "A", "status": "enabled"}',
        client=mock_client,
        ctx=mock_ctx,
    )
    assert res == {"id": 10}
    mock_client.create_subscriber.assert_called_once()

    # Unknown action
    with pytest.raises(ValueError, match="Unknown action: invalid_action"):
        tool.fn(
            action="invalid_action", params_json="{}", client=mock_client, ctx=mock_ctx
        )


def test_listmonk_lists_tool(mock_client, mock_ctx):
    mcp = FastMCP("test")
    register_listmonk_lists_tools(mcp)
    tool = get_tool(mcp, "listmonk_lists")

    # Invalid JSON
    res = tool.fn(
        action="get_lists", params_json="{invalid}", client=mock_client, ctx=mock_ctx
    )
    assert "error" in res

    # get_lists
    mock_client.get_lists.return_value = [{"id": 1}]
    res = tool.fn(
        action="get_lists",
        params_json='{"per_page": 50}',
        client=mock_client,
        ctx=mock_ctx,
    )
    assert res == {"results": [{"id": 1}]}

    # get_list
    mock_client.get_list.return_value = {"id": 2}
    res = tool.fn(
        action="get_list",
        params_json='{"list_id": 2}',
        client=mock_client,
        ctx=mock_ctx,
    )
    assert res == {"id": 2}

    # create_list
    mock_client.create_list.return_value = {"id": 3}
    res = tool.fn(
        action="create_list",
        params_json='{"name": "List", "type": "public", "optin": "single"}',
        client=mock_client,
        ctx=mock_ctx,
    )
    assert res == {"id": 3}

    # edit_list
    mock_client.edit_list.return_value = {"id": 4}
    res = tool.fn(
        action="edit_list",
        params_json='{"list_id": 4, "data": {"name": "New"}}',
        client=mock_client,
        ctx=mock_ctx,
    )
    assert res == {"id": 4}

    # Unknown action
    with pytest.raises(ValueError, match="Unknown action"):
        tool.fn(
            action="invalid_action", params_json="{}", client=mock_client, ctx=mock_ctx
        )


def test_listmonk_imports_tool(mock_client, mock_ctx):
    mcp = FastMCP("test")
    register_listmonk_imports_tools(mcp)
    tool = get_tool(mcp, "listmonk_imports")

    # Invalid JSON
    res = tool.fn(
        action="get_subscriber_import_status",
        params_json="{invalid}",
        client=mock_client,
        ctx=mock_ctx,
    )
    assert "error" in res

    # get_subscriber_import_status
    mock_client.get_subscriber_import_status.return_value = {"status": "ok"}
    res = tool.fn(
        action="get_subscriber_import_status",
        params_json="{}",
        client=mock_client,
        ctx=mock_ctx,
    )
    assert res == {"status": "ok"}

    # get_subscriber_import_logs
    mock_client.get_subscriber_import_logs.return_value = ["log"]
    res = tool.fn(
        action="get_subscriber_import_logs",
        params_json="{}",
        client=mock_client,
        ctx=mock_ctx,
    )
    assert res == ["log"]

    # import_subscribers
    mock_client.import_subscribers.return_value = {"imported": True}
    res = tool.fn(
        action="import_subscribers",
        params_json='{"file": "base64", "mode": "subscribe", "lists": [1]}',
        client=mock_client,
        ctx=mock_ctx,
    )
    assert res == {"imported": True}

    # delete_subscriber_import
    mock_client.delete_subscriber_import.return_value = {"deleted": True}
    res = tool.fn(
        action="delete_subscriber_import",
        params_json="{}",
        client=mock_client,
        ctx=mock_ctx,
    )
    assert res == {"deleted": True}

    # Unknown action
    with pytest.raises(ValueError, match="Unknown action"):
        tool.fn(
            action="invalid_action", params_json="{}", client=mock_client, ctx=mock_ctx
        )


def test_listmonk_campaigns_tool(mock_client, mock_ctx):
    mcp = FastMCP("test")
    register_listmonk_campaigns_tools(mcp)
    tool = get_tool(mcp, "listmonk_campaigns")

    # Invalid JSON
    res = tool.fn(
        action="get_campaigns",
        params_json="{invalid}",
        client=mock_client,
        ctx=mock_ctx,
    )
    assert "error" in res

    # get_campaigns
    mock_client.get_campaigns.return_value = [{"id": 1}]
    res = tool.fn(
        action="get_campaigns", params_json="{}", client=mock_client, ctx=mock_ctx
    )
    assert res == {"results": [{"id": 1}]}

    # get_campaign
    mock_client.get_campaign.return_value = {"id": 1}
    res = tool.fn(
        action="get_campaign",
        params_json='{"campaign_id": 1}',
        client=mock_client,
        ctx=mock_ctx,
    )
    assert res == {"id": 1}

    # get_campaign_preview
    mock_client.get_campaign_preview.return_value = "preview"
    res = tool.fn(
        action="get_campaign_preview",
        params_json='{"campaign_id": 1}',
        client=mock_client,
        ctx=mock_ctx,
    )
    assert res == "preview"

    # get_campaign_stats
    mock_client.get_campaign_stats.return_value = {"clicks": 0}
    res = tool.fn(
        action="get_campaign_stats",
        params_json='{"campaign_id": 1}',
        client=mock_client,
        ctx=mock_ctx,
    )
    assert res == {"clicks": 0}

    # create_campaign
    mock_client.create_campaign.return_value = {"id": 2}
    res = tool.fn(
        action="create_campaign",
        params_json='{"name": "C", "subject": "S", "lists": [1], "from_email": "a@b.com", "send_type": "regular", "content_type": "plain", "body": "B"}',
        client=mock_client,
        ctx=mock_ctx,
    )
    assert res == {"id": 2}

    # set_campaign_status
    mock_client.set_campaign_status.return_value = {"success": True}
    res = tool.fn(
        action="set_campaign_status",
        params_json='{"campaign_id": 1, "data": {"status": "paused"}}',
        client=mock_client,
        ctx=mock_ctx,
    )
    assert res == {"success": True}

    # delete_campaign
    mock_client.delete_campaign.return_value = {"deleted": True}
    res = tool.fn(
        action="delete_campaign",
        params_json='{"campaign_id": 1}',
        client=mock_client,
        ctx=mock_ctx,
    )
    assert res == {"deleted": True}

    # Unknown action
    with pytest.raises(ValueError, match="Unknown action"):
        tool.fn(
            action="invalid_action", params_json="{}", client=mock_client, ctx=mock_ctx
        )


def test_listmonk_media_tool(mock_client, mock_ctx):
    mcp = FastMCP("test")
    register_listmonk_media_tools(mcp)
    tool = get_tool(mcp, "listmonk_media")

    # Invalid JSON
    res = tool.fn(
        action="get_media", params_json="{invalid}", client=mock_client, ctx=mock_ctx
    )
    assert "error" in res

    # get_media
    mock_client.get_media.return_value = {"id": 1}
    res = tool.fn(
        action="get_media",
        params_json='{"media_id": 1}',
        client=mock_client,
        ctx=mock_ctx,
    )
    assert res == {"id": 1}

    # upload_media
    mock_client.upload_media.return_value = {"uploaded": True}
    res = tool.fn(
        action="upload_media",
        params_json='{"file": "base64"}',
        client=mock_client,
        ctx=mock_ctx,
    )
    assert res == {"uploaded": True}

    # delete_media
    mock_client.delete_media.return_value = {"deleted": True}
    res = tool.fn(
        action="delete_media",
        params_json='{"media_id": 1}',
        client=mock_client,
        ctx=mock_ctx,
    )
    assert res == {"deleted": True}

    # Unknown action
    with pytest.raises(ValueError, match="Unknown action"):
        tool.fn(
            action="invalid_action", params_json="{}", client=mock_client, ctx=mock_ctx
        )


def test_listmonk_templates_tool(mock_client, mock_ctx):
    mcp = FastMCP("test")
    register_listmonk_templates_tools(mcp)
    tool = get_tool(mcp, "listmonk_templates")

    # Invalid JSON
    res = tool.fn(
        action="get_templates",
        params_json="{invalid}",
        client=mock_client,
        ctx=mock_ctx,
    )
    assert "error" in res

    # get_templates
    mock_client.get_templates.return_value = [{"id": 1}]
    res = tool.fn(
        action="get_templates", params_json="{}", client=mock_client, ctx=mock_ctx
    )
    assert res == {"results": [{"id": 1}]}

    # get_template
    mock_client.get_template.return_value = {"id": 1}
    res = tool.fn(
        action="get_template",
        params_json='{"template_id": 1}',
        client=mock_client,
        ctx=mock_ctx,
    )
    assert res == {"id": 1}

    # get_template_preview
    mock_client.get_template_preview.return_value = "preview"
    res = tool.fn(
        action="get_template_preview",
        params_json='{"template_id": 1}',
        client=mock_client,
        ctx=mock_ctx,
    )
    assert res == "preview"

    # set_default_template
    mock_client.set_default_template.return_value = {"success": True}
    res = tool.fn(
        action="set_default_template",
        params_json='{"template_id": 1}',
        client=mock_client,
        ctx=mock_ctx,
    )
    assert res == {"success": True}

    # delete_template
    mock_client.delete_template.return_value = {"deleted": True}
    res = tool.fn(
        action="delete_template",
        params_json='{"template_id": 1}',
        client=mock_client,
        ctx=mock_ctx,
    )
    assert res == {"deleted": True}

    # Unknown action
    with pytest.raises(ValueError, match="Unknown action"):
        tool.fn(
            action="invalid_action", params_json="{}", client=mock_client, ctx=mock_ctx
        )


def test_listmonk_tx_tool(mock_client, mock_ctx):
    mcp = FastMCP("test")
    register_listmonk_tx_tools(mcp)
    tool = get_tool(mcp, "listmonk_tx")

    # Invalid JSON
    res = tool.fn(
        action="transactional_message",
        params_json="{invalid}",
        client=mock_client,
        ctx=mock_ctx,
    )
    assert "error" in res

    # transactional_message
    mock_client.transactional_message.return_value = {"sent": True}
    res = tool.fn(
        action="transactional_message",
        params_json='{"template_id": 1, "subscriber_email": "a@b.com"}',
        client=mock_client,
        ctx=mock_ctx,
    )
    assert res == {"sent": True}

    # Unknown action
    with pytest.raises(ValueError, match="Unknown action"):
        tool.fn(
            action="invalid_action", params_json="{}", client=mock_client, ctx=mock_ctx
        )


# ==============================================================================
# Server Initialization & Launch Tests
# ==============================================================================


@patch("sys.argv", ["listmonk-mcp"])
@patch("listmonk_api.mcp_server.get_client")
@patch.dict(
    "os.environ",
    {
        "LISTMONK_URL": "http://localhost:9000",
        "LISTMONK_TOKEN": "secret",
        "LISTMONK_SUBSCRIBERSTOOL": "True",
        "LISTMONK_LISTSTOOL": "True",
        "LISTMONK_IMPORTSTOOL": "True",
        "LISTMONK_CAMPAIGNSTOOL": "True",
        "LISTMONK_MEDIATOOL": "True",
        "LISTMONK_TEMPLATESTOOL": "True",
        "LISTMONK_TXTOOL": "True",
    },
)
def test_get_mcp_instance_standard(mock_get_client):
    mcp, args, middlewares, registered_tags, imported_tools = get_mcp_instance()
    assert mcp.name == "Listmonk"
    # Ensure tools got registered
    assert get_tool(mcp, "listmonk_subscribers") is not None
    assert get_tool(mcp, "listmonk_lists") is not None


@patch("listmonk_api.mcp_server.get_client")
@patch("listmonk_api.mcp_server.config", {"enable_delegation": True})
@patch.dict(
    "os.environ",
    {
        "LISTMONK_URL": "http://localhost:9000",
        "LISTMONK_TOKEN": "secret",
    },
)
def test_get_mcp_instance_openapi_delegation_error(mock_get_client):
    # Mocking parser arguments to include an openapi_file path
    with patch("listmonk_api.mcp_server.create_mcp_server") as mock_create:
        mock_args = Mock()
        mock_args.openapi_file = "spec.json"
        mock_create.return_value = (mock_args, Mock(), [])

        with pytest.raises(
            ValueError, match="OpenAPI import not supported with delegation enabled"
        ):
            get_mcp_instance()


@patch("listmonk_api.mcp_server.get_client")
@patch("listmonk_api.mcp_server.config", {"enable_delegation": False})
@patch.dict(
    "os.environ",
    {
        "LISTMONK_URL": "http://localhost:9000",
        "LISTMONK_TOKEN": "secret",
    },
)
def test_get_mcp_instance_openapi_import_failure(mock_get_client):
    with (
        patch("listmonk_api.mcp_server.create_mcp_server") as mock_create,
        patch("builtins.open", mock_open(read_data="{}")),
    ):
        mock_args = Mock()
        mock_args.openapi_file = "spec.json"
        mock_args.openapi_use_token = True
        mock_create.return_value = (mock_args, Mock(), [])

        # Should call sys.exit(1) on failure (since local doesn't have token)
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            get_mcp_instance()
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 1


@patch("listmonk_api.mcp_server.get_client")
@patch("listmonk_api.mcp_server.config", {"enable_delegation": False})
@patch.dict(
    "os.environ",
    {
        "LISTMONK_URL": "http://localhost:9000",
        "LISTMONK_TOKEN": "secret",
        "OPENAPI_USERNAME": "admin",
        "OPENAPI_PASSWORD": "password",
    },
)
def test_get_mcp_instance_openapi_import_success(mock_get_client):
    with (
        patch("listmonk_api.mcp_server.create_mcp_server") as mock_create,
        patch("builtins.open", mock_open(read_data='{"openapi": "3.0.0"}')),
        patch("listmonk_api.mcp_server.FastMCP.from_openapi") as mock_from_openapi,
    ):
        mock_args = Mock()
        mock_args.openapi_file = "spec.json"
        mock_args.openapi_use_token = False
        mock_args.openapi_username = "admin"
        mock_args.openapi_password = "password"
        mock_args.openapi_client_id = None
        mock_args.openapi_client_secret = None
        mock_args.openapi_base_url = "http://localhost:9000"

        mock_mcp = FastMCP("test")
        mock_create.return_value = (mock_args, mock_mcp, [])

        mock_openapi_mcp = Mock()

        async def mock_get_tools():
            return []

        async def mock_get_resources():
            return []

        mock_openapi_mcp.get_tools = mock_get_tools
        mock_openapi_mcp.get_resources = mock_get_resources
        mock_from_openapi.return_value = mock_openapi_mcp

        mcp, args, middlewares, registered_tags, imported_tools = get_mcp_instance()
        # Verify that tools and resources were imported successfully
        assert mcp is mock_mcp


@patch("listmonk_api.mcp_server.get_mcp_instance")
def test_mcp_server_run_stdio(mock_get_instance):
    mock_mcp = Mock()
    mock_args = Mock()
    mock_args.transport = "stdio"
    mock_args.auth_type = "token"
    mock_args.eunomia_type = "none"
    mock_get_instance.return_value = (mock_mcp, mock_args, [], [], [])

    mcp_server()
    mock_mcp.run.assert_called_once_with(transport="stdio")


@patch("listmonk_api.mcp_server.get_mcp_instance")
def test_mcp_server_run_sse_and_http(mock_get_instance):
    mock_mcp = Mock()
    mock_args = Mock()
    mock_args.auth_type = "token"
    mock_args.eunomia_type = "none"

    # Test HTTP
    mock_args.transport = "streamable-http"
    mock_args.host = "127.0.0.1"
    mock_args.port = 8000
    mock_get_instance.return_value = (mock_mcp, mock_args, [], [], [])

    mcp_server()
    mock_mcp.run.assert_called_with(
        transport="streamable-http", host="127.0.0.1", port=8000
    )

    # Test SSE
    mock_args.transport = "sse"
    mcp_server()
    mock_mcp.run.assert_called_with(transport="sse", host="127.0.0.1", port=8000)


@patch("listmonk_api.mcp_server.get_mcp_instance")
def test_mcp_server_invalid_transport(mock_get_instance):
    mock_mcp = Mock()
    mock_args = Mock()
    mock_args.auth_type = "token"
    mock_args.eunomia_type = "none"
    mock_args.transport = "invalid-type"
    mock_get_instance.return_value = (mock_mcp, mock_args, [], [], [])

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        mcp_server()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1
