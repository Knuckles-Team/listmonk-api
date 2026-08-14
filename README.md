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

*Version: 2.1.0*

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

#### Condensed action-routed tools (`MCP_TOOL_MODE=condensed`)

| MCP Tool | Toggle Env Var | Description |
|----------|----------------|-------------|
| `listmonk_campaigns` | `LISTMONK_CAMPAIGNSTOOL` | Manage listmonk campaigns operations. |
| `listmonk_imports` | `LISTMONK_IMPORTSTOOL` | Manage listmonk imports operations. |
| `listmonk_ingest` | `LISTMONK_INGESTTOOL` | Natively ingest Listmonk records into epistemic-graph as typed nodes + documents. |
| `listmonk_lists` | `LISTMONK_LISTSTOOL` | Manage listmonk lists operations. |
| `listmonk_media` | `LISTMONK_MEDIATOOL` | Manage listmonk media operations. |
| `listmonk_subscribers` | `LISTMONK_SUBSCRIBERSTOOL` | Manage listmonk subscribers operations. |
| `listmonk_templates` | `LISTMONK_TEMPLATESTOOL` | Manage listmonk templates operations. |
| `listmonk_tx` | `LISTMONK_TXTOOL` | Manage listmonk tx operations. |

#### Verbose 1:1 API-mapped tools (`MCP_TOOL_MODE=verbose` or `both`)

<details>
<summary>28 per-operation tools — one per public API method (click to expand)</summary>

| MCP Tool | Toggle Env Var | Description |
|----------|----------------|-------------|
| `listmonk_create_campaign` | `LISTMONK_APITOOL` | Invoke the create_campaign operation. |
| `listmonk_create_list` | `LISTMONK_APITOOL` | Invoke the create_list operation. |
| `listmonk_create_subscriber` | `LISTMONK_APITOOL` | Invoke the create_subscriber operation. |
| `listmonk_delete_campaign` | `LISTMONK_APITOOL` | Invoke the delete_campaign operation. |
| `listmonk_delete_media` | `LISTMONK_APITOOL` | Invoke the delete_media operation. |
| `listmonk_delete_subscriber_import` | `LISTMONK_APITOOL` | Invoke the delete_subscriber_import operation. |
| `listmonk_delete_template` | `LISTMONK_APITOOL` | Invoke the delete_template operation. |
| `listmonk_edit_list` | `LISTMONK_APITOOL` | Invoke the edit_list operation. |
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
| `listmonk_set_campaign_status` | `LISTMONK_APITOOL` | Invoke the set_campaign_status operation. |
| `listmonk_set_default_template` | `LISTMONK_APITOOL` | Invoke the set_default_template operation. |
| `listmonk_transactional_message` | `LISTMONK_APITOOL` | Invoke the transactional_message operation. |
| `listmonk_upload_media` | `LISTMONK_APITOOL` | Invoke the upload_media operation. |

</details>

_8 action-routed tool(s) · 28 verbose 1:1 tool(s). Each is enabled unless its `<DOMAIN>TOOL` toggle is set false; `MCP_TOOL_MODE` selects the surface (**`intent` default** — the six verb-tools, granular set loaded on demand · `condensed` action-routed · `verbose` 1:1 · `both`). Auto-generated — do not edit._
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

> **Install the connector-focused `[mcp]` extra.** Examples use `listmonk-api[mcp]` to add
> FastMCP / FastAPI through `agent-utilities[mcp]`; the required Agent Utilities core
> still carries `epistemic-graph[full]`. The `[agent-runtime]` extra additionally
> enables model orchestration.

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
        "MCP_TOOL_MODE": "intent",
        "LISTMONK_CAMPAIGNSTOOL": "True",
        "LISTMONK_IMPORTSTOOL": "True",
        "LISTMONK_LISTSTOOL": "True",
        "LISTMONK_MEDIATOOL": "True",
        "LISTMONK_SUBSCRIBERSTOOL": "True",
        "LISTMONK_TEMPLATESTOOL": "True",
        "LISTMONK_TLS_PROFILE": "system",
        "LISTMONK_TXTOOL": "True",
        "LISTMONK_URL": "https://listmonk.example.invalid",
        "OPENAPI_PASSWORD": "adminpassword",
        "OPENAPI_USERNAME": "admin"
      }
    }
  }
}
```

Runtime references require an alias-aware launcher such as GraphOS. Other
launchers must omit those entries and inject the resolved values through their
own runtime secret boundary.

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
        "HOST": "127.0.0.1",
        "PORT": "8000",
        "MCP_TOOL_MODE": "intent",
        "LISTMONK_CAMPAIGNSTOOL": "True",
        "LISTMONK_IMPORTSTOOL": "True",
        "LISTMONK_LISTSTOOL": "True",
        "LISTMONK_MEDIATOOL": "True",
        "LISTMONK_SUBSCRIBERSTOOL": "True",
        "LISTMONK_TEMPLATESTOOL": "True",
        "LISTMONK_TLS_PROFILE": "system",
        "LISTMONK_TXTOOL": "True",
        "LISTMONK_URL": "https://listmonk.example.invalid",
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

Run a reviewed container image as a least-privilege stdio child (no
listener or published port):

```bash
docker run -i --rm \
  --read-only \
  --cap-drop=ALL \
  --security-opt=no-new-privileges \
  --pids-limit=256 \
  --tmpfs /tmp:rw,noexec,nosuid,nodev,size=64m \
  -e TRANSPORT=stdio \
  -e MCP_TOOL_MODE=intent \
  -e LISTMONK_CAMPAIGNSTOOL=True \
  -e LISTMONK_IMPORTSTOOL=True \
  -e LISTMONK_LISTSTOOL=True \
  -e LISTMONK_MEDIATOOL=True \
  -e LISTMONK_SUBSCRIBERSTOOL=True \
  -e LISTMONK_TEMPLATESTOOL=True \
  -e LISTMONK_TLS_PROFILE=system \
  -e LISTMONK_TXTOOL=True \
  -e LISTMONK_URL=https://listmonk.example.invalid \
  -e OPENAPI_PASSWORD=adminpassword \
  -e OPENAPI_USERNAME=admin \
  registry.example.invalid/listmonk-api@sha256:<digest> listmonk-mcp
```

For containerized network HTTP, supply an authenticated TLS ingress (or
direct server TLS), exact `MCP_ALLOWED_HOSTS`, and an exact trusted-proxy
CIDR policy through the operator-owned deployment profile. The generator
does not emit an unauthenticated non-loopback listener.

_Auto-generated from the code-read env surface (`MCP_TOOL_MODE` + package vars) — do not edit._
<!-- MCP-CONFIG-EXAMPLES:END -->

<!-- BEGIN GENERATED: additional-deployment-options -->
### Additional Deployment Options

`listmonk-api` can run as a local stdio process or container, or behind a remote
network boundary. The
[Deployment guide](https://knuckles-team.github.io/listmonk-api/deployment/) carries
the detailed transport contract.

- **Local container** — launch a reviewed immutable image as a least-privilege
  stdio child with no listener or published port.
- **Remote URL** — connect through an operator-supplied authenticated HTTPS
  ingress. Keep its URL, outbound identity references, trust profile, and exact
  `MCP_ALLOWED_HOSTS` in `AgentConfig`.
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
    image: example/listmonk-api@sha256:<digest>
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
    image: example/listmonk-api@sha256:<digest>
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

Detailed graph node architecture explanations, custom skill configurations, and agentic trace guides are available in [docs/deployment.md](docs/deployment.md).

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
| `OTEL_EXPORTER_OTLP_PUBLIC_KEY` | secret-injected |  |
| `OTEL_EXPORTER_OTLP_SECRET_KEY` | secret-injected |  |
| `OTEL_EXPORTER_OTLP_PROTOCOL` | `http/protobuf` |  |
| `AUTH_TYPE` | — |  |
| `EUNOMIA_TYPE` | `none` | options: none, embedded, remote |
| `EUNOMIA_POLICY_FILE` | `mcp_policies.json` |  |
| `EUNOMIA_REMOTE_URL` | `http://eunomia-server:8000` |  |
| `OIDC_BASE_URL` | — |  |
| `OPENAPI_USERNAME` | `admin` |  |
| `OPENAPI_PASSWORD` | secret-injected |  |
| `OPENAPI_CLIENT_ID` | — | OAuth client id for OpenAPI tool import |
| `OPENAPI_CLIENT_SECRET` | secret-injected | OAuth client secret for OpenAPI tool import |
| `LISTMONK_URL` | `https://listmonk.example.invalid` |  |
| `LISTMONK_TOKEN` | secret-injected |  |
| `LISTMONK_TLS_PROFILE` | `system` | Named outbound TLS policy from AgentConfig. Use a reference for runtime-only trust material; peer and hostname verification remain mandatory. |
| `LISTMONK_TLS_PROFILE_REF` | — |  |
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
| `MCP_TOOL_MODE` | `intent` | Tool surface: `intent` \| `condensed` \| `verbose` \| `both` |
| `MCP_ENABLED_TOOLS` | — | Comma-separated tool allow-list |
| `MCP_DISABLED_TOOLS` | — | Comma-separated tool deny-list |
| `MCP_ENABLED_TAGS` | — | Comma-separated tag allow-list |
| `MCP_DISABLED_TAGS` | — | Comma-separated tag deny-list |
| `MCP_CLIENT_AUTH` | — | Outbound MCP child auth: `oidc-client-credentials` \| `basic` \| `none` |
| `OIDC_CLIENT_ID` | — | OIDC client id (service-account auth) |
| `OIDC_CLIENT_SECRET_REF` | `secret://identity/oidc-client-secret` | Runtime secret reference for the OIDC service account |
| `MCP_BASIC_AUTH_USERNAME` | — | HTTP Basic username (`MCP_CLIENT_AUTH=basic`) |
| `MCP_BASIC_AUTH_PASSWORD_REF` | `secret://identity/mcp-basic-password` | Runtime secret reference for HTTP Basic auth (`MCP_CLIENT_AUTH=basic`) |
| `DEBUG` | `False` | Verbose logging |
| `PYTHONUNBUFFERED` | `1` | Unbuffered stdout (recommended in containers) |
| `MCP_URL` | `http://localhost:8000/mcp` | URL of the MCP server the agent connects to |
| `PROVIDER` | `openai` | LLM provider for the agent |
| `MODEL_ID` | `gpt-4o` | Model id for the agent |
| `ENABLE_WEB_UI` | `True` | Serve the AG-UI web interface |

_28 package + 16 inherited variable(s). Auto-generated from `.env.example` + the shared agent-utilities set — do not edit._
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
| `listmonk-api[mcp]` | Connector-focused MCP server (`agent-utilities[mcp]` — FastMCP/FastAPI + `epistemic-graph[full]`) | You only run the **MCP server** (smallest install / image) |
| `listmonk-api[agent]` | Agent runtime (`agent-utilities[agent-runtime,logfire]` — model orchestration + `epistemic-graph[full]`) | You run the **integrated agent** |
| `listmonk-api[all]` | Everything (`mcp` + `agent` + `logfire`) | Development / both surfaces |

```bash
# Connector-focused MCP server (includes the shared graph engine)
uv pip install "listmonk-api[mcp]"

# Agent runtime (adds model orchestration to the shared graph engine)
uv pip install "listmonk-api[agent]"

# Everything (development)
uv pip install "listmonk-api[all]"      # or: python -m pip install "listmonk-api[all]"
```

### Container images (`:mcp` vs `:agent`)

One multi-stage `docker/Dockerfile` builds two right-sized images, selected by `--target`:

| Image tag | Build target | Contents | Entrypoint |
|-----------|--------------|----------|------------|
| `example/listmonk-api:mcp` | `--target mcp` | `listmonk-api[mcp]` — **connector-focused**, includes `epistemic-graph[full]`; no model-orchestration stack | `listmonk-mcp` |
| `example/listmonk-api@sha256:<digest>` | `--target agent` (default) | `listmonk-api[agent]` — **agent runtime**, model orchestration + `epistemic-graph[full]` | `listmonk-agent` |

```bash
docker build --target mcp   -t example/listmonk-api:mcp    docker/   # connector-focused MCP server
docker build --target agent -t example/listmonk-api:agent-local docker/   # agent runtime
```

`docker/mcp.compose.yml` runs the connector-focused `:mcp` server; `docker/agent.compose.yml` runs the
agent (`immutable agent digest`) with a co-located `:mcp` sidecar.

### Knowledge-graph database (`epistemic-graph`)

Both `[mcp]` and `[agent]` carry the **epistemic-graph** engine through the required
Agent Utilities core dependency (`epistemic-graph[full]`). The `[mcp]` extra keeps
the server connector-focused; `[agent]` additionally enables model orchestration. Local
deployments can use the bundled engine. For production or shared state, run
**epistemic-graph as a dedicated database service** and configure the runtime to use it.
Deployment recipes (single-node + Raft HA), connection configuration, and architecture
diagrams are documented in the
[epistemic-graph deployment guide](https://knuckles-team.github.io/epistemic-graph/deployment/).

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

<img width="100%" height="180em" src="https://github-readme-stats.vercel.app/api?username=example&show_icons=true&hide_border=true&&count_private=true&include_all_commits=true" />

![GitHub followers](https://img.shields.io/github/followers/example)
![GitHub User's stars](https://img.shields.io/github/stars/example)

---

## Contribute

Contributions are welcome! Please ensure code quality by executing local checks before submitting pull requests:
- Format code using `ruff format .`
- Lint code using `ruff check .`
- Validate type-safety with `mypy .`
- Execute test suites using `pytest`


<!-- BEGIN agent-utilities-deployment (generated; do not edit between markers) -->

## Deploy with `agent-utilities-deployment`

Provision this package with the consolidated **`agent-utilities-deployment`**
workflow. It selects an installed-package, editable-source, or immutable-container
path; records only runtime secret and TLS-profile references in `AgentConfig`; and
runs doctor, registration, policy, observability, and rollback gates. Ask your agent
to **"deploy `listmonk-api` with agent-utilities-deployment"**.

| Install mode | Command |
|------|---------|
| Installed package | `uv tool install "listmonk-api[mcp]"`, then run `listmonk-mcp` |
| Editable source | `uv pip install -e ".[agent]"`, then run `listmonk-mcp` |
| Immutable container | deploy `registry.example.invalid/listmonk-api@sha256:<digest>` through the operator-selected orchestrator |

The repository embeds no deployment profile, credential value, certificate path, or
environment-specific endpoint. Supply those at runtime through `AgentConfig` and the
configured secret provider.

<!-- END agent-utilities-deployment -->

<!-- GOVERNED-CAPABILITY:START -->
## Governed capability contract

This package ships a compact canonical skill surface with specialist procedures
kept as referenced workflows. The current MCP tools, skill metadata,
`connector_manifest.yml`, ontology, mappings, shapes, fixtures, migrations,
tool-schema fingerprints, and certification metadata form one versioned
capability contract. Validate them together; do not rely on stale tool names or
historical per-task skill wrappers.

Runtime endpoints, credentials, certificate trust, tenant identity, retention,
and observability policy are deployment inputs and are never packaged values.
See [Configuration, trust, and privacy](docs/configuration.md) before enabling a
network transport, connector ingestion, GraphOS delegation, or trace export.
<!-- GOVERNED-CAPABILITY:END -->
