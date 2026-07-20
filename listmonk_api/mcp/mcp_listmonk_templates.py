"""MCP tools for listmonk templates operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from agent_utilities.mcp.action_dispatch import resolve_action
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from fastmcp.utilities.logging import get_logger
from pydantic import Field

from listmonk_api.auth import get_client

logger = get_logger(name="ListmonkMCP")


def register_listmonk_templates_tools(mcp: FastMCP):
    @mcp.tool(tags={"listmonk_templates"})
    def listmonk_templates(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_templates', 'get_template', 'get_template_preview', 'set_default_template', 'delete_template'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage listmonk templates operations."""
        if ctx:
            logger.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": "Operation failed"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        valid_actions = (
            "get_templates",
            "get_template",
            "get_template_preview",
            "set_default_template",
            "delete_template",
        )
        resolved = resolve_action(action, valid_actions, service="listmonk-api")
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "get_templates":
            return {"results": client.get_templates(**kwargs)}
        if action == "get_template":
            return client.get_template(**kwargs)
        if action == "get_template_preview":
            return client.get_template_preview(**kwargs)
        if action == "set_default_template":
            return client.set_default_template(**kwargs)
        if action == "delete_template":
            return client.delete_template(**kwargs)
        raise ValueError(f"Unknown action: {action}")
