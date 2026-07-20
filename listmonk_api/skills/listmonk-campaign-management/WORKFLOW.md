# Listmonk Campaign Management

Email-campaign operations on Listmonk via the listmonk-api MCP server — list, read, preview, create, schedule/run, and stat campaigns with the domain-typed tool (not raw HTTP). Use when the agent must build a newsletter campaign against explicit list_ids, transition a campaign's status (draft → scheduled → running → paused/cancelled), preview rendered content, or read running stats. Do NOT use for managing subscribers or lists (use listmonk-subscriber-lists) or for one-off per-recipient mail (use listmonk-transactional-messaging).

# Listmonk Campaign Management

Domain-typed access to Listmonk **campaigns** for newsletter/broadcast email.
Prefer these tools over raw calls — they carry the campaign field conventions
(the create payload key is `type`, not `send_type`) and return campaign-shaped
records.

## When to use
- List / read campaigns; preview rendered content; read running stats.
- Create a campaign against explicit `lists` (list_ids) with subject + body.
- Transition status: `scheduled`, `running`, `paused`, `cancelled`.

## When NOT to use
- Managing subscribers, subscription lists, or imports → `listmonk-subscriber-lists`.
- One-off per-subscriber mail rendered from a template → `listmonk-transactional-messaging`.
- Bulk KG ingestion of campaigns → the `listmonk_ingest` tool (`entity="campaigns"`),
  not the operational recipes below.

## Prerequisites & environment
Connect via the `mcp-client` skill against the **`listmonk-api`** MCP server.

| Variable | Required | Notes |
|----------|----------|-------|
| `LISTMONK_URL` | ✅ | Base URL, e.g. `[configured-endpoint]` |
| `LISTMONK_TOKEN` | ✅ | API token (`user:token` or admin token) |

`MCP_TOOL_MODE` (`condensed`|`verbose`|`both`) selects the condensed surface
(used below) vs. the one-to-one verbose tools.

## Tools & actions
Prefer the **condensed** tool; it takes `action` + a `params_json` **JSON string**
whose keys are passed straight to the client method.

| Condensed tool | Actions |
|----------------|---------|
| `listmonk_campaigns` | `get_campaigns`, `get_campaign`, `get_campaign_preview`, `get_campaign_stats`, `create_campaign`, `set_campaign_status`, `delete_campaign` |

### Key parameters
- `campaign_id` — required for get_campaign / preview / stats / set_campaign_status / delete.
- `create_campaign` fields: `name`, `subject`, `lists` (list of list_ids), `from_email`,
  `type` (`regular`|`optin`), `content_type` (`html`|`richtext`|`plain`|`markdown`),
  `body`, optional `template_id`, `send_at`, `tags`, `media` (uploaded media ids).
- `set_campaign_status` takes `campaign_id` + `data:{"status": ...}`.
- `get_campaigns` supports `order_by` (name/status/created_at/updated_at), `order`
  (ASC/DESC), `per_page`, `max_pages`.

## Recipes (`params_json`)
List the newest campaigns:
```json
{"order_by":"created_at","order":"DESC","per_page":25,"max_pages":1}
```
Create an HTML campaign against two lists:
```json
{"name":"July Newsletter","subject":"What's new in July","lists":[3,7],"from_email":"[REDACTED_EMAIL]","type":"regular","content_type":"html","body":"<h1>Hello</h1><p>...</p>"}
```
Schedule it to run:
```json
{"campaign_id":42,"data":{"status":"scheduled"}}
```
Preview rendered content / read live stats:
```json
{"campaign_id":42}
```

## Gotchas
- `params_json` is a **string** of JSON, not an object — serialize it.
- The create payload key is **`type`** (regular/optin), not `send_type`; the model
  maps it via a pydantic alias, so pass `type`.
- Always preview and confirm `from_email` + `lists` before `set_campaign_status` to
  `scheduled`/`running` — a running campaign starts sending immediately.
- `get_campaign_stats` only returns data for a **running** campaign
  (`/campaigns/{id}/running/stats`).
- `media` is a list of already-uploaded media **ids** (upload first via `listmonk_media`).

## Related
- `listmonk-subscriber-lists` — the audience (lists + subscribers) a campaign targets.
- `listmonk-transactional-messaging` — per-recipient mail from a template.
- `listmonk_ingest` (`entity="campaigns"`) pulls campaigns into the KG as `:Campaign`
  nodes (+ `:targetsList`/`:usesTemplate` links and `:Document` bodies).
