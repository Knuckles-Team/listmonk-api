# CONN-LISTMONK-API — listmonk API-user authentication

## Outcome

The connector must authenticate to listmonk as an API user.
Every request must carry `Authorization: token <user>:<token>`.

## Scope and owner

The `listmonk-api` repository owns listmonk API calls and their authentication header.
The shared connector SDK owns transport, TLS, and error types.
The shared pipelines repository owns quality gates and delivery rendering.

Component: Connector integration
Code: ../../listmonk_api/api/api_client_base.py ../../listmonk_api/auth.py ../../tests/test_token_auth.py

## Non-goals

This specification grants no service access and creates no credentials.
The connector must not log the token.

## Why a new spec

The repository holds no local spec. The search of `specs/` found only the template.
No other owner states the listmonk authentication scheme.

## Requirements

See [requirements.md](requirements.md), [plan.md](plan.md), and [test-spec.md](test-spec.md).
