# Concept Registry — listmonk-api

> **Prefix**: `CONCEPT:LM-*`
> **Version**: 0.6.0
> **Bridge**: [`CONCEPT:AU-ECO.messaging.native-backend-abstraction`](https://github.com/Knuckles-Team/agent-connector-sdk/blob/main/docs/concepts.md) (Unified Toolkit Ingestion)

---

## Project-Specific Concepts

| Concept ID | Name | Description |
|------------|------|-------------|
| `CONCEPT:LM-OS.governance.lm` | Listmonk Campaigns Operations | MCP tool domain `listmonk_campaigns` — Action-routed dynamic tool registration |
| `CONCEPT:LM-OS.governance.lm-2` | Listmonk Imports Operations | MCP tool domain `listmonk_imports` — Action-routed dynamic tool registration |
| `CONCEPT:LM-OS.governance.lm-3` | Listmonk Lists Operations | MCP tool domain `listmonk_lists` — Action-routed dynamic tool registration |
| `CONCEPT:LM-OS.governance.lm-4` | Listmonk Media Operations | MCP tool domain `listmonk_media` — Action-routed dynamic tool registration |
| `CONCEPT:LM-OS.governance.lm-5` | Listmonk Subscribers Operations | MCP tool domain `listmonk_subscribers` — Action-routed dynamic tool registration |
| `CONCEPT:LM-OS.governance.lm-6` | Listmonk Templates Operations | MCP tool domain `listmonk_templates` — Action-routed dynamic tool registration |
| `CONCEPT:LM-OS.governance.lm-7` | Listmonk Tx Operations | MCP tool domain `listmonk_tx` — Action-routed dynamic tool registration |

## Cross-Project References (from agent-connector-sdk)

| Concept ID | Name | Origin |
|------------|------|--------|
| `CONCEPT:AU-ECO.messaging.native-backend-abstraction` | Unified Toolkit Ingestion | agent-connector-sdk |
| `CONCEPT:AU-ORCH.adapter.hot-cache-invalidation` | Confidence-Gated Router | agent-connector-sdk |
| `CONCEPT:AU-OS.config.secrets-authentication` | Prompt Injection Defense | agent-connector-sdk |
| `CONCEPT:AU-OS.state.cognitive-scheduler-preemption` | Cognitive Scheduler | agent-connector-sdk |
| `CONCEPT:AU-OS.governance.reactive-multi-axis-budget` | Guardrail Engine | agent-connector-sdk |
| `CONCEPT:AU-OS.governance.wasm-micro-agent-sandbox` | Audit Logging | agent-connector-sdk |
| `CONCEPT:AU-KG.query.object-graph-mapper` | Knowledge Graph Core | agent-connector-sdk |

## Synergy with agent-connector-sdk

This project integrates with `agent-connector-sdk` via `CONCEPT:AU-ECO.messaging.native-backend-abstraction` (Unified Toolkit Ingestion). The `listmonk_api` MCP server registers its tools with the agent-connector-sdk FastMCP middleware, enabling automatic discovery, telemetry, and Knowledge Graph ingestion of all LM-* concepts.
