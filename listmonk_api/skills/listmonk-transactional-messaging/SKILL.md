---
name: listmonk-transactional-messaging
skill_type: skill
description: >-
  Listmonk transactional email and templates via the listmonk-api MCP server: send a one-off message to one subscriber from a template, and list, preview, set default or delete templates. Do NOT use for bulk newsletters (listmonk-campaign-management) or audience management (listmonk-subscriber-lists).
license: MIT
tags: [listmonk, transactional, template, email, mcp]
metadata:
  author: Knuckles-Team
  version: '0.1.0'
---
# Listmonk Transactional Messaging & Templates

Scope: Transactional email + template operations on Listmonk via the listmonk-api MCP server — send a one-off, per-recipient message rendered from a template, and manage the email templates it uses, with the domain-typed tools (not raw HTTP). Use when the agent must send a receipt/notification/password-reset style mail to a single subscriber, or list/read/preview/set-default/delete templates. Do NOT use for bulk newsletters (use listmonk-campaign-management) or for managing the audience (use listmonk-subscriber-lists).

Domain-typed access to Listmonk **transactional messages** and **templates** —
one-off, per-recipient mail (receipts, notifications, resets) rendered from a
template, plus the template lifecycle. Prefer these tools over raw calls.

## When to use
- Send a single transactional email to one subscriber from a `template_id`.
- List / read / preview templates; set a default template; delete a template.

## When NOT to use
- Bulk newsletters / broadcasts to lists → `listmonk-campaign-management`.
- Managing subscribers or lists → `listmonk-subscriber-lists`.
- Bulk KG ingestion of campaigns → the `listmonk_ingest` tool.

## Prerequisites & environment
Connect via the `mcp-client` skill against the **`listmonk-api`** MCP server.

| Variable | Required | Notes |
|----------|----------|-------|
| `LISTMONK_URL` | ✅ | Base URL, e.g. `http://localhost:8080` |
| `LISTMONK_TOKEN` | ✅ | API token (`user:token` or admin token) |

The template must be of the **transactional** type in Listmonk for `listmonk_tx` to use it.
`MCP_TOOL_MODE` (`condensed`|`verbose`|`both`) selects the condensed vs. verbose surface.

## Steps

1. List templates with `listmonk_templates` (`action=get_templates`). Verify a transactional template exists and note its `template_id`.
2. Render it with `action=get_template_preview` (`template_id`). Verify the placeholders you plan to fill appear in the output.
3. Send the message with `listmonk_tx` (`action=transactional_message`, `params_json` with `template_id`, one of `subscriber_email` or `subscriber_id`, and `data`). Verify the call returns success.
4. To change the default, call `action=set_default_template` (`template_id`) only after confirming impact on future campaigns. Verify `get_template` shows it as default.

## Failure recovery

| Failure | Cause | Recovery |
|---------|-------|----------|
| 401 or connection error | `LISTMONK_URL` or `LISTMONK_TOKEN` missing or wrong | Set both variables to the right instance and token, then call `get_templates` to confirm access. |
| Message not rendered | `template_id` points at a campaign template, not a transactional one | Call `get_templates`, choose a transactional template, and resend `transactional_message` with that `template_id`. |
| Recipient rejected | Both or neither of `subscriber_email` and `subscriber_id` were given | Resend with exactly one recipient key. |

## Tools & actions
Prefer the **condensed** tools; each takes `action` + a `params_json` **JSON string**.

| Condensed tool | Actions |
|----------------|---------|
| `listmonk_tx` | `transactional_message` |
| `listmonk_templates` | `get_templates`, `get_template`, `get_template_preview`, `set_default_template`, `delete_template` |

### Key parameters
- `transactional_message`: `template_id` (required), one of `subscriber_email` /
  `subscriber_id`, optional `data` (object of template vars), `headers`,
  `content_type`, `attachments` (list of `{name, content}` objects).
- `get_template` / `get_template_preview` / `set_default_template` / `delete_template`
  take the numeric `template_id`.

## Recipes (`params_json`)
Send a transactional message to one subscriber with template vars:
```json
{"template_id":5,"subscriber_email":"jane@example.com","data":{"order_id":"A-1007","total":"$42.00"}}
```
Preview a template's rendered output:
```json
{"template_id":5}
```
Set the default campaign template:
```json
{"template_id":2}
```

## Gotchas
- `params_json` is a **string** of JSON, not an object — serialize it.
- Provide exactly one recipient key — `subscriber_email` **or** `subscriber_id`.
- `template_id` must reference a **transactional** template; a campaign/visual
  template will not render via `listmonk_tx`.
- `data` keys must match the template's placeholders, else they render empty.
- Deleting or changing the default template affects future campaigns — confirm first.

## Related
- `listmonk-campaign-management` — bulk campaigns can also reference a `template_id`.
- `listmonk-subscriber-lists` — resolve the recipient (`subscriber_id`/`email`) here.
- In the KG, templates surface as `:EmailTemplate` nodes linked from campaigns via
  `:usesTemplate` (populated by `listmonk_ingest`).
