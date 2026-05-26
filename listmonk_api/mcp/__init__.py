"""MCP tool registration modules for listmonk-api.

Auto-generated during ecosystem standardization.
Each domain has its own module with a register_*_tools function.
"""

from listmonk_api.mcp.mcp_listmonk_campaigns import register_listmonk_campaigns_tools
from listmonk_api.mcp.mcp_listmonk_imports import register_listmonk_imports_tools
from listmonk_api.mcp.mcp_listmonk_lists import register_listmonk_lists_tools
from listmonk_api.mcp.mcp_listmonk_media import register_listmonk_media_tools
from listmonk_api.mcp.mcp_listmonk_subscribers import (
    register_listmonk_subscribers_tools,
)
from listmonk_api.mcp.mcp_listmonk_templates import register_listmonk_templates_tools
from listmonk_api.mcp.mcp_listmonk_tx import register_listmonk_tx_tools

__all__ = [
    "register_listmonk_campaigns_tools",
    "register_listmonk_imports_tools",
    "register_listmonk_lists_tools",
    "register_listmonk_media_tools",
    "register_listmonk_subscribers_tools",
    "register_listmonk_templates_tools",
    "register_listmonk_tx_tools",
]
