# CONN-LISTMONK-API-CONNECTOR-CONTENT — Requirements

Governing spec: [spec.md](spec.md).

Each row is one requirement. A row names the file it touches and the test that proves it. The generator sets each row's state in `status.json`.

| ID | Requirement | Acceptance |
|---|---|---|
| `CONN-LISTMONK-API-CONNECTOR-CONTENT-R001` | **Default content.** `pyproject.toml` declares `listmonk-mcp` as the single `scion_sdk.connector` entry point. The server lists the packaged `skill://` and `ontology://` resources and the packaged prompts with no `content=` argument. Proving test: `tests/test_default_content_surfaces.py`. Caller chain: the scion_sdk.connector entry point listmonk-mcp in pyproject.toml resolves to listmonk_api/__init__.py::connector, which the listmonk-mcp console script (scion_sdk.cli:serve) serves; the packaged skills and ontology directories are listmonk_api/skills and listmonk_api/ontology, and register_prompts in listmonk_api/mcp_server.py (line 460) adds the prompts. Shape: serve the packaged skills, ontology and prompts through scion_sdk.mcp.content.ConnectorContent.for_package with no content= argument; no test lists resources today, so add a served resources/list and prompts/list check next to tests/test_fleet_name.py. | `resources/list` includes `skill://` and `ontology://`; `prompts/list` includes each packaged prompt. Planned test: `tests/test_default_content_surfaces.py::test_default_content_surfaces`. |
