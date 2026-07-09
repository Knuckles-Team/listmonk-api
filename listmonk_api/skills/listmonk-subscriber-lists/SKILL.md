---
name: listmonk-subscriber-lists
skill_type: skill
description: >-
  Audience management on Listmonk via the listmonk-api MCP server — manage
  subscription lists and the subscribers on them with the domain-typed tools
  (not raw HTTP). Use when the agent must create/read/edit a mailing list, read
  or create subscribers, read the subscribers of a list, or bulk-import
  subscribers from a file. Do NOT use for building/sending campaigns (use
  listmonk-campaign-management) or one-off transactional mail (use
  listmonk-transactional-messaging).
license: MIT
tags: [listmonk, subscribers, lists, audience, import, mcp]
metadata:
  author: Genius
  version: '0.1.0'
---
# Listmonk Subscriber & List Management

Domain-typed access to Listmonk **subscription lists** and **subscribers** — the
audience a campaign targets. Prefer these tools over raw calls; they carry the
opt-in/consent conventions and return list/subscriber-shaped records.

## When to use
- Create / read / edit subscription lists (public/private, single/double opt-in).
- Read or create subscribers; read the subscribers of a specific list.
- Bulk-import subscribers from a file and track import status/logs.

## When NOT to use
- Building, previewing, or sending campaigns → `listmonk-campaign-management`.
- One-off per-subscriber mail from a template → `listmonk-transactional-messaging`.
- Bulk KG ingestion → the `listmonk_ingest` tool (`entity="lists"` / `"subscribers"`).

## Prerequisites & environment
Connect via the `mcp-client` skill against the **`listmonk-api`** MCP server.

| Variable | Required | Notes |
|----------|----------|-------|
| `LISTMONK_URL` | ✅ | Base URL, e.g. `http://localhost:8080` |
| `LISTMONK_TOKEN` | ✅ | API token (`user:token` or admin token) |

`MCP_TOOL_MODE` (`condensed`|`verbose`|`both`) selects the condensed vs. verbose surface.

## Tools & actions
Prefer the **condensed** tools; each takes `action` + a `params_json` **JSON string**.

| Condensed tool | Actions |
|----------------|---------|
| `listmonk_lists` | `get_lists`, `get_list`, `create_list`, `edit_list` |
| `listmonk_subscribers` | `get_subscribers`, `get_subscriber`, `get_subscribers_from_list`, `create_subscriber` |
| `listmonk_imports` | `get_subscriber_import_status`, `get_subscriber_import_logs`, `import_subscribers`, `delete_subscriber_import` |

### Key parameters
- `create_list`: `name`, `type` (`public`|`private`), `optin` (`single`|`double`), `tags`.
- `edit_list`: `list_id` + any of `name`/`type`/`optin`/`tags`.
- `create_subscriber`: `email`, `name`, `status` (`enabled`|`disabled`|`blocklisted`),
  `lists` (list of list_ids), `attribs` (object), `preconfirm_subscriptions`.
- `get_subscribers` supports `list_id` (int or list of ints), `query`, `per_page`, `max_pages`.
- `get_subscribers_from_list` / `get_list` / `get_subscriber` take the numeric `list_id` / `subscriber_id`.

## Recipes (`params_json`)
Create a double opt-in public list:
```json
{"name":"Product Updates","type":"public","optin":"double","tags":["product"]}
```
Add a subscriber to two lists (pre-confirmed):
```json
{"email":"jane@example.com","name":"Jane Doe","status":"enabled","lists":[3,7],"preconfirm_subscriptions":true}
```
Read the subscribers of list 3:
```json
{"list_id":3}
```
Bulk-import subscribers (mode `subscribe`/`blocklist`):
```json
{"file":"email,name\njoe@example.com,Joe","mode":"subscribe","delim":",","lists":[3],"overwrite":true}
```

## Gotchas
- `params_json` is a **string** of JSON, not an object — serialize it.
- `optin: "double"` means new subscribers get a confirmation email unless
  `preconfirm_subscriptions` is set — respect consent; don't preconfirm without cause.
- `status: "blocklisted"` suppresses a subscriber from all sends globally.
- `get_subscribers` accepts a repeated `list_id` (pass a list) to filter across lists;
  unbounded reads are slow — set `per_page`/`max_pages`.
- Only one subscriber import runs at a time; check `get_subscriber_import_status`
  before starting another and `delete_subscriber_import` to clear a stuck one.

## Related
- `listmonk-campaign-management` — send a campaign to the lists managed here.
- `listmonk_ingest` (`entity="lists"`/`"subscribers"`) maps these to `:SubscriptionList`
  / `:Subscriber` nodes with `:subscribedToList` links in the knowledge graph.
