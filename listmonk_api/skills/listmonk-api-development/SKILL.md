---
name: listmonk-api-development
skill_type: skill
description: >-
  Develop and verify listmonk-api as a connector-owned package while preserving
  its SDK entry point, action-routed tools, Listmonk authentication boundary,
  packaged content, and source-backed spec-delivery publication.
---

# Listmonk API Development

Use this skill for changes to the `listmonk-api` connector. The package owns
Listmonk API calls, mappings, MCP tools, and connector content; it does not own
the connector SDK, Arbora admission, the shared Pages renderer, or Pipelines
hooks.

## Repository map and runtime boundary

- `listmonk_api/__init__.py` creates the SDK `Connector` with `ListmonkAPI`,
  `get_client`, and `listmonk_api.mcp_server` as its tool module. Preserve this
  wiring when changing a tool or client.
- `listmonk_api/mcp_server.py` registers the action-routed domains
  `subscribers`, `lists`, `imports`, `campaigns`, `media`, `templates`, `tx`,
  and `ingest`, plus prompt registration. The domain API classes live under
  `listmonk_api/api/` and are composed by `listmonk_api/api_client.py`.
- `listmonk_api/auth.py` reads `LISTMONK_URL`, `LISTMONK_TOKEN`, and optional
  `LISTMONK_USERNAME` through the SDK setting boundary and resolves the named
  `listmonk` TLS profile from `LISTMONK_TLS_PROFILE` or
  `LISTMONK_TLS_PROFILE_REF`.
- `listmonk_api/ontology/`, `listmonk_api/prompts/`, and
  `listmonk_api/skills/` are packaged connector content. The package-data table
  in `pyproject.toml` includes `skills/**`, `prompts/**`, `ontology/**`, and
  `connectors/**`; inspect a built wheel when changing these files.
- The only declared current console script is `listmonk-mcp`, provided by
  `scion_sdk.cli:serve`; `python -m listmonk_api` delegates to the SDK
  runner. The tracked `docker/compose.yml` and older docs still mention a
  `listmonk-agent` profile, but current `pyproject.toml` declares no such script
  or `agent_server.py`. Do not invent that runtime or rewrite it as part of a
  Pages/skill change.

## Rapid delivery: the 5-minute contract

1. Read the owning `specs/` row and this repository's `AGENTS.md` before editing.
2. Inspect the active client/tool path and its focused tests before changing API
   behavior, auth, ontology content, or packaged skills.
3. Prefer the smallest connector-owned change. Preserve action names, parameter
   schemas, SDK `Connector` wiring, Listmonk auth/TLS verification, and package
   data declarations unless the owning requirement changes them.
4. Run the focused tests through the narrow test-slot wrapper, then run the
   repository pre-commit and pre-push gates without bypasses.
5. For public packaged content, update the patch version and `uv.lock` together;
   inspect the built wheel for the new skill.
6. Treat Pages as a separate proof: after the exact main SHA has a successful
   Pages run, check `/spec-delivery/`, its `index.html`, and `snapshot.json` over
   HTTPS and record the revision from the snapshot.

## Focused development commands

From the repository root:

```bash
uv sync --locked

/var/tmp/arbora-delivery/scale/run-narrow-test-slot.sh \
  uv run --locked --extra test pytest -q \
    tests/test_init.py \
    tests/test_init_dynamics.py \
    tests/test_action_discovery.py \
    tests/test_auth_and_server.py \
    tests/test_mcp_server.py \
    tests/test_publication_workflow.py

uvx pre-commit run --all-files
uvx pre-commit run --all-files --hook-stage pre-push
```

These checks cover SDK server construction, runtime entry points, action
discovery, auth/tool behavior, and the Pages/release contract. Do not replace
them with a live Listmonk call or a credential-bearing test.

## Pages and package publication

`.github/workflows/pages.yml` is the one Pages caller. It invokes the shared
Pipelines `pages_pipeline.yml@main` with `content_source: docs` and the version 1
`.github/spec-dashboard.json` source declaration for `specs/*/status.json`.
Keep manual dispatch and the docs/spec/config/workflow path filters. The old
direct `mkdocs gh-deploy` publisher must not be restored because it would compete
with the shared dashboard build.

After a merge, verify the exact main SHA in the successful Pages run and probe:

```bash
curl -fsSI https://knuckles-team.github.io/listmonk-api/
curl -fsSI https://knuckles-team.github.io/listmonk-api/spec-delivery/
curl -fsSI https://knuckles-team.github.io/listmonk-api/spec-delivery/index.html
curl -fsS https://knuckles-team.github.io/listmonk-api/spec-delivery/snapshot.json
```

Keep `.github/workflows/pipeline.yml` on the shared `connector: true` and
`render_connector: true` flags. Central generation owns generated connector
manifests and release container artifacts; preserve this package's existing
runtime/auth/port semantics and inspect generated output before making claims.

## Change discipline

- Keep Listmonk API calls, request models, ontology mappings, and MCP schemas
  under this repository's `CONN-LISTMONK-API-*` boundary. SDK transport and
  central renderer behavior belong to their owner repositories.
- Use `LISTMONK_URL`, `LISTMONK_TOKEN`, and `LISTMONK_USERNAME` only in injected
  runtime configuration; never print or commit their values. Preserve TLS
  certificate verification and the named profile path.
- For mutations, inspect current state first, require operator approval where
  the existing connector procedure calls for it, and verify the result. Keep KG
  ingestion opt-in and preserve its provenance/tenant contract.
- Keep generated status changes and central promotion with the Pipelines/status
  owner. Do not claim Pages or public package results from a local build.
