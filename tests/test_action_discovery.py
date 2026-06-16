"""Verify standardized action discovery on listmonk MCP tools.

Asserts that the shared ``resolve_action`` helper wired into the
action-routed tools yields a ``list_actions`` discovery payload and a rich
'did you mean ... list_actions' error for unknown actions.
"""

from unittest.mock import MagicMock

import pytest

import listmonk_api.mcp_server as mcp_server


def _get_tool_fn(register):
    """Capture the raw callable a register_* function decorates with @mcp.tool."""
    captured = {}

    class _Recorder:
        def tool(self, *args, **kwargs):
            def deco(fn):
                captured["fn"] = fn
                return fn

            return deco

        def prompt(self, fn):
            return fn

    register(_Recorder())
    return captured["fn"]


REGISTRARS = [
    mcp_server.register_listmonk_subscribers_tools,
    mcp_server.register_listmonk_lists_tools,
    mcp_server.register_listmonk_imports_tools,
    mcp_server.register_listmonk_campaigns_tools,
    mcp_server.register_listmonk_media_tools,
    mcp_server.register_listmonk_templates_tools,
    mcp_server.register_listmonk_tx_tools,
]


@pytest.mark.parametrize("register", REGISTRARS)
def test_list_actions_returns_names(register):
    fn = _get_tool_fn(register)
    result = fn(action="list_actions", params_json="{}", client=MagicMock(), ctx=None)
    assert isinstance(result, dict)
    assert result.get("service") == "listmonk-api"
    assert isinstance(result.get("actions"), list)
    assert len(result["actions"]) >= 1


@pytest.mark.parametrize("register", REGISTRARS)
def test_bogus_action_raises_with_list_actions(register):
    fn = _get_tool_fn(register)
    with pytest.raises(ValueError) as exc:
        fn(
            action="definitely_not_an_action",
            params_json="{}",
            client=MagicMock(),
            ctx=None,
        )
    assert "list_actions" in str(exc.value)
