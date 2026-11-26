---
name: listmonk-campaign-management
skill_type: skill
description: >-
  Listmonk email campaigns via the listmonk-api MCP server: list, read, preview, create, schedule or run, and stat campaigns. Use to build a newsletter against explicit list_ids or change campaign status. Do NOT use for subscribers or lists (listmonk-subscriber-lists) or one-off mail (listmonk-transactional-messaging).
license: MIT
tags: [listmonk, campaign, newsletter, email, mcp]
metadata:
  author: Knuckles-Team
  version: '0.1.0'
---
# Listmonk Campaign Management

Scope: Email-campaign operations on Listmonk via the listmonk-api MCP server — list, read, preview, create, schedule/run, and stat campaigns with the domain-typed tool (not raw HTTP). Use when the agent must build a newsletter campaign against explicit list_ids, transition a campaign's status (draft → scheduled → running → paused/cancelled), preview rendered content, or read running stats. Do NOT use for managing subscribers or lists (use listmonk-subscriber-lists) or for one-off per-recipient mail (use listmonk-transactional-messaging).

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
| `LISTMONK_URL` | ✅ | Base URL, e.g. `http://localhost:8080` |
| `LISTMONK_TOKEN` | ✅ | API token (`user:token` or admin token) |

`MCP_TOOL_MODE` (`condensed`|`verbose`|`both`) selects the condensed surface
(used below) vs. the one-to-one verbose tools.

## Steps

1. Resolve the target lists with `listmonk_lists` (`action=get_lists`). Verify the list_ids you will target appear in the result.
2. Create the campaign with `listmonk_campaigns` (`action=create_campaign`, `params_json` with `name`, `subject`, `lists`, `from_email`, `type`, `body`). Verify the response returns a `campaign_id`.
3. Render it with `listmonk_campaigns` (`action=get_campaign_preview`, `campaign_id`). Verify the content and `from_email` are correct before any send.
4. Schedule or start it with `action=set_campaign_status` (`campaign_id`, `data` holding `status`). Verify `get_campaign` reports the new status.
5. Watch a running campaign with `action=get_campaign_stats` (`campaign_id`). Verify the sent counter increases.

## Failure recovery

| Failure | Cause | Recovery |
|---------|-------|----------|
| 401 or connection error | `LISTMONK_URL` or `LISTMONK_TOKEN` missing or wrong | Set both variables to the right instance and token, then call `get_campaigns` with `per_page=1` to confirm access. |
| Create rejected | Payload used `send_type` instead of `type`, or `params_json` was an object | Resend with the key `type` set to `regular` or `optin` and `params_json` serialized as a JSON string. |
| Stats empty | The campaign is not running, so no running stats exist | Read `get_campaign` for its status and call `set_campaign_status` to `running` only after preview, then call `get_campaign_stats` again. |

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
{"name":"July Newsletter","subject":"What's new in July","lists":[3,7],"from_email":"news@example.com","type":"regular","content_type":"html","body":"<h1>Hello</h1><p>...</p>"}
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
