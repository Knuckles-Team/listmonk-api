"""MCP tools for listmonk lists operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from agent_utilities.mcp.action_dispatch import resolve_action
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from fastmcp.utilities.logging import get_logger
from pydantic import Field

from listmonk_api.auth import get_client

logger = get_logger(name="ListmonkMCP")


def register_listmonk_lists_tools(mcp: FastMCP):
    @mcp.tool(tags={"listmonk_lists"})
    def listmonk_lists(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_lists', 'get_list', 'create_list', 'edit_list'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage listmonk lists operations."""
        if ctx:
            logger.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": "Operation failed"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        valid_actions = ("get_lists", "get_list", "create_list", "edit_list")
        resolved = resolve_action(action, valid_actions, service="listmonk-api")
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "get_lists":
            return {"results": client.get_lists(**kwargs)}
        if action == "get_list":
            return client.get_list(**kwargs)
        if action == "create_list":
            from listmonk_api.models import ListCreateRequest

            return client.create_list(ListCreateRequest(**kwargs))
        if action == "edit_list":
            from listmonk_api.models import ListEditRequest

            return client.edit_list(
                list_id=kwargs["list_id"], data=ListEditRequest(**kwargs["data"])
            )
        raise ValueError(f"Unknown action: {action}")
