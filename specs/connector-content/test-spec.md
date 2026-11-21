# CONN-LISTMONK-API-CONNECTOR-CONTENT — Test specification

Governing spec: [spec.md](spec.md).

| Test ID | Requirement | Proving test | Expected observation |
|---|---|---|---|
| T-001 | `CONN-LISTMONK-API-CONNECTOR-CONTENT-R001` | `tests/test_default_content_surfaces.py` | The listings include the packaged skills, ontology and prompts. |
| T-002 | `CONN-LISTMONK-API-CONNECTOR-CONTENT-R002` | `tests/test_pack_extends_core.py` | No core term is redeclared and no retired IRI base remains. |
