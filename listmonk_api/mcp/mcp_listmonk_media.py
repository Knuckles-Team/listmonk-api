"""MCP tools for listmonk media operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field
from fastmcp.utilities.logging import get_logger
from listmonk_api.auth import get_client

logger = get_logger(name="ListmonkMCP")


def register_listmonk_media_tools(mcp: FastMCP):
    @mcp.tool(tags={"listmonk_media"})
    def listmonk_media(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_media', 'upload_media', 'delete_media'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage listmonk media operations."""
        if ctx:
            logger.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "get_media":
            return client.get_media(**kwargs)
        if action == "upload_media":
            from listmonk_api.models import MediaUploadRequest

            return client.upload_media(MediaUploadRequest(**kwargs))
        if action == "delete_media":
            return client.delete_media(**kwargs)
        raise ValueError(f"Unknown action: {action}")
