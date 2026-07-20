# Installation

`listmonk-api` is a standard Python package and a prebuilt container image. Choose the
path that matches how you intend to run it.

## Requirements

- **Python 3.11–3.14**.
- A reachable **Listmonk instance** — see [Backing Platform](platform.md) to deploy one
  locally with Docker.

## From PyPI (recommended)

```bash
pip install listmonk-api
```

### Optional extras

The base install ships the API client and the MCP server runtime. Install the extra for
what you need:

| Extra | Install | Pulls in |
|---|---|---|
| _(base)_ | `pip install listmonk-api` | `agent-utilities[mcp]` — FastMCP MCP-server runtime |
| `agent` | `pip install "listmonk-api[agent]"` | Pydantic-AI agent + Logfire tracing |
| `all` | `pip install "listmonk-api[all]"` | Everything above (MCP + agent + Logfire) |

```bash
# Typical: run the MCP server and the A2A agent
pip install "listmonk-api[all]"
```

## From source

```bash
git clone https://github.com/Knuckles-Team/listmonk-api.git
cd listmonk-api
pip install -e ".[all]"          # editable install with every extra
```

With [`uv`](https://docs.astral.sh/uv/):

```bash
uv pip install -e ".[all]"
uv run listmonk-mcp
```

## Prebuilt Docker image

A multi-stage runtime image is published on every release (entrypoint `listmonk-mcp`):

```bash
docker pull example/listmonk-api@sha256:<digest>

docker run --rm -i \
  -e LISTMONK_URL=https://listmonk.yourdomain.com \
  -e LISTMONK_TOKEN=your-bearer-token \
  example/listmonk-api@sha256:<digest>        # stdio transport (default)
```

For an HTTP server with a published port and the agent server, see
[Deployment](deployment.md).

## Verify the install

```bash
listmonk-mcp --help
python -c "import listmonk_api; print(listmonk_api.__version__)"
```

## Next steps

- **[Deployment](deployment.md)** — run it as a long-lived MCP server and agent behind Caddy + DNS.
- **[Usage](usage.md)** — call the tools, the API, and the agent CLI.
- **[Configuration](deployment.md#configuration-environment)** — every environment variable.
