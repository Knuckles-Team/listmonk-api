# Listmonk Api
## CLI or API | MCP | Agent

![PyPI - Version](https://img.shields.io/pypi/v/listmonk-api)
![MCP Server](https://badge.mcpx.dev?type=server 'MCP Server')
![PyPI - Downloads](https://img.shields.io/pypi/dd/listmonk-api)
![GitHub Repo stars](https://img.shields.io/github/stars/Knuckles-Team/listmonk-api)
![GitHub forks](https://img.shields.io/github/forks/Knuckles-Team/listmonk-api)
![GitHub contributors](https://img.shields.io/github/contributors/Knuckles-Team/listmonk-api)
![PyPI - License](https://img.shields.io/pypi/l/listmonk-api)
![GitHub](https://img.shields.io/github/license/Knuckles-Team/listmonk-api)
![GitHub last commit (by committer)](https://img.shields.io/github/last-commit/Knuckles-Team/listmonk-api)
![GitHub pull requests](https://img.shields.io/github/issues-pr/Knuckles-Team/listmonk-api)
![GitHub closed pull requests](https://img.shields.io/github/issues-pr-closed/Knuckles-Team/listmonk-api)
![GitHub issues](https://img.shields.io/github/issues/Knuckles-Team/listmonk-api)
![GitHub top language](https://img.shields.io/github/languages/top/Knuckles-Team/listmonk-api)
![GitHub language count](https://img.shields.io/github/languages/count/Knuckles-Team/listmonk-api)
![GitHub repo size](https://img.shields.io/github/repo-size/Knuckles-Team/listmonk-api)
![GitHub repo file count (file type)](https://img.shields.io/github/directory-file-count/Knuckles-Team/listmonk-api)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/listmonk-api)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/listmonk-api)

*Version: 0.26.0*

> **Documentation** — Installation, deployment, usage across the API, CLI, MCP, and
> agent interfaces, and guidance for provisioning the Listmonk platform are maintained
> in the [official documentation](https://knuckles-team.github.io/listmonk-api/).

---

## Overview

**Listmonk Api** is a production-grade Agent and Model Context Protocol (MCP) server designed to interface directly with Python Listmonk API Wrapper.

---

## Key Features

- **Consolidated Action-Routed MCP Tools:** Minimizes token overhead and eliminates tool bloat in LLM contexts by grouping methods into optimized, togglable tool modules.
- **Enterprise-Grade Security:** Comprehensive support for Eunomia policies, OIDC token delegation, and granular execution context tracking.
- **Integrated Graph Agent:** Built-in Pydantic AI agent supporting the Agent Control Protocol (ACP) and standard Web interfaces (AG-UI).
- **Native Telemetry & Tracing:** Out-of-the-box OpenTelemetry exports and native Langfuse tracing.

---

## CLI or API

This agent wraps the Python Listmonk API Wrapper API. You can interact with it programmatically or via its integrated execution entrypoints.

Detailed instructions on how to use the underlying API wrappers, extended schema bindings, and developer SDK references are maintained in [docs/index.md](docs/index.md).

---

## MCP

This server utilizes dynamic Action-Routed tools to optimize token overhead and maximize IDE compatibility.

### Available MCP Tools

Auto-generated — do not edit between the markers below.

<!-- MCP-TOOLS-TABLE:START -->

| MCP Tool | Toggle Env Var | Description |
|----------|----------------|-------------|
| `listmonk_campaigns` | `LISTMONK_CAMPAIGNSTOOL` | Manage listmonk campaigns operations. |
| `listmonk_imports` | `LISTMONK_IMPORTSTOOL` | Manage listmonk imports operations. |
| `listmonk_lists` | `LISTMONK_LISTSTOOL` | Manage listmonk lists operations. |
| `listmonk_media` | `LISTMONK_MEDIATOOL` | Manage listmonk media operations. |
| `listmonk_subscribers` | `LISTMONK_SUBSCRIBERSTOOL` | Manage listmonk subscribers operations. |
| `listmonk_templates` | `LISTMONK_TEMPLATESTOOL` | Manage listmonk templates operations. |
| `listmonk_tx` | `LISTMONK_TXTOOL` | Manage listmonk tx operations. |

_7 action-routed tools (default `MCP_TOOL_MODE=condensed`). Each is enabled unless its toggle is set false; set `MCP_TOOL_MODE=verbose` (or `both`) for the 1:1 per-operation surface. Auto-generated — do not edit._
<!-- MCP-TOOLS-TABLE:END -->

### Dynamic Tool Selection & Visibility

This MCP server supports dynamic toolset selection and visibility filtering at runtime. This allows you to restrict the set of exposed tools in order to prevent blowing up the LLM's context window.

You can configure tool filtering via multiple input channels:

- **CLI Arguments:** Pass `--tools` or `--toolsets` (or their disabled counterparts `--disabled-tools` and `--disabled-toolsets`) during startup.
- **Environment Variables:** Define standard environment variables:
  - `MCP_ENABLED_TOOLS` / `MCP_DISABLED_TOOLS`
  - `MCP_ENABLED_TAGS` / `MCP_DISABLED_TAGS`
- **HTTP SSE Request Headers:** Pass custom headers during transport initialization:
  - `x-mcp-enabled-tools` / `x-mcp-disabled-tools`
  - `x-mcp-enabled-tags` / `x-mcp-disabled-tags`
- **HTTP SSE Request Query Parameters:** Append query parameters directly to your transport connection URL:
  - `?tools=tool1,tool2`
  - `?tags=tag1`

When query strings or parameters are supplied, an LLM-free **Knowledge Graph resolution layer** (using `DynamicToolOrchestrator`) matches query intents against known tool tags, names, or descriptions, with safe fallback and automated 24-hour background cache refreshing.

---

### MCP Configuration Examples

#### stdio Transport (Recommended for local IDEs e.g., Cursor, Claude Desktop)
Configure your IDE's `mcp.json` to launch the MCP server via `uvx`:

```json
{
  "mcpServers": {
    "listmonk-api": {
      "command": "uvx",
      "args": [
        "--from",
        "listmonk-api",
        "listmonk-mcp"
      ],
      "env": {
        "LISTMONK_URL": "your_listmonk_url_here",
        "LISTMONK_USERNAME": "your_listmonk_username_here",
        "LISTMONK_PASSWORD": "your_listmonk_password_here"
      }
    }
  }
}
```

#### Streamable-HTTP Transport (Recommended for production deployments)
Configure your client's `mcp.json` to launch the Streamable-HTTP server via `uvx` with explicit host and port definition:

```json
{
  "mcpServers": {
    "listmonk-api": {
      "command": "uvx",
      "args": [
        "--from",
        "listmonk-api",
        "listmonk-mcp"
      ],
      "env": {
        "TRANSPORT": "streamable-http",
        "HOST": "0.0.0.0",
        "PORT": "8000",
        "LISTMONK_URL": "your_listmonk_url_here",
        "LISTMONK_USERNAME": "your_listmonk_username_here",
        "LISTMONK_PASSWORD": "your_listmonk_password_here"
      }
    }
  }
}
```

Alternatively, connect to a pre-deployed remote or local Streamable-HTTP instance:

```json
{
  "mcpServers": {
    "listmonk-api": {
      "url": "http://localhost:8000/listmonk-api/mcp"
    }
  }
}
```

Deploying the Streamable-HTTP server via Docker:

```bash
docker run -d \
  --name listmonk-api-mcp \
  -p 8000:8000 \
  -e TRANSPORT=streamable-http \
  -e PORT=8000 \
  -e LISTMONK_URL="your_listmonk_url_here" \
  -e LISTMONK_USERNAME="your_listmonk_username_here" \
  -e LISTMONK_PASSWORD="your_listmonk_password_here" \
  knucklessg1/listmonk-api:latest
```

---

<!-- BEGIN GENERATED: additional-deployment-options -->
### Additional Deployment Options

`listmonk-api` can also run as a **local container** (Docker / Podman / `uv`) or be
consumed from a **remote deployment**. The
[Deployment guide](https://knuckles-team.github.io/listmonk-api/deployment/) has full, copy-paste
`mcp_config.json` for all four transports — **stdio**, **streamable-http**,
**local container / uv**, and **remote URL**:

- **Local container / uv** — launch the server from `mcp_config.json` via `uvx`,
  `docker run`, or `podman run`, or point at a local streamable-http container by `url`.
- **Remote URL** — connect to a server deployed behind Caddy at
  `http://listmonk-mcp.arpa/mcp` using the `"url"` key.
<!-- END GENERATED: additional-deployment-options -->

## Agent

This repository features a fully integrated Pydantic AI Graph Agent. It communicates over the **Agent Control Protocol (ACP)** and interacts seamlessly with the **Agent Web UI (AG-UI)** and Terminal interface.

### Running the Agent CLI
To start the interactive command-line agent:

```bash
# Set credentials
export LISTMONK_URL="your_listmonk_url_here"
export LISTMONK_USERNAME="your_listmonk_username_here"
export LISTMONK_PASSWORD="your_listmonk_password_here"

# Run the agent server
listmonk-agent --provider openai --model-id gpt-4o
```

### Docker Compose Orchestration
The following `docker/agent.compose.yml` configures the Agent, Web UI, and Terminal Interface together:

```yaml
version: '3.8'

services:
  listmonk-api-mcp:
    image: knucklessg1/listmonk-api:latest
    container_name: listmonk-api-mcp
    hostname: listmonk-api-mcp
    restart: always
    env_file:
      - ../.env
    environment:
      - PYTHONUNBUFFERED=1
      - HOST=0.0.0.0
      - PORT=8000
      - TRANSPORT=streamable-http
    ports:
      - "8000:8000"
    healthcheck:
      test: ["CMD", "python3", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"

  listmonk-api-agent:
    image: knucklessg1/listmonk-api:latest
    container_name: listmonk-api-agent
    hostname: listmonk-api-agent
    restart: always
    depends_on:
      - listmonk-api-mcp
    env_file:
      - ../.env
    command: [ "listmonk-agent" ]
    environment:
      - PYTHONUNBUFFERED=1
      - HOST=0.0.0.0
      - PORT=9004
      - MCP_URL=http://listmonk-api-mcp:8000/mcp
      - PROVIDER=${PROVIDER:-openai}
      - MODEL_ID=${MODEL_ID:-gpt-4o}
      - ENABLE_WEB_UI=True
      - ENABLE_OTEL=True
    ports:
      - "9004:9004"
    healthcheck:
      test: ["CMD", "python3", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:9004/health')"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"

```

Detailed graph node architecture explanations, custom skill configurations, and agentic trace guides are available in [docs/agent.md](docs/agent.md).

---

## Security & Governance

Built directly upon the enterprise-ready [`agent-utilities`](https://github.com/Knuckles-Team/agent-utilities) core, standard security parameters are fully supported:

### Access Control & Policy Enforcement
- **Eunomia Policies:** Fine-grained, policy-driven tool authorization. Supports `none`, local `embedded` (`mcp_policies.json`), or centralized `remote` modes.
- **OIDC Token Delegation:** Compliant with RFC 8693 token exchange for flowing authenticating user credentials from Web UI / ACP → Agent → MCP.
- **Scoped Credentials:** Execution context runs restricted to the specific caller identity.

### Runtime Security Grid
| Feature | Functionality | Enablement |
|---------|---------------|------------|
| **Tool Guard** | Sensitivity inspection with human-in-the-loop validation | Enabled by default |
| **Prompt Injection Defense** | Input scanning, repetition monitoring, and recursive loop blocks | Enabled by default |
| **Context Safety Guard** | Stuck-loop detectors and contextual overflow preemptive alerts | Enabled by default |

---

## Environment Variables

The server and client support standard configuration environment variables:

| Variable | Description | Default |
|---|---|---|
| `LISTMONK_URL` | Base URL of your Listmonk instance. | `http://localhost:8080` |
| `LISTMONK_TOKEN` | Bearer Token used for secure API authorization. | `""` |
| `LISTMONK_USERNAME` | Username for Basic Authorization (if token is empty). | `""` |
| `LISTMONK_PASSWORD` | Password for Basic Authorization (if token is empty). | `""` |
| **Toggles** | | |
| `LISTMONK_SUBSCRIBERSTOOL`| Enable or disable the `listmonk_subscribers` tool. | `True` |
| `LISTMONK_LISTSTOOL` | Enable or disable the `listmonk_lists` tool. | `True` |
| `LISTMONK_IMPORTSTOOL` | Enable or disable the `listmonk_imports` tool. | `True` |
| `LISTMONK_CAMPAIGNSTOOL` | Enable or disable the `listmonk_campaigns` tool. | `True` |
| `LISTMONK_MEDIATOOL` | Enable or disable the `listmonk_media` tool. | `True` |
| `LISTMONK_TEMPLATESTOOL` | Enable or disable the `listmonk_templates` tool. | `True` |
| `LISTMONK_TXTOOL` | Enable or disable the `listmonk_tx` tool. | `True` |
| **Security & Policies** | | |
| `AUTH_TYPE` | Type of API authentication schema required. | `""` |
| `EUNOMIA_TYPE` | Type of authorization engine policy enforcement (`none`, `embedded`, `remote`). | `none` |
| `EUNOMIA_POLICY_FILE` | Path to your local policy definition file (e.g., `mcp_policies.json`). | `""` |
| `EUNOMIA_REMOTE_URL` | Host/Port URL pointing to a remote Eunomia policy daemon. | `""` |
| `ALLOWED_CLIENT_REDIRECT_URIS`| Whitelisted URIs allowed to complete Oauth/OIDC identity validation flows. | `""` |
| `OAUTH_BASE_URL` | Base endpoint of your trusted OAuth provider. | `""` |
| `OIDC_BASE_URL` | Base endpoint of your OIDC identity provider. | `""` |
| **OpenAPI Docs** | | |
| `OPENAPI_USERNAME` | Username whitelisted to view internal raw API specifications. | `""` |
| `OPENAPI_PASSWORD` | Password whitelisted to view internal raw API specifications. | `""` |
| `OPENAPI_BEARER_TOKEN` | Bearer authorization token used to limit raw API specifications access. | `""` |

---

## Installation

Install the Python package locally:

```bash
# Using uv (highly recommended)
uv pip install listmonk-api[all]

# Using standard pip
python -m pip install listmonk-api[all]
```

---

## Documentation

The complete documentation is published as the
[official documentation site](https://knuckles-team.github.io/listmonk-api/) and is the
recommended reference for installation, deployment, and day-to-day operation.

| Page | Contents |
|---|---|
| [Installation](https://knuckles-team.github.io/listmonk-api/installation/) | pip, source, extras, prebuilt Docker image |
| [Deployment](https://knuckles-team.github.io/listmonk-api/deployment/) | run the MCP and agent servers, Compose, Caddy + Technitium, env config |
| [Usage](https://knuckles-team.github.io/listmonk-api/usage/) | the MCP tools, the `ListmonkAPI` client, the agent CLI |
| [Backing Platform](https://knuckles-team.github.io/listmonk-api/platform/) | deploy Listmonk with Docker |
| [Overview](https://knuckles-team.github.io/listmonk-api/overview/) | API structure, tool reference, quick start |
| [Concepts](https://knuckles-team.github.io/listmonk-api/concepts/) | concept registry (`CONCEPT:LM-*`) |

---

## Repository Owners

<img width="100%" height="180em" src="https://github-readme-stats.vercel.app/api?username=Knucklessg1&show_icons=true&hide_border=true&&count_private=true&include_all_commits=true" />

![GitHub followers](https://img.shields.io/github/followers/Knucklessg1)
![GitHub User's stars](https://img.shields.io/github/stars/Knucklessg1)

---

## Contribute

Contributions are welcome! Please ensure code quality by executing local checks before submitting pull requests:
- Format code using `ruff format .`
- Lint code using `ruff check .`
- Validate type-safety with `mypy .`
- Execute test suites using `pytest`


<!-- BEGIN agent-os-genesis-deploy (generated; do not edit between markers) -->

## Deploy with `agent-os-genesis`

This package can be provisioned for you — skill-guided — by the **`agent-os-genesis`**
universal skill (its *single-package deploy mode*): it picks your install method, seeds
secrets to OpenBao/Vault (or `.env`), trusts your enterprise CA, registers the MCP
server, and verifies it — the same machinery that stands up the whole Agent OS, narrowed
to just this package. Ask your agent to **"deploy `listmonk-api` with agent-os-genesis"**.

| Install mode | Command |
|------|---------|
| Bare-metal, prod (PyPI) | `uvx listmonk-mcp` · or `uv tool install listmonk-api` |
| Bare-metal, dev (editable) | `uv pip install -e ".[all]"` · or `pip install -e ".[all]"` |
| Container, prod | deploy `knucklessg1/listmonk-api:latest` via docker-compose / swarm / podman / podman-compose / kubernetes |
| Container, dev (editable) | deploy `docker/compose.dev.yml` (source-mounted at `/src`; edits live on restart) |

Secrets are read-existing + seeded via `vault_sync` — you are only prompted for what's missing.

<!-- END agent-os-genesis-deploy -->
