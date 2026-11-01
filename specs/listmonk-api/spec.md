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

## Scope and interfaces

In scope: the rows of [requirements.md](requirements.md). Out of scope: the SDK modules and the engine, which own the shared capabilities.

## User Scenarios & Testing

### User Story 1 - listmonk API-user authentication (Priority: P1)

The connector must authenticate to listmonk as an API user.

**Acceptance Scenarios**:

1. **Given** the connector is configured, **When** the behaviour of row `CONN-LISTMONK-API-R001` (token scheme) is exercised, **Then** `tests/test_token_auth.py::test_header_uses_token_scheme_with_username` and `::test_header_never_uses_bearer` must pass.
2. **Given** the connector is configured, **When** the behaviour of row `CONN-LISTMONK-API-R002` (credential shapes) is exercised, **Then** `tests/test_token_auth.py::test_combined_user_token_is_used_as_given` and `::test_token_without_username_is_sent_as_given` must pass.
3. **Given** the connector is configured, **When** the behaviour of row `CONN-LISTMONK-API-R003` (wiring) is exercised, **Then** `tests/test_token_auth.py::test_auth_client_reads_listmonk_username` must observe the header through `get_client`.

### Edge Cases

- If `CONN-LISTMONK-API-R001` is not met, its proving test fails: token scheme.
- If `CONN-LISTMONK-API-R002` is not met, its proving test fails: credential shapes.
- If `CONN-LISTMONK-API-R003` is not met, its proving test fails: wiring.

## Requirements

- **FR-001**: Token scheme. Rows: `CONN-LISTMONK-API-R001`.
- **FR-002**: Credential shapes. Rows: `CONN-LISTMONK-API-R002`.
- **FR-003**: Wiring. Rows: `CONN-LISTMONK-API-R003`.
- **FR-004**: Fleet name. Rows: `CONN-LISTMONK-API-R004`.

## Success Criteria

- **SC-001**: `tests/test_token_auth.py::test_header_uses_token_scheme_with_username` and `::test_header_never_uses_bearer` must pass. Rows: `CONN-LISTMONK-API-R001`.
- **SC-002**: `tests/test_token_auth.py::test_combined_user_token_is_used_as_given` and `::test_token_without_username_is_sent_as_given` must pass. Rows: `CONN-LISTMONK-API-R002`.
- **SC-003**: `tests/test_token_auth.py::test_auth_client_reads_listmonk_username` must observe the header through `get_client`. Rows: `CONN-LISTMONK-API-R003`.
- **SC-004**: Every connector name in the package is `listmonk-mcp`. Rows: `CONN-LISTMONK-API-R004`.

## Assumptions

- The external system is reachable with operator-supplied credentials.
- The SDK and engine contracts the rows cite are at the floors declared in `pyproject.toml`.

## Traceability

| Label | Rows | Design section | Test ID | Evidence |
|---|---|---|---|---|
| FR-001 | `CONN-LISTMONK-API-R001` | [plan.md](plan.md) | T-001 | [test-spec.md](test-spec.md) |
| FR-002 | `CONN-LISTMONK-API-R002` | [plan.md](plan.md) | T-002 | [test-spec.md](test-spec.md) |
| FR-003 | `CONN-LISTMONK-API-R003` | [plan.md](plan.md) | T-003 | [test-spec.md](test-spec.md) |
| FR-004 | `CONN-LISTMONK-API-R004` | [plan.md](plan.md) | T-004 | [test-spec.md](test-spec.md) |
