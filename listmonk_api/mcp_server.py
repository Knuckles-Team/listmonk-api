"""
Listmonk MCP Server.

Provides a Model Context Protocol (MCP) interface to manage Listmonk operations.
(Actionable Reporting)
(SDD Handoff)
"""

import warnings

from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from fastmcp.utilities.logging import get_logger
from pydantic import Field

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    try:
        from requests.exceptions import RequestsDependencyWarning

        warnings.filterwarnings("ignore", category=RequestsDependencyWarning)
    except ImportError:
        pass
warnings.filterwarnings("ignore", message=".*urllib3.*or chardet.*")
warnings.filterwarnings("ignore", message=".*urllib3.*or charset_normalizer.*")
import asyncio
import json
import logging
import sys
from threading import local
from typing import Any

import httpx
from agent_utilities.core.config import load_config, setting
from agent_utilities.mcp.action_dispatch import resolve_action
from agent_utilities.mcp.server_factory import (
    create_mcp_server,
)
from agent_utilities.mcp.server_factory import (
    mcp_auth_config as config,
)
from agent_utilities.mcp.verbose_tools import register_tool_surface

from listmonk_api.api_client import ListmonkAPI
from listmonk_api.auth import get_client

__version__ = "2.0.0"
logger = get_logger(name="ListmonkMCP")
logger.setLevel(logging.DEBUG)


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
        except Exception:
            return {"error": "Operation failed"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        valid_actions = (
            "get_subscribers",
            "get_subscriber",
            "get_subscribers_from_list",
            "create_subscriber",
        )
        resolved = resolve_action(action, valid_actions, service="listmonk-api")
        if isinstance(resolved, dict):
            return resolved
        action = resolved

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
        except Exception:
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
        except Exception:
            return {"error": "Operation failed"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        valid_actions = (
            "get_campaigns",
            "get_campaign",
            "get_campaign_preview",
            "get_campaign_stats",
            "create_campaign",
            "set_campaign_status",
            "delete_campaign",
        )
        resolved = resolve_action(action, valid_actions, service="listmonk-api")
        if isinstance(resolved, dict):
            return resolved
        action = resolved

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
        except Exception:
            return {"error": "Operation failed"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        valid_actions = ("get_media", "upload_media", "delete_media")
        resolved = resolve_action(action, valid_actions, service="listmonk-api")
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "get_media":
            return client.get_media(**kwargs)
        if action == "upload_media":
            from listmonk_api.models import MediaUploadRequest

            return client.upload_media(MediaUploadRequest(**kwargs))
        if action == "delete_media":
            return client.delete_media(**kwargs)
        raise ValueError(f"Unknown action: {action}")


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
        except Exception:
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
        except Exception:
            return {"error": "Operation failed"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        valid_actions = ("transactional_message",)
        resolved = resolve_action(action, valid_actions, service="listmonk-api")
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "transactional_message":
            from listmonk_api.models import TransactionalMessageRequest

            return client.transactional_message(TransactionalMessageRequest(**kwargs))
        raise ValueError(f"Unknown action: {action}")


def register_listmonk_ingest_tools(mcp: FastMCP):
    @mcp.tool(tags={"listmonk_ingest"})
    def listmonk_ingest(
        entity: str = Field(
            default="campaigns",
            description="What to ingest into the KG: 'campaigns', 'lists', or 'subscribers'.",
        ),
        params_json: str = Field(
            default="{}",
            description="JSON string of list filters (e.g. per_page, max_pages, list_id).",
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Natively ingest Listmonk records into epistemic-graph as typed nodes + documents.

        Lists campaigns / lists / subscribers via the Listmonk API and pushes them into
        the knowledge graph as ``:Campaign`` / ``:SubscriptionList`` / ``:Subscriber``
        nodes (+ :targetsList / :subscribedToList / :usesTemplate links, and campaign
        bodies as ``:Document`` nodes) via the fast engine client. Best-effort: returns
        ``{"ingested": None}`` when no engine is reachable.
        CONCEPT:AU-KG.ingest.enterprise-source-extractor.
        """
        if ctx:
            logger.info("Ingesting Listmonk %s into the KG...", entity)
        import json

        from listmonk_api.kg_ingest import (
            ingest_campaigns,
            ingest_lists,
            ingest_subscribers,
        )

        try:
            kwargs = json.loads(params_json) if params_json else {}
        except Exception:
            return {"error": "Operation failed"}
        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if entity == "campaigns":
            records = client.get_campaigns(**kwargs)
            result = ingest_campaigns(records)
        elif entity == "lists":
            records = client.get_lists(**kwargs)
            result = ingest_lists(records)
        elif entity == "subscribers":
            records = client.get_subscribers(**kwargs)
            result = ingest_subscribers(records)
        else:
            return {
                "error": f"Unknown entity '{entity}'. Use campaigns, lists, or subscribers."
            }

        listed = len(records) if isinstance(records, list) else 1
        return {"entity": entity, "listed": listed, "ingested": result}


def register_prompts(mcp: FastMCP):
    """Register MCP prompts."""

    @mcp.prompt
    def create_campaign_prompt(
        name: str, subject: str, list_ids: str, type: str = "regular"
    ) -> str:
        """
        Generates a prompt for creating a Listmonk campaign.
        """
        return f"Create a new Listmonk campaign with name '{name}', subject '{subject}', lists [{list_ids}], and type '{type}'. Use the listmonk_campaigns tool with action='create_campaign'."

    @mcp.prompt
    def send_transactional_message_prompt(
        subscriber_email: str, template_id: int
    ) -> str:
        """
        Generates a prompt for sending a Listmonk transactional message.
        """
        return f"Send a transactional message to {subscriber_email} using template ID {template_id}. Use the listmonk_tx tool with action='transactional_message'."


def get_mcp_instance() -> tuple[Any, Any, Any, Any, Any]:
    """Initialize and return the MCP instance, args, and middlewares."""
    load_config()
    args, mcp, middlewares = create_mcp_server(
        name="Listmonk",
        version=__version__,
        instructions="Listmonk MCP Server — Manage subscribers, lists, campaigns, templates, media, imports, and transactional messages.",
    )
    imported_tools = []
    imported_resources = []
    if args.openapi_file:
        if config["enable_delegation"]:
            raise ValueError("OpenAPI import not supported with delegation enabled")
        try:
            with open(args.openapi_file) as f:
                spec = json.load(f)

            async def _load_openapi_tools():
                token = None
                username = None
                password = None
                client_id = None
                client_secret = None
                if args.openapi_use_token:
                    token = getattr(local, "user_token", None)
                    if not token:
                        raise ValueError(
                            "OpenAPI import requires --openapi-use-token and a valid Bearer token in the request"
                        )
                    print("Using incoming JWT for OpenAPI import", file=sys.stderr)
                else:
                    username = args.openapi_username or setting("OPENAPI_USERNAME")
                    password = args.openapi_password or setting("OPENAPI_PASSWORD")
                    client_id = args.openapi_client_id or setting("OPENAPI_CLIENT_ID")
                    client_secret = args.openapi_client_secret or setting(
                        "OPENAPI_CLIENT_SECRET"
                    )
                    if not (username and password) and (
                        not (client_id and client_secret)
                    ):
                        raise ValueError(
                            "OpenAPI import requires either --openapi-use-token or (username+password) or (client_id+client_secret)"
                        )
                api = get_client()
                base_url = args.openapi_base_url or api.base_url
                async with httpx.AsyncClient(base_url=base_url) as client:
                    openapi_mcp = FastMCP.from_openapi(
                        openapi_spec=spec, client=client, name="OpenAPI Tools"
                    )
                    tools = await openapi_mcp.get_tools()
                    resources = await openapi_mcp.get_resources()
                    return (tools, resources)

            print("Importing OpenAPI tools...", file=sys.stderr)
            imported_tools, imported_resources = asyncio.run(_load_openapi_tools())
            print(
                f"Imported {len(imported_tools)} tools, {len(imported_resources)} resources",
                file=sys.stderr,
            )
            for tool in imported_tools:
                mcp.add_tool(tool)
            for resource in imported_resources:
                mcp.add_resource(resource)
        except Exception as exc:
            print(f"Operation failed: {type(exc).__name__}", file=sys.stderr)
            logger.error("OpenAPI import failed", extra={"error": "Operation failed"})
            sys.exit(1)

    registered_tags = register_tool_surface(
        mcp,
        client_cls=ListmonkAPI,
        get_client=get_client,
        service="listmonk-api",
        tools_module=sys.modules[__name__],
    )
    register_prompts(mcp)
    for tool in imported_tools:
        mcp.add_tool(tool)
    for resource in imported_resources:
        mcp.add_resource(resource)
    for mw in middlewares:
        mcp.add_middleware(mw)
    return (mcp, args, middlewares, registered_tags, imported_tools)


def mcp_server() -> None:
    mcp, args, middlewares, registered_tags, imported_tools = get_mcp_instance()
    print("\nStarting Listmonk MCP Server", file=sys.stderr)
    print(f"  Transport: {args.transport.upper()}", file=sys.stderr)
    print(f"  Auth: {args.auth_type}", file=sys.stderr)
    print(
        f"  Delegation: {('ON' if config['enable_delegation'] else 'OFF')}",
        file=sys.stderr,
    )
    print(f"  Eunomia: {args.eunomia_type}", file=sys.stderr)
    print(f"  Imported OpenAPI Tools: {len(imported_tools)} total", file=sys.stderr)
    if args.transport == "stdio":
        mcp.run(transport="stdio")
    elif args.transport == "streamable-http":
        mcp.run(transport="streamable-http", host=args.host, port=args.port)
    elif args.transport == "sse":
        mcp.run(transport="sse", host=args.host, port=args.port)
    else:
        logger.error("Invalid transport", extra={"transport": args.transport})
        sys.exit(1)


if __name__ == "__main__":
    mcp_server()
