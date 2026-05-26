# Concept Registry — listmonk-api

> **Prefix**: `CONCEPT:LM-*`
> **Version**: 0.6.0
> **Bridge**: [`CONCEPT:ECO-4.0`](../../agent-utilities/docs/concepts.md) (Unified Toolkit Ingestion)

---

## Project-Specific Concepts

| Concept ID | Name | Description |
|------------|------|-------------|
| `CONCEPT:LM-001` | Listmonk Campaigns Operations | MCP tool domain `listmonk_campaigns` — Action-routed dynamic tool registration |
| `CONCEPT:LM-002` | Listmonk Imports Operations | MCP tool domain `listmonk_imports` — Action-routed dynamic tool registration |
| `CONCEPT:LM-003` | Listmonk Lists Operations | MCP tool domain `listmonk_lists` — Action-routed dynamic tool registration |
| `CONCEPT:LM-004` | Listmonk Media Operations | MCP tool domain `listmonk_media` — Action-routed dynamic tool registration |
| `CONCEPT:LM-005` | Listmonk Subscribers Operations | MCP tool domain `listmonk_subscribers` — Action-routed dynamic tool registration |
| `CONCEPT:LM-006` | Listmonk Templates Operations | MCP tool domain `listmonk_templates` — Action-routed dynamic tool registration |
| `CONCEPT:LM-007` | Listmonk Tx Operations | MCP tool domain `listmonk_tx` — Action-routed dynamic tool registration |

## Cross-Project References (from agent-utilities)

| Concept ID | Name | Origin |
|------------|------|--------|
| `CONCEPT:ECO-4.0` | Unified Toolkit Ingestion | agent-utilities |
| `CONCEPT:ORCH-1.2` | Confidence-Gated Router | agent-utilities |
| `CONCEPT:OS-5.1` | Prompt Injection Defense | agent-utilities |
| `CONCEPT:OS-5.2` | Cognitive Scheduler | agent-utilities |
| `CONCEPT:OS-5.3` | Guardrail Engine | agent-utilities |
| `CONCEPT:OS-5.4` | Audit Logging | agent-utilities |
| `CONCEPT:KG-2.0` | Knowledge Graph Core | agent-utilities |

## Synergy with agent-utilities

This project integrates with `agent-utilities` via `CONCEPT:ECO-4.0` (Unified Toolkit Ingestion). The `listmonk_api` MCP server registers its tools with the agent-utilities FastMCP middleware, enabling automatic discovery, telemetry, and Knowledge Graph ingestion of all LM-* concepts.
