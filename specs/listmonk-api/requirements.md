# CONN-LISTMONK-API — Requirements

Governing spec: [spec.md](spec.md).

Each row is one requirement. A row names the file it touches and the test that proves it.

| ID | Requirement | Acceptance |
|---|---|---|
| `CONN-LISTMONK-API-R001` | **Token scheme.** The client must send `Authorization: token <user>:<token>` and never `Bearer`, in `listmonk_api/api/api_client_base.py`. | `tests/test_token_auth.py::test_header_uses_token_scheme_with_username` and `::test_header_never_uses_bearer` must pass. |
| `CONN-LISTMONK-API-R002` | **Credential shapes.** A token that already reads `user:token` must be sent as given. A token with no username must be sent as `token <token>`. | `tests/test_token_auth.py::test_combined_user_token_is_used_as_given` and `::test_token_without_username_is_sent_as_given` must pass. |
| `CONN-LISTMONK-API-R003` | **Wiring.** `get_client` in `listmonk_api/auth.py:20` must pass `LISTMONK_USERNAME` to the client. | `tests/test_token_auth.py::test_auth_client_reads_listmonk_username` must observe the header through `get_client`. |
| `CONN-LISTMONK-API-R004` | **Fleet name.** `pyproject.toml` declares `listmonk-mcp` as the single `agent_connector_sdk.connector` entry point. The content pack, the manifest `connector`, the fingerprints and the ingest binding all carry `listmonk-mcp`. Proving test: `tests/test_fleet_name.py::test_connector_name_is_the_fleet_name`. | Every connector name in the package is `listmonk-mcp`. |
