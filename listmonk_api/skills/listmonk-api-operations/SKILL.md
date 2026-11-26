---
name: listmonk-api-operations
skill_type: skill
description: >-
  Operate listmonk-api through its governed MCP and Arbora capabilities, including listmonk campaign management, listmonk subscriber lists, listmonk transactional messaging. Use when a request requires this provider's read, change, automation, ingestion, troubleshooting, or evidence workflows.
---

# Listmonk Api Operations

Use the provider's governed MCP tools through Arbora delegation.

## Workflow

1. Establish the verified GraphSession and tenant before discovery or retrieval.
2. Discover the current condensed tool surface; never assume a stale tool name or schema.
3. Prefer read-only inspection first. For changes, present impact and use the provider's
   dry-run or preview mode when available.
4. Execute mutations as fenced WorkItems so retries remain idempotent and auditable.
5. Ingest source data only through the signed connector preset and ChangeEnvelope path.
6. Verify the durable result and its trace/evidence before reporting completion.

## Safety contract

- Never persist credentials, endpoints, raw personal identifiers, hostnames, or local paths.
- Resolve TLS trust and verification from environment/configuration; never hardcode bypasses.
- Treat unknown ACL, tenant, schema, or tool-contract state as a hard failure.
- Require explicit approval for destructive, externally visible, or irreversible actions.
- Keep runtime traces policy-scoped and privacy-sanitized.

## Steps

1. Confirm the tool surface by reading the [workflow catalog](references/catalog.md) with `cat references/catalog.md`. Verify the workflow you need is listed there.
2. Open the matching skill, for example `listmonk-campaign-management`, and read its Tools table. Verify every tool and action you plan to call is named in it.
3. Run read-only inspection first, for example `listmonk_campaigns` with `action=get_campaigns`. Verify the ids you will change exist in the result.
4. For a change, present the impact and execute one mutating action, for example `listmonk_lists` with `action=create_list`. Verify the response echoes the changed object.
5. Re-read the object with the matching get action, for example `get_campaign` with `campaign_id`. Verify it matches the intended state before reporting completion.

## Failure recovery

| Failure | Cause | Recovery |
|---------|-------|----------|
| Unknown tool or action | Stale name or wrong tool mode | Re-read the Tools table of the matching skill and call the exact listed action with a `params_json` JSON string. |
| 401 or connection error | `LISTMONK_URL` or `LISTMONK_TOKEN` missing or wrong | Set both variables to the right instance and token, then call `get_lists` with `per_page=1` to confirm access. |
| Destructive action blocked | No explicit approval | Obtain explicit approval naming the ids, then call the delete action again with those ids. |

## Specialized workflows

Read [the workflow catalog](references/catalog.md) only when the request needs a
provider-specific procedure, parameter map, script, or reference asset.
