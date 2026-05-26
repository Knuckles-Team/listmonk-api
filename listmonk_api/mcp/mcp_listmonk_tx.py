"""MCP tools for listmonk tx operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field
from fastmcp.utilities.logging import get_logger
from listmonk_api.auth import get_client

logger = get_logger(name="ListmonkMCP")


def register_listmonk_tx_tools(mcp: FastMCP):
    @mcp.tool(tags={"listmonk_tx"})
    def listmonk_tx(
        action: str = Field(
            description="Action to perform. Must be one of: 'transactional_message'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage listmonk tx operations."""
        if ctx:
            logger.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "transactional_message":
            from listmonk_api.models import TransactionalMessageRequest

            return client.transactional_message(TransactionalMessageRequest(**kwargs))
        raise ValueError(f"Unknown action: {action}")
