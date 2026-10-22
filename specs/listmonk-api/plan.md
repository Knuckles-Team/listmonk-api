# CONN-LISTMONK-API — Design and implementation plan

Governing spec: [spec.md](spec.md).

## Existing system and reuse

`BaseApiClient` in `listmonk_api/api/api_client_base.py` owns the HTTP session and its headers.
`get_client` in `listmonk_api/auth.py` builds the client from settings.
The fix reuses both. It adds one helper, `build_authorization`, and no second client.

## Architecture

listmonk API users authenticate with `Authorization: token <user>:<token>`.
It rejects `Bearer` with 403. `build_authorization` builds the value from the token and username.
`get_client` reads `LISTMONK_USERNAME` and passes it to the client.

## Interfaces and data model

No tool, wire, or schema change. The settings keys are unchanged.
`LISTMONK_USERNAME` is now read. The token is never logged.

## Live integration path

An MCP tool calls an `Api` method. The method calls `get` or `post` on the session.
`BaseApiClient.__init__` sets the header at `api_client_base.py` through `build_authorization`.
`get_client` at `auth.py:20` passes the username.

## Quality and release gates

Run `pytest tests/test_token_auth.py` with a faked session. No network is used.
Run `pipelines-hook spec-standard` and `pipelines-hook spec-status --write`.

## Risks, alternatives, and decisions

Accepting a combined `user:token` keeps existing deployments that stored that shape working.
