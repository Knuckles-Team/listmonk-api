# listmonk-api

A Python **API client, MCP Server, and A2A agent** for [Listmonk](https://listmonk.app/)
— the self-hosted newsletter and mailing-list manager — built on the agent-utilities
ecosystem.

!!! info "Official documentation"
    This site is the canonical reference for `listmonk-api`, maintained alongside every
    release.

[![PyPI](https://img.shields.io/pypi/v/listmonk-api)](https://pypi.org/project/listmonk-api/)
![MCP Server](https://badge.mcpx.dev?type=server 'MCP Server')
[![License](https://img.shields.io/pypi/l/listmonk-api)](https://github.com/Knuckles-Team/listmonk-api/blob/main/LICENSE)
[![GitHub](https://img.shields.io/badge/source-GitHub-181717?logo=github)](https://github.com/Knuckles-Team/listmonk-api)

## Overview

`listmonk-api` wraps Listmonk's REST API with a typed, modular Python client and a
deterministic MCP tool surface, and ships a Pydantic-AI agent server for conversational
automation. It provides:

- **`ListmonkAPI`** — a delegated-subclassing client that aggregates dedicated
  sub-API managers for subscribers, lists, campaigns, media, templates, imports, and
  transactional messaging.
- **Action-routed MCP tools** — togglable tool modules that group related operations
  to minimize LLM context overhead while keeping permissions granular.
- **An integrated A2A agent** — a Pydantic-AI graph agent (console script
  `listmonk-agent`) with an optional web interface, wired to the MCP server.

The connector remains inactive when credentials are absent, so it is safe to install
ahead of provisioning a Listmonk instance.

## Explore the documentation

<div class="grid cards" markdown>

- :material-rocket-launch: **[Installation](installation.md)** — pip, source, extras, and the prebuilt Docker image.
- :material-server-network: **[Deployment](deployment.md)** — run the MCP and agent servers, Docker Compose, Caddy + Technitium.
- :material-console: **[Usage](usage.md)** — the MCP tools, the `ListmonkAPI` client, and the agent CLI.
- :material-database-cog: **[Backing Platform](platform.md)** — deploy Listmonk with Docker.
- :material-sitemap: **[Overview](overview.md)** — API structure, tool reference, and quick start.
- :material-tag-multiple: **[Concepts](concepts.md)** — the `CONCEPT:LM-*` registry.

</div>

## Quick start

```bash
pip install "listmonk-api[all]"
listmonk-mcp                     # stdio MCP server (default transport)
```

Connect it to a Listmonk instance:

```bash
export LISTMONK_URL=https://listmonk.yourdomain.com
export LISTMONK_TOKEN=your-bearer-token
listmonk-mcp --transport streamable-http --host 0.0.0.0 --port 8000
```

See **[Installation](installation.md)** and **[Deployment](deployment.md)** for the
full matrix (PyPI extras, Docker image, all transports, agent server, reverse proxy, DNS).
