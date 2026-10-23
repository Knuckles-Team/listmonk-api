# CONN-LISTMONK-API-CONNECTOR-CONTENT — Design and implementation plan

Governing spec: [spec.md](spec.md).

## Architecture

`pyproject.toml` declares `listmonk-mcp` as the connector identity. `create_mcp_server` resolves the packaged content of `listmonk_api` from it.
