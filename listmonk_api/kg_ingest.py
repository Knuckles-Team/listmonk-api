"""Native epistemic-graph ingestion for Listmonk records and documents.

All writes use the required ``agent_utilities.knowledge_graph.memory.native_ingest``
primitive. Nodes use canonical ``node_type`` and edges use canonical ``relationship``;
nodes and edges commit in one native transaction. Missing engine dependencies, rejected
records, conflicts, and transaction failures propagate as ``NativeIngestError``.
"""

from __future__ import annotations

import logging
from typing import Any


logger = logging.getLogger("listmonk_api.kg")

_SOURCE = "listmonk-api"
_DOMAIN = "listmonk"


def ingest_entities(*args: object, **kwargs: object) -> object:
    """Write canonical typed nodes and relationships in one native transaction.

    SDK-GAP: Always raises now; see KnowledgeGraphIngestUnavailable.
    """
    _kg_unavailable("ingest_entities")


def ingest_documents(*args: object, **kwargs: object) -> object:
    """Write text records as canonical Document nodes.

    SDK-GAP: Always raises now; see KnowledgeGraphIngestUnavailable.
    """
    _kg_unavailable("ingest_documents")


# --- record mappers (records -> entity/document dicts) ------------------------


def _as_list_from_dict(records: dict[str, Any]) -> list[dict[str, Any]]:
    """Unwrap a single record, or a {"results": [...]} / {"data": {...}} envelope."""
    if "results" in records and isinstance(records["results"], list):
        return records["results"]
    data = records.get("data")
    if isinstance(data, dict) and isinstance(data.get("results"), list):
        return data["results"]
    if isinstance(data, list):
        return data
    return [records]


def _as_list(records: Any) -> list[dict[str, Any]]:
    if records is None:
        return []
    if isinstance(records, dict):
        return _as_list_from_dict(records)
    if isinstance(records, list):
        return [r for r in records if isinstance(r, dict)]
    return []


def _campaign_entity(camp: dict[str, Any], cid: Any, node_id: str) -> dict[str, Any]:
    """Build one campaign record's :Campaign entity dict."""
    return {
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


def _campaign_list_links(
    camp: dict[str, Any], node_id: str
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """:SubscriptionList entities + :targetsList relationships for a campaign's lists."""
    entities: list[dict[str, Any]] = []
    relationships: list[dict[str, Any]] = []
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
    return entities, relationships


def _campaign_template_link(
    camp: dict[str, Any], node_id: str
) -> tuple[dict[str, Any], dict[str, Any]] | tuple[None, None]:
    """The :EmailTemplate entity + :usesTemplate relationship, or (None, None)."""
    tid = camp.get("template_id")
    if not tid:
        return None, None
    entity = {"id": f"listmonk:template:{tid}", "node_type": "EmailTemplate"}
    relationship = {
        "source": node_id,
        "target": f"listmonk:template:{tid}",
        "relationship": "usesTemplate",
    }
    return entity, relationship


def _campaign_body_document(
    camp: dict[str, Any], cid: Any, node_id: str
) -> tuple[dict[str, Any], dict[str, Any]] | tuple[None, None]:
    """The campaign body's :Document + :hasBody relationship, or (None, None)."""
    body = camp.get("body")
    if not body:
        return None, None
    doc_id = f"listmonk:campaign:{cid}:body"
    document = {
        "id": doc_id,
        "text": body,
        "title": camp.get("subject") or camp.get("name"),
        "campaign_id": str(cid),
    }
    relationship = {"source": node_id, "target": doc_id, "relationship": "hasBody"}
    return document, relationship


def ingest_campaigns(*args: object, **kwargs: object) -> object:
    """Map Listmonk campaign records → :Campaign nodes (+ :SubscriptionList /

    SDK-GAP: Always raises now; see KnowledgeGraphIngestUnavailable.
    """
    _kg_unavailable("ingest_campaigns")


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


class KnowledgeGraphIngestUnavailable(RuntimeError):
    """Direct-to-graph ingestion is unavailable from this connector.

    SDK-GAP (EH-48x, /var/tmp/l9/finish/au-decon-G4c/SDK-GAPS.md): raised in
    place of the old ``agent_utilities.knowledge_graph`` native-ingest call --
    agent-connector-sdk has no facade over EG's typed ingestion protocol yet,
    and the fleet precedent (agents/world-reference-mcp) moves direct-to-graph
    delivery to agent_connector_sdk.runner/sinks at the deployment layer, out
    of connector scope.
    """


def _kg_unavailable(name: str) -> None:
    raise KnowledgeGraphIngestUnavailable(
        f"{name}: direct-to-graph ingestion moved out of connector code "
        "(agent-utilities removed); no agent-connector-sdk facade exists yet "
        "-- see SDK-GAPS.md"
    )
