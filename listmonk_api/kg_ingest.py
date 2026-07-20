"""Native epistemic-graph ingestion for Listmonk records and documents.

All writes use the required ``agent_utilities.knowledge_graph.memory.native_ingest``
primitive. Nodes use canonical ``node_type`` and edges use canonical ``relationship``;
nodes and edges commit in one native transaction. Missing engine dependencies, rejected
records, conflicts, and transaction failures propagate as ``NativeIngestError``.
"""

from __future__ import annotations

import logging
from typing import Any

from agent_utilities.knowledge_graph.memory.native_ingest import (
    ingest_documents as _native_ingest_documents,
)
from agent_utilities.knowledge_graph.memory.native_ingest import (
    ingest_entities as _native_ingest_entities,
)

logger = logging.getLogger("listmonk_api.kg")

_SOURCE = "listmonk-api"
_DOMAIN = "listmonk"


def ingest_entities(
    entities: list[dict[str, Any]],
    relationships: list[dict[str, Any]] | None = None,
    *,
    source: str = _SOURCE,
    domain: str = _DOMAIN,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int]:
    """Write canonical typed nodes and relationships in one native transaction."""
    return _native_ingest_entities(
        entities, relationships, source=source, domain=domain, client=client, graph=graph
    )


def ingest_documents(
    documents: list[dict[str, Any]],
    *,
    source: str = _SOURCE,
    domain: str = _DOMAIN,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int]:
    """Write text records as canonical Document nodes."""
    return _native_ingest_documents(
        documents, source=source, domain=domain, client=client, graph=graph
    )


# --- record mappers (records -> entity/document dicts) ------------------------


def _as_list(records: Any) -> list[dict[str, Any]]:
    if records is None:
        return []
    if isinstance(records, dict):
        # A single record, or a {"results": [...]} / {"data": {...}} envelope.
        if "results" in records and isinstance(records["results"], list):
            return records["results"]
        data = records.get("data")
        if isinstance(data, dict) and isinstance(data.get("results"), list):
            return data["results"]
        if isinstance(data, list):
            return data
        return [records]
    if isinstance(records, list):
        return [r for r in records if isinstance(r, dict)]
    return []


def ingest_campaigns(
    campaigns: Any,
    *,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int]:
    """Map Listmonk campaign records → :Campaign nodes (+ :SubscriptionList /
    :EmailTemplate links) and their bodies → :Document nodes, and ingest both."""
    entities: list[dict[str, Any]] = []
    relationships: list[dict[str, Any]] = []
    documents: list[dict[str, Any]] = []
    document_relationships: list[dict[str, Any]] = []
    for camp in _as_list(campaigns):
        cid = camp.get("id")
        if cid is None:
            continue
        node_id = f"listmonk:campaign:{cid}"
        entities.append(
            {
                "id": node_id,
                "node_type": "Campaign",
                "name": camp.get("name"),
                "subject": camp.get("subject"),
                "campaignStatus": camp.get("status"),
                "fromEmail": camp.get("from_email"),
                "sendAt": camp.get("send_at"),
                "created_at": camp.get("created_at"),
                "updated_at": camp.get("updated_at"),
                "externalToolId": str(cid),
            }
        )
        for lst in camp.get("lists") or []:
            lid = lst.get("id") if isinstance(lst, dict) else lst
            if lid is None:
                continue
            entities.append(
                {
                    "id": f"listmonk:list:{lid}",
                    "node_type": "SubscriptionList",
                    "name": lst.get("name") if isinstance(lst, dict) else None,
                }
            )
            relationships.append(
                {
                    "source": node_id,
                    "target": f"listmonk:list:{lid}",
                    "relationship": "targetsList",
                }
            )
        tid = camp.get("template_id")
        if tid:
            entities.append({"id": f"listmonk:template:{tid}", "node_type": "EmailTemplate"})
            relationships.append(
                {
                    "source": node_id,
                    "target": f"listmonk:template:{tid}",
                    "relationship": "usesTemplate",
                }
            )
        body = camp.get("body")
        if body:
            doc_id = f"listmonk:campaign:{cid}:body"
            documents.append(
                {
                    "id": doc_id,
                    "text": body,
                    "title": camp.get("subject") or camp.get("name"),
                    "campaign_id": str(cid),
                }
            )
            document_relationships.append(
                {"source": node_id, "target": doc_id, "relationship": "hasBody"}
            )
    ent_res = ingest_entities(entities, relationships, client=client, graph=graph)
    doc_res = (
        _native_ingest_documents(
            documents,
            document_relationships,
            source=_SOURCE,
            domain=_DOMAIN,
            client=client,
            graph=graph,
        )
        if documents
        else {"nodes": 0, "edges": 0}
    )
    return _merge(ent_res, doc_res)


def ingest_lists(
    lists: Any,
    *,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int]:
    """Map Listmonk list records → :SubscriptionList nodes and ingest."""
    entities: list[dict[str, Any]] = []
    for lst in _as_list(lists):
        lid = lst.get("id")
        if lid is None:
            continue
        entities.append(
            {
                "id": f"listmonk:list:{lid}",
                "node_type": "SubscriptionList",
                "name": lst.get("name"),
                "listType": lst.get("type"),
                "optinType": lst.get("optin"),
                "subscriber_count": lst.get("subscriber_count"),
                "created_at": lst.get("created_at"),
                "updated_at": lst.get("updated_at"),
                "externalToolId": str(lid),
            }
        )
    return ingest_entities(entities, client=client, graph=graph)


def ingest_subscribers(
    subscribers: Any,
    *,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int]:
    """Map Listmonk subscriber records → :Subscriber nodes (+ :subscribedToList links)."""
    entities: list[dict[str, Any]] = []
    relationships: list[dict[str, Any]] = []
    for sub in _as_list(subscribers):
        sid = sub.get("id")
        if sid is None:
            continue
        node_id = f"listmonk:subscriber:{sid}"
        entities.append(
            {
                "id": node_id,
                "node_type": "Subscriber",
                "name": sub.get("name"),
                "email": sub.get("email"),
                "subscriberStatus": sub.get("status"),
                "created_at": sub.get("created_at"),
                "updated_at": sub.get("updated_at"),
                "externalToolId": str(sid),
            }
        )
        for lst in sub.get("lists") or []:
            lid = lst.get("id") if isinstance(lst, dict) else lst
            if lid is None:
                continue
            relationships.append(
                {
                    "source": node_id,
                    "target": f"listmonk:list:{lid}",
                    "relationship": "subscribedToList",
                }
            )
    return ingest_entities(entities, relationships, client=client, graph=graph)


def _merge(a: dict[str, int], b: dict[str, int]) -> dict[str, int]:
    return {
        "nodes": a["nodes"] + b["nodes"],
        "edges": a["edges"] + b["edges"],
    }
