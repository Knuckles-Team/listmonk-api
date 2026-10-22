# CONN-LISTMONK-API — Test specification

Governing spec: [spec.md](spec.md).

| Test ID | Requirement | Level | Setup and input | Expected observation | Evidence |
|---|---|---|---|---|---|
| T-001 | `CONN-LISTMONK-API-R001` | Unit | Client built with token `abc` and username `arbora-mcp`. | The header reads `token arbora-mcp:abc`. | `tests/test_token_auth.py::test_header_uses_token_scheme_with_username` |
| T-002 | `CONN-LISTMONK-API-R001` | Unit | Same client. | The header does not start with `Bearer`. | `tests/test_token_auth.py::test_header_never_uses_bearer` |
| T-003 | `CONN-LISTMONK-API-R002` | Unit | Token `arbora-mcp:abc`. | The header carries it unchanged. | `tests/test_token_auth.py::test_combined_user_token_is_used_as_given` |
| T-004 | `CONN-LISTMONK-API-R002` | Unit | Token `abc`, no username. | The header reads `token abc`. | `tests/test_token_auth.py::test_token_without_username_is_sent_as_given` |
| T-005 | `CONN-LISTMONK-API-R003` | Integration | `get_client` with `LISTMONK_USERNAME` set. | The header reads `token arbora-mcp:abc`. | `tests/test_token_auth.py::test_auth_client_reads_listmonk_username` |

## Negative and boundary cases

An empty username with a bare token sends the bare token. No case sends `Bearer`.

## Quality and release proof

Run `pytest tests/test_token_auth.py`. Run `pipelines-hook spec-standard`.
