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

*Version: 1.0.0*

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

#### Condensed action-routed tools (default — `MCP_TOOL_MODE=condensed`)

| MCP Tool | Toggle Env Var | Description |
|----------|----------------|-------------|
| `listmonk_campaigns` | `LISTMONK_CAMPAIGNSTOOL` | Manage listmonk campaigns operations. |
| `listmonk_imports` | `LISTMONK_IMPORTSTOOL` | Manage listmonk imports operations. |
| `listmonk_lists` | `LISTMONK_LISTSTOOL` | Manage listmonk lists operations. |
| `listmonk_media` | `LISTMONK_MEDIATOOL` | Manage listmonk media operations. |
| `listmonk_subscribers` | `LISTMONK_SUBSCRIBERSTOOL` | Manage listmonk subscribers operations. |
| `listmonk_templates` | `LISTMONK_TEMPLATESTOOL` | Manage listmonk templates operations. |
| `listmonk_tx` | `LISTMONK_TXTOOL` | Manage listmonk tx operations. |

#### Verbose 1:1 API-mapped tools (`MCP_TOOL_MODE=verbose` or `both`)

<details>
<summary>32 per-operation tools — one per public API method (click to expand)</summary>

| MCP Tool | Toggle Env Var | Description |
|----------|----------------|-------------|
| `listmonk_create_campaign` | `LISTMONK_APITOOL` | Invoke the create_campaign operation. |
| `listmonk_create_list` | `LISTMONK_APITOOL` | Invoke the create_list operation. |
| `listmonk_create_subscriber` | `LISTMONK_APITOOL` | Invoke the create_subscriber operation. |
| `listmonk_delete` | `BASE_API_CLIENTTOOL` | Invoke the delete operation. |
| `listmonk_delete_campaign` | `LISTMONK_APITOOL` | Invoke the delete_campaign operation. |
| `listmonk_delete_media` | `LISTMONK_APITOOL` | Invoke the delete_media operation. |
| `listmonk_delete_subscriber_import` | `LISTMONK_APITOOL` | Invoke the delete_subscriber_import operation. |
| `listmonk_delete_template` | `LISTMONK_APITOOL` | Invoke the delete_template operation. |
| `listmonk_edit_list` | `LISTMONK_APITOOL` | Invoke the edit_list operation. |
| `listmonk_get` | `BASE_API_CLIENTTOOL` | Invoke the get operation. |
| `listmonk_get_campaign` | `LISTMONK_APITOOL` | Invoke the get_campaign operation. |
| `listmonk_get_campaign_preview` | `LISTMONK_APITOOL` | Invoke the get_campaign_preview operation. |
| `listmonk_get_campaign_stats` | `LISTMONK_APITOOL` | Invoke the get_campaign_stats operation. |
| `listmonk_get_campaigns` | `LISTMONK_APITOOL` | Invoke the get_campaigns operation. |
| `listmonk_get_list` | `LISTMONK_APITOOL` | Invoke the get_list operation. |
| `listmonk_get_lists` | `LISTMONK_APITOOL` | Invoke the get_lists operation. |
| `listmonk_get_media` | `LISTMONK_APITOOL` | Invoke the get_media operation. |
| `listmonk_get_subscriber` | `LISTMONK_APITOOL` | Invoke the get_subscriber operation. |
| `listmonk_get_subscriber_import_logs` | `LISTMONK_APITOOL` | Invoke the get_subscriber_import_logs operation. |
| `listmonk_get_subscriber_import_status` | `LISTMONK_APITOOL` | Invoke the get_subscriber_import_status operation. |
| `listmonk_get_subscribers` | `LISTMONK_APITOOL` | Invoke the get_subscribers operation. |
| `listmonk_get_subscribers_from_list` | `LISTMONK_APITOOL` | Invoke the get_subscribers_from_list operation. |
| `listmonk_get_template` | `LISTMONK_APITOOL` | Invoke the get_template operation. |
| `listmonk_get_template_preview` | `LISTMONK_APITOOL` | Invoke the get_template_preview operation. |
| `listmonk_get_templates` | `LISTMONK_APITOOL` | Invoke the get_templates operation. |
| `listmonk_import_subscribers` | `LISTMONK_APITOOL` | Invoke the import_subscribers operation. |
| `listmonk_post` | `BASE_API_CLIENTTOOL` | Invoke the post operation. |
| `listmonk_put` | `BASE_API_CLIENTTOOL` | Invoke the put operation. |
| `listmonk_set_campaign_status` | `LISTMONK_APITOOL` | Invoke the set_campaign_status operation. |
| `listmonk_set_default_template` | `LISTMONK_APITOOL` | Invoke the set_default_template operation. |
| `listmonk_transactional_message` | `LISTMONK_APITOOL` | Invoke the transactional_message operation. |
| `listmonk_upload_media` | `LISTMONK_APITOOL` | Invoke the upload_media operation. |

</details>

_7 action-routed tool(s) (default) · 32 verbose 1:1 tool(s). Each is enabled unless its `<DOMAIN>TOOL` toggle is set false; `MCP_TOOL_MODE` selects the surface (`condensed` default · `verbose` 1:1 · `both`). Auto-generated — do not edit._
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

<!-- MCP-CONFIG-EXAMPLES:START -->

> **Install the slim `[mcp]` extra.** All examples install `listmonk-api[mcp]` — the
> MCP-server extra that pulls only the FastMCP / FastAPI tooling (`agent-utilities[mcp]`).
> It deliberately **excludes** the heavy agent runtime (`pydantic-ai`, the epistemic-graph
> engine, `dspy`, `llama-index`), so `uvx` / container installs are far smaller. Use the
> full `[agent]` extra only when you need the integrated Pydantic AI agent.

#### stdio Transport (local IDEs — Cursor, Claude Desktop, VS Code)

```json
{
  "mcpServers": {
    "listmonk-mcp": {
      "command": "uvx",
      "args": [
        "--from",
        "listmonk-api[mcp]",
        "listmonk-mcp"
      ],
      "env": {
        "MCP_TOOL_MODE": "condensed",
        "LISTMONK_CAMPAIGNSTOOL": "True",
        "LISTMONK_IMPORTSTOOL": "True",
        "LISTMONK_LISTSTOOL": "True",
        "LISTMONK_MEDIATOOL": "True",
        "LISTMONK_SUBSCRIBERSTOOL": "True",
        "LISTMONK_TEMPLATESTOOL": "True",
        "LISTMONK_TOKEN": "your_bearer_token_here",
        "LISTMONK_TXTOOL": "True",
        "LISTMONK_URL": "http://localhost:8080",
        "OPENAPI_CLIENT_ID": "",
        "OPENAPI_PASSWORD": "adminpassword",
        "OPENAPI_USERNAME": "admin"
      }
    }
  }
}
```

#### Streamable-HTTP Transport (networked / production)

```json
{
  "mcpServers": {
    "listmonk-mcp": {
      "command": "uvx",
      "args": [
        "--from",
        "listmonk-api[mcp]",
        "listmonk-mcp",
        "--transport",
        "streamable-http",
        "--port",
        "8000"
      ],
      "env": {
        "TRANSPORT": "streamable-http",
        "HOST": "0.0.0.0",
        "PORT": "8000",
        "MCP_TOOL_MODE": "condensed",
        "LISTMONK_CAMPAIGNSTOOL": "True",
        "LISTMONK_IMPORTSTOOL": "True",
        "LISTMONK_LISTSTOOL": "True",
        "LISTMONK_MEDIATOOL": "True",
        "LISTMONK_SUBSCRIBERSTOOL": "True",
        "LISTMONK_TEMPLATESTOOL": "True",
        "LISTMONK_TOKEN": "your_bearer_token_here",
        "LISTMONK_TXTOOL": "True",
        "LISTMONK_URL": "http://localhost:8080",
        "OPENAPI_CLIENT_ID": "",
        "OPENAPI_PASSWORD": "adminpassword",
        "OPENAPI_USERNAME": "admin"
      }
    }
  }
}
```

Alternatively, connect to a pre-deployed Streamable-HTTP instance by `url`:

```json
{
  "mcpServers": {
    "listmonk-mcp": {
      "url": "http://localhost:8000/listmonk-mcp/mcp"
    }
  }
}
```

Deploying the Streamable-HTTP server via Docker:

```bash
docker run -d \
  --name listmonk-mcp-mcp \
  -p 8000:8000 \
  -e TRANSPORT=streamable-http \
  -e HOST=0.0.0.0 \
  -e PORT=8000 \
  -e MCP_TOOL_MODE=condensed \
  -e LISTMONK_CAMPAIGNSTOOL=True \
  -e LISTMONK_IMPORTSTOOL=True \
  -e LISTMONK_LISTSTOOL=True \
  -e LISTMONK_MEDIATOOL=True \
  -e LISTMONK_SUBSCRIBERSTOOL=True \
  -e LISTMONK_TEMPLATESTOOL=True \
  -e LISTMONK_TOKEN=your_bearer_token_here \
  -e LISTMONK_TXTOOL=True \
  -e LISTMONK_URL=http://localhost:8080 \
  -e OPENAPI_CLIENT_ID="" \
  -e OPENAPI_PASSWORD=adminpassword \
  -e OPENAPI_USERNAME=admin \
  knucklessg1/listmonk-api:mcp
```

_Auto-generated from the code-read env surface (`MCP_TOOL_MODE` + package vars) — do not edit._
<!-- MCP-CONFIG-EXAMPLES:END -->

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

<!-- ENV-VARS-TABLE:START -->

#### Package environment variables

| Variable | Example | Description |
|----------|---------|-------------|
| `HOST` | `0.0.0.0` |  |
| `PORT` | `8000` |  |
| `TRANSPORT` | `stdio` | options: stdio, streamable-http, sse |
| `ENABLE_OTEL` | `True` |  |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | `http://localhost:8080/api/public/otel` |  |
| `OTEL_EXPORTER_OTLP_PUBLIC_KEY` | `pk-...` |  |
| `OTEL_EXPORTER_OTLP_SECRET_KEY` | `sk-...` |  |
| `OTEL_EXPORTER_OTLP_PROTOCOL` | `http/protobuf` |  |
| `AUTH_TYPE` | — |  |
| `EUNOMIA_TYPE` | `none` | options: none, embedded, remote |
| `EUNOMIA_POLICY_FILE` | `mcp_policies.json` |  |
| `EUNOMIA_REMOTE_URL` | `http://eunomia-server:8000` |  |
| `OIDC_BASE_URL` | — |  |
| `OPENAPI_USERNAME` | `admin` |  |
| `OPENAPI_PASSWORD` | `adminpassword` |  |
| `OPENAPI_CLIENT_ID` | — | OAuth client id for OpenAPI tool import |
| `OPENAPI_CLIENT_SECRET` | — | OAuth client secret for OpenAPI tool import |
| `LISTMONK_URL` | `http://localhost:8080` |  |
| `LISTMONK_TOKEN` | `your_bearer_token_here` |  |
| `LISTMONK_CAMPAIGNSTOOL` | `True` |  |
| `LISTMONK_IMPORTSTOOL` | `True` |  |
| `LISTMONK_LISTSTOOL` | `True` |  |
| `LISTMONK_MEDIATOOL` | `True` |  |
| `LISTMONK_SUBSCRIBERSTOOL` | `True` |  |
| `LISTMONK_TEMPLATESTOOL` | `True` |  |
| `LISTMONK_TXTOOL` | `True` |  |

#### Inherited agent-utilities variables (apply to every connector)

| Variable | Example | Description |
|----------|---------|-------------|
| `MCP_TOOL_MODE` | `condensed` | Tool surface: `condensed` | `verbose` | `both` |
| `MCP_ENABLED_TOOLS` | — | Comma-separated tool allow-list |
| `MCP_DISABLED_TOOLS` | — | Comma-separated tool deny-list |
| `MCP_ENABLED_TAGS` | — | Comma-separated tag allow-list |
| `MCP_DISABLED_TAGS` | — | Comma-separated tag deny-list |
| `MCP_CLIENT_AUTH` | — | Outbound MCP auth (`oidc-client-credentials` for fleet calls) |
| `OIDC_CLIENT_ID` | — | OIDC client id (service-account auth) |
| `OIDC_CLIENT_SECRET` | — | OIDC client secret (service-account auth) |
| `DEBUG` | `False` | Verbose logging |
| `PYTHONUNBUFFERED` | `1` | Unbuffered stdout (recommended in containers) |
| `MCP_URL` | `http://localhost:8000/mcp` | URL of the MCP server the agent connects to |
| `PROVIDER` | `openai` | LLM provider for the agent |
| `MODEL_ID` | `gpt-4o` | Model id for the agent |
| `ENABLE_WEB_UI` | `True` | Serve the AG-UI web interface |

_26 package + 14 inherited variable(s). Auto-generated from `.env.example` + the shared agent-utilities set — do not edit._
<!-- ENV-VARS-TABLE:END -->


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

Pick the extra that matches what you want to run:

| Extra | Installs | Use when |
|-------|----------|----------|
| `listmonk-api[mcp]` | Slim MCP server only (`agent-utilities[mcp]` — FastMCP/FastAPI) | You only run the **MCP server** (smallest install / image) |
| `listmonk-api[agent]` | Full agent runtime (`agent-utilities[agent,logfire]` — Pydantic AI + the epistemic-graph engine) | You run the **integrated agent** |
| `listmonk-api[all]` | Everything (`mcp` + `agent` + `logfire`) | Development / both surfaces |

```bash
# MCP server only (recommended for tool hosting — slim deps)
uv pip install "listmonk-api[mcp]"

# Full agent runtime (Pydantic AI + epistemic-graph engine)
uv pip install "listmonk-api[agent]"

# Everything (development)
uv pip install "listmonk-api[all]"      # or: python -m pip install "listmonk-api[all]"
```

### Container images (`:mcp` vs `:agent`)

One multi-stage `docker/Dockerfile` builds two right-sized images, selected by `--target`:

| Image tag | Build target | Contents | Entrypoint |
|-----------|--------------|----------|------------|
| `knucklessg1/listmonk-api:mcp` | `--target mcp` | `listmonk-api[mcp]` — **slim**, no engine/`pydantic-ai`/`dspy`/`llama-index`/`tree-sitter` | `listmonk-mcp` |
| `knucklessg1/listmonk-api:latest` | `--target agent` (default) | `listmonk-api[agent]` — **full** agent runtime + epistemic-graph engine | `listmonk-agent` |

```bash
docker build --target mcp   -t knucklessg1/listmonk-api:mcp    docker/   # slim MCP server
docker build --target agent -t knucklessg1/listmonk-api:latest docker/   # full agent
```

`docker/mcp.compose.yml` runs the slim `:mcp` server; `docker/agent.compose.yml` runs the
agent (`:latest`) with a co-located `:mcp` sidecar.

### Knowledge-graph database (`epistemic-graph`)

The **full agent** (`[agent]` / `:latest`) embeds the **epistemic-graph** engine (pulled in
transitively via `agent-utilities[agent]`). For production — or to share one knowledge graph
across multiple agents — run **epistemic-graph as its own database container** and point the
agent at it instead of embedding it. Deployment recipes (single-node + Raft HA), connection
config, and the full database architecture (with diagrams) are documented in the
[epistemic-graph deployment guide](https://knuckles-team.github.io/epistemic-graph/deployment/).
The slim `[mcp]` server does **not** require the database.

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
