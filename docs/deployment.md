# Deployment

<!-- BEGIN GENERATED: deployment-options -->
## Deployment Options

`listmonk-api` supports local stdio, a loopback-only development listener, a
least-privilege stdio container, and a remote authenticated HTTPS boundary.
Provider endpoint, credential, selector, identity, and trust material are supplied
at runtime through `AgentConfig`; none is stored in this repository.

### Installed stdio process

```json
{
  "mcpServers": {
    "listmonk": {
      "command": "listmonk-mcp",
      "args": [],
      "env": {"MCP_TOOL_MODE": "intent"}
    }
  }
}
```

### Loopback development listener

```bash
listmonk-mcp --transport streamable-http --host 127.0.0.1 --port 8000
```

Do not expose this listener beyond loopback. Network deployments require direct TLS
or an explicitly trusted TLS-terminating ingress, configured authentication, exact
`MCP_ALLOWED_HOSTS`, and an exact trusted-proxy CIDR policy.

### Least-privilege local container

```bash
docker run -i --rm \
  --read-only \
  --cap-drop=ALL \
  --security-opt=no-new-privileges \
  --pids-limit=256 \
  --tmpfs /tmp:rw,noexec,nosuid,nodev,size=64m \
  -e TRANSPORT=stdio \
  registry.example.invalid/listmonk-api@sha256:<digest> listmonk-mcp
```

The operator projects the selected AgentConfig profile into the process at runtime;
the image remains immutable and contains no environment connection profile.

### Remote authenticated HTTPS endpoint

```json
{
  "mcpServers": {
    "listmonk": {"url": "https://service.example.invalid/mcp"}
  }
}
```

Store the real remote URL, outbound identity reference, and TLS-profile reference in
`AgentConfig`, not in MCP client JSON or documentation.
<!-- END GENERATED: deployment-options -->

This page covers running `listmonk-api` as a long-lived service: the transports, the
companion A2A agent, a Docker Compose stack, putting it behind a Caddy reverse proxy,
and giving it a DNS name with Technitium. To provision the **Listmonk instance** it
connects to, see [Backing Platform](platform.md).

> `listmonk-api` ships both an **MCP server** (console script `listmonk-mcp`) and an
> **A2A agent server** (console script `listmonk-agent`). The MCP server is the typed,
> deterministic tool surface; the agent server is a Pydantic-AI graph that calls those
> tools over an MCP connection.

## Run the MCP server

The transport is selected with `--transport` (or the `TRANSPORT` env var):

=== "stdio (default)"

    ```bash
    listmonk-mcp
    ```
    For IDE / desktop MCP clients that launch the server as a subprocess.

=== "streamable-http"

    ```bash
    listmonk-mcp --transport streamable-http --host 0.0.0.0 --port 8000
    ```
    A network server with a `/health` endpoint and `/mcp` route.

=== "sse"

    ```bash
    listmonk-mcp --transport sse --host 0.0.0.0 --port 8000
    ```

Health check (HTTP transports):

```bash
curl -s http://localhost:8000/health        # {"status":"OK"}
```

## Configuration (environment)

`listmonk-api` is configured entirely from the environment. The **required** connection
set:

| Var | Default | Meaning |
|---|---|---|
| `LISTMONK_URL` | `http://localhost:8080` | Base URL of the Listmonk instance |
| `LISTMONK_TOKEN` | `""` | Bearer / API token for authorization |
| `LISTMONK_USERNAME` | `""` | Username for basic auth (when token is empty) |
| `LISTMONK_PASSWORD` | `""` | Password for basic auth (when token is empty) |
| `HOST` | `0.0.0.0` | Bind address (HTTP transports) |
| `PORT` | `8000` | Bind port (HTTP transports) |
| `TRANSPORT` | `stdio` | `stdio`, `streamable-http`, or `sse` |

Each tool module can be toggled with `LISTMONK_<MODULE>TOOL` (for example
`LISTMONK_CAMPAIGNSTOOL`, `LISTMONK_SUBSCRIBERSTOOL`), all enabled by default. The full
set — including telemetry (OTEL) and access-governance (Eunomia / OIDC) variables — is
documented in
[`.env.example`](https://github.com/Knuckles-Team/listmonk-api/blob/main/.env.example).
Copy it to `.env` and populate only what you use.

## Docker Compose

The repo ships [`docker/mcp.compose.yml`](https://github.com/Knuckles-Team/listmonk-api/blob/main/docker/mcp.compose.yml).
It reads a sibling `.env` and publishes the HTTP server:

```yaml
services:
  listmonk-api-mcp:
    image: example/listmonk-api@sha256:<digest>
    container_name: listmonk-api-mcp
    hostname: listmonk-api-mcp
    restart: always
    env_file:
      - .env
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
```

```bash
cp .env.example .env          # then edit LISTMONK_* values
docker compose -f docker/mcp.compose.yml up -d
docker compose -f docker/mcp.compose.yml logs -f
```

## Run the A2A agent server

The agent server (console script `listmonk-agent`) is a Pydantic-AI graph that connects
to the MCP server and exposes an optional web interface (AG-UI) and terminal interface.
It is published on port `9004` by convention and is wired to the MCP server with
`MCP_URL`.

```bash
export LISTMONK_URL=https://listmonk.yourdomain.com
export LISTMONK_TOKEN=your-bearer-token

# Point the agent at a running MCP server
listmonk-agent \
  --provider openai --model-id gpt-4o \
  --host 0.0.0.0 --port 9004 \
  --mcp-url http://listmonk-api-mcp:8000/mcp
```

The repo ships
[`docker/agent.compose.yml`](https://github.com/Knuckles-Team/listmonk-api/blob/main/docker/agent.compose.yml),
which runs the MCP server and the agent together on one network so the agent reaches the
MCP server by container name:

```yaml
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

  listmonk-api-agent:
    image: example/listmonk-api@sha256:<digest>
    container_name: listmonk-api-agent
    hostname: listmonk-api-agent
    restart: always
    depends_on:
      - listmonk-api-mcp
    env_file:
      - ../.env
    command: ["listmonk-agent"]
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
```

```bash
docker compose -f docker/agent.compose.yml up -d
```

## Behind a Caddy reverse proxy

Expose the HTTP server on a hostname with automatic TLS. Add to your `Caddyfile`:

```caddy
# Internal (self-signed) — homelab .example.invalid zone
listmonk-api.example.invalid {
    tls internal
    reverse_proxy listmonk-api-mcp:8000
}
```

```caddy
# Public — automatic Let's Encrypt
listmonk-api.example.com {
    reverse_proxy listmonk-api-mcp:8000
}
```

Reload Caddy:

```bash
docker compose -f services/caddy/compose.yml exec caddy caddy reload --config /etc/caddy/Caddyfile
```

## DNS with Technitium

Point the hostname at the host running Caddy. Via the Technitium API:

```bash
curl -s "http://technitium.example.invalid:5380/api/zones/records/add" \
  --data-urlencode "token=$TECHNITIUM_DNS_TOKEN" \
  --data-urlencode "domain=listmonk-api.example.invalid" \
  --data-urlencode "zone=arpa" \
  --data-urlencode "type=A" \
  --data-urlencode "ipAddress=192.0.2.10" \
  --data-urlencode "ttl=3600"
```

…or add an **A record** `listmonk-api.example.invalid → <caddy-host-ip>` in the Technitium web
console (`http://technitium.example.invalid:5380`). The ecosystem
[`technitium-dns-mcp`](https://knuckles-team.github.io/technitium-dns-mcp/) automates
this as a tool.

## Register with an MCP client

Add to your client's `mcp_config.json`:

```json
{
  "mcpServers": {
    "listmonk-api": {
      "command": "uvx",
      "args": ["--from", "listmonk-api", "listmonk-mcp"],
      "env": {
        "LISTMONK_URL": "https://listmonk.yourdomain.com",
        "LISTMONK_TOKEN": "your-bearer-token"
      }
    }
  }
}
```

For a remote HTTP server, point the client at `http://listmonk-api.example.invalid/mcp` instead.
