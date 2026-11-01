# CONN-LISTMONK-API — Implementation plan

Governing spec: [spec.md](spec.md). Rows: [requirements.md](requirements.md).

## Summary

`BaseApiClient` in `listmonk_api/api/api_client_base.py` owns the HTTP session and its headers. `get_client` in `listmonk_api/auth.py` builds the client from settings. The fix reuses both. It adds one helper, `build_authorization`, and no second client. listmonk API users authenticate with `Authorization: token <user>:<token>`. It rejects `Bearer` with 403. `build_authorization` builds the value from the token and username. `get_client` reads `LISTMONK_USERNAME` and passes it to the client.

## Technical Context

- **Language/Version**: Python 3.14 (floor 3.12)
- **Primary Dependencies**: scion-sdk, fastmcp
- **Storage**: N/A; the connector stores nothing
- **Testing**: pytest; the proof level each row names
- **Target Platform**: Linux containers
- **Project Type**: connector (MCP server)
- **Performance Goals**: N/A
- **Constraints**: one tool per API operation; shared capabilities come from the SDK
- **Scale/Scope**: 4 rows

## Constitution Check

- One owner per concept: pass. The connector owns one external system's calls, mappings and tools only.
- Connectors depend on the SDK and are called through arbora: pass.
- No ratchets: pass. The rows add no suppression.

## Project Structure

```text
listmonk_api/api/api_client_base.py  existing
pyproject.toml  existing
```

## Phase 0: Research

No unknowns. Each row names the code it touches.

## Phase 1: Design

### Interfaces and data model

No tool, wire, or schema change. The settings keys are unchanged.
`LISTMONK_USERNAME` is now read. The token is never logged.

### Live integration path

An MCP tool calls an `Api` method. The method calls `get` or `post` on the session.
`BaseApiClient.__init__` sets the header at `api_client_base.py` through `build_authorization`.
`get_client` at `auth.py:20` passes the username.

### Quality and release gates

Run `pytest tests/test_token_auth.py` with a faked session. No network is used.
Run `pipelines-hook spec-standard` and `pipelines-hook spec-status --write`.

### Risks, alternatives, and decisions

Accepting a combined `user:token` keeps existing deployments that stored that shape working.

## Phase 2: Task approach

`tasks.md` holds one task line per row, producer first.

## Complexity Tracking

None. The constitution check passed.

## Build contract

The repository pre-commit hooks apply: `ruff-format`, `connector-standard`, `secrets`, `tests-fast`. Each row names its proving test. No suppression and no duplicate implementation.

## Production caller chain

1. `CONN-LISTMONK-API-R001`: the listmonk-mcp console script (pyproject.toml scripts, scion_sdk.cli:serve) loads the scion_sdk.connector entry point listmonk_api/__init__.py::connector, which registers listmonk_api/mcp_server.py tool functions that call the client built by listmonk_api/auth.py::get_client.
2. `CONN-LISTMONK-API-R002`: the listmonk-mcp console script (pyproject.toml scripts, scion_sdk.cli:serve) loads the scion_sdk.connector entry point listmonk_api/__init__.py::connector, which registers listmonk_api/mcp_server.py tool functions that call the client built by listmonk_api/auth.py::get_client.
3. `CONN-LISTMONK-API-R003`: the listmonk-mcp console script (pyproject.toml scripts, scion_sdk.cli:serve) loads the scion_sdk.connector entry point listmonk_api/__init__.py::connector, which registers listmonk_api/mcp_server.py tool functions that call the client built by listmonk_api/auth.py::get_client.
4. `CONN-LISTMONK-API-R004`: the scion_sdk.connector entry point listmonk-mcp in pyproject.toml resolves to listmonk_api/__init__.py::connector, and listmonk_api/kg_ingest.py::ingest_entities and ingest_documents submit through the listmonk_api/kg_ingest.py::_BINDING IngestBinding (line 28) reached by the listmonk_ingest tool in listmonk_api/mcp_server.py.

## Cross-repo seams

none
