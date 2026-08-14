"""MCP tools for listmonk imports operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from agent_utilities.mcp.action_dispatch import resolve_action
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from fastmcp.utilities.logging import get_logger
from pydantic import Field

from listmonk_api.auth import get_client

logger = get_logger(name="ListmonkMCP")


def register_listmonk_imports_tools(mcp: FastMCP):
    @mcp.tool(tags={"listmonk_imports"})
    def listmonk_imports(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_subscriber_import_status', 'get_subscriber_import_logs', 'import_subscribers', 'delete_subscriber_import'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage listmonk imports operations."""
        if ctx:
            logger.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception:
            return {"error": "Operation failed"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        valid_actions = (
            "get_subscriber_import_status",
            "get_subscriber_import_logs",
            "import_subscribers",
            "delete_subscriber_import",
        )
        resolved = resolve_action(action, valid_actions, service="listmonk-api")
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "get_subscriber_import_status":
            return client.get_subscriber_import_status()
        if action == "get_subscriber_import_logs":
            return client.get_subscriber_import_logs()
        if action == "import_subscribers":
            from listmonk_api.models import ImportSubscribersRequest

            return client.import_subscribers(ImportSubscribersRequest(**kwargs))
        if action == "delete_subscriber_import":
            return client.delete_subscriber_import()
        raise ValueError(f"Unknown action: {action}")
