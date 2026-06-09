# Usage — MCP / API / Agent

`listmonk-api` exposes the same capability three ways: as **MCP tools** an agent calls,
as a **Python API** (`ListmonkAPI`) you import, and as an **A2A agent**. The complete
tool surface and the API structure are in [Overview](overview.md).

## As an MCP server

Once [deployed](deployment.md), the server registers action-routed tool modules. Each
module groups related operations to keep the LLM context lean while preserving granular,
tag-based permissions.

| Tool module | Toggle env var | Operations |
|---|---|---|
| `listmonk_subscribers` | `LISTMONK_SUBSCRIBERSTOOL` | `get_subscribers`, `get_subscriber`, `get_subscribers_from_list`, `create_subscriber` |
| `listmonk_lists` | `LISTMONK_LISTSTOOL` | `get_lists`, `get_list`, `create_list`, `edit_list` |
| `listmonk_campaigns` | `LISTMONK_CAMPAIGNSTOOL` | `get_campaigns`, `get_campaign`, `get_campaign_preview`, `get_campaign_stats`, `create_campaign`, `set_campaign_status`, `delete_campaign` |
| `listmonk_media` | `LISTMONK_MEDIATOOL` | `get_media`, `upload_media`, `delete_media` |
| `listmonk_templates` | `LISTMONK_TEMPLATESTOOL` | `get_templates`, `get_template`, `get_template_preview`, `set_default_template`, `delete_template` |
| `listmonk_imports` | `LISTMONK_IMPORTSTOOL` | `get_subscriber_import_status`, `get_subscriber_import_logs`, `import_subscribers`, `delete_subscriber_import` |
| `listmonk_tx` | `LISTMONK_TXTOOL` | `transactional_message` |

Example agent prompts that map onto these tools:

- *"List the active subscriber lists"* → `listmonk_lists`
- *"Create a subscriber for jane@example.com on list 1"* → `listmonk_subscribers`
- *"Show the stats for campaign 12"* → `listmonk_campaigns`

## As a Python API

`ListmonkAPI` aggregates dedicated sub-API managers (subscribers, lists, campaigns,
media, templates, imports, transactional) behind one unified client.

```python
from listmonk_api import ListmonkAPI

client = ListmonkAPI(
    url="https://listmonk.yourdomain.com",
    token="your-bearer-token",
)

# Reads
lists = client.get_lists()
for lst in lists:
    print(f"List: {lst.name} (ID: {lst.id})")

campaigns = client.get_campaigns()
subscribers = client.get_subscribers()
```

### Writes

```python
new_subscriber = client.create_subscriber(
    email="jane@example.com",
    name="Jane Doe",
    status="enabled",
    lists=[1],
)
print(f"Created: {new_subscriber['name']}")

client.create_campaign(name="Weekly Update", subject="This week", lists=[1])
```

## As an A2A agent

The agent server (console script `listmonk-agent`) is a Pydantic-AI graph that calls the
MCP tools on your behalf, with an optional web interface and terminal interface.

```bash
export LISTMONK_URL="https://listmonk.yourdomain.com"
export LISTMONK_TOKEN="your-bearer-token"

# Interactive agent against a running MCP server
listmonk-agent --provider openai --model-id gpt-4o
```

The agent connects to the MCP server via `--mcp-url` (env: `MCP_URL`), so it can drive
the same subscriber, list, campaign, and template operations conversationally. See
[Deployment](deployment.md#run-the-a2a-agent-server) for the combined Compose stack.
