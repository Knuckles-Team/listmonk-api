"""MCP tools for listmonk campaigns operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field
from fastmcp.utilities.logging import get_logger
from listmonk_api.auth import get_client

logger = get_logger(name="ListmonkMCP")


def register_listmonk_campaigns_tools(mcp: FastMCP):
    @mcp.tool(tags={"listmonk_campaigns"})
    def listmonk_campaigns(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_campaigns', 'get_campaign', 'get_campaign_preview', 'get_campaign_stats', 'create_campaign', 'set_campaign_status', 'delete_campaign'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage listmonk campaigns operations."""
        if ctx:
            logger.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "get_campaigns":
            return {"results": client.get_campaigns(**kwargs)}
        if action == "get_campaign":
            return client.get_campaign(**kwargs)
        if action == "get_campaign_preview":
            return client.get_campaign_preview(**kwargs)
        if action == "get_campaign_stats":
            return client.get_campaign_stats(**kwargs)
        if action == "create_campaign":
            from listmonk_api.models import CampaignCreateRequest

            return client.create_campaign(CampaignCreateRequest(**kwargs))
        if action == "set_campaign_status":
            from listmonk_api.models import CampaignStatusRequest

            return client.set_campaign_status(
                campaign_id=kwargs["campaign_id"],
                data=CampaignStatusRequest(**kwargs["data"]),
            )
        if action == "delete_campaign":
            return client.delete_campaign(**kwargs)
        raise ValueError(f"Unknown action: {action}")
