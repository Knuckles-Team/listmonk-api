"""MCP tools for listmonk subscribers operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field
from fastmcp.utilities.logging import get_logger
from listmonk_api.auth import get_client

logger = get_logger(name="ListmonkMCP")


def register_listmonk_subscribers_tools(mcp: FastMCP):
    @mcp.tool(tags={"listmonk_subscribers"})
    def listmonk_subscribers(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_subscribers', 'get_subscriber', 'get_subscribers_from_list', 'create_subscriber'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage listmonk subscribers operations."""
        if ctx:
            logger.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "get_subscribers":
            return {"results": client.get_subscribers(**kwargs)}
        if action == "get_subscriber":
            return client.get_subscriber(**kwargs)
        if action == "get_subscribers_from_list":
            return client.get_subscribers_from_list(**kwargs)
        if action == "create_subscriber":
            from listmonk_api.models import SubscriberCreateRequest

            return client.create_subscriber(SubscriberCreateRequest(**kwargs))
        raise ValueError(f"Unknown action: {action}")
