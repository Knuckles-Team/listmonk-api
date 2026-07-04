"""Native epistemic-graph ingestion for Listmonk records (typed graph nodes + documents).

CONCEPT:AU-KG.ingest.enterprise-source-extractor. This connector natively pushes its
data into the ONE epistemic-graph knowledge graph **from its own code**, in every
modality that applies (the "maximum ingestion" bar):

* **typed nodes** — campaigns/lists/subscribers/templates → OWL ``:Campaign`` /
  ``:SubscriptionList`` / ``:Subscriber`` / ``:EmailTemplate`` nodes + links
  (:targetsList / :subscribedToList / :usesTemplate), via ``ingest_entities``.
* **documents** — campaign & template bodies worth semantic search → ``:Document``
  nodes carrying the text (``ingest_documents``); hub-side enrichment chunks/embeds them.

All writes ride the lightweight engine client (``GraphComputeEngine()._client`` + ``txn``) —
the same fast client the blob ``MediaStore`` uses, NOT the heavy in-process ingestion
engine. This module is a thin mapper over the shared primitive
``agent_utilities.knowledge_graph.memory.native_ingest``; the import is GUARDED so that
with no KG stack / no reachable engine every entry point **no-ops** (returns ``None``) and
the connector keeps working with zero KG infrastructure. Node ids follow
``listmonk:<class>:<externalId>``; ``type`` on each entity matches a class federated by
``listmonk_api.ontology`` (``listmonk.ttl``).
"""

from __future__ import annotations

import logging
import time
from typing import Any

logger = logging.getLogger("listmonk_api.kg")

_SOURCE = "listmonk-api"
_DOMAIN = "listmonk"
_DEFAULT_GRAPH = "__commons__"


def _client() -> tuple[Any | None, str]:
    """Return ``(engine_client, graph_name)`` or ``(None, "")`` when unavailable.

    Prefers the shared ``native_ingest.native_client``; falls back to building the
    lightweight :class:`GraphComputeEngine` directly. Never raises.
    """
    try:
        from agent_utilities.knowledge_graph.memory.native_ingest import native_client

        return native_client()
    except Exception as e:  # noqa: BLE001 — primitive not present in installed AU
        logger.debug("native primitive unavailable, falling back: %s", e)
    try:
        from agent_utilities.knowledge_graph.core.graph_compute import (
            GraphComputeEngine,
        )
    except Exception as e:  # noqa: BLE001 — KG stack absent
        logger.debug("KG ingest unavailable (import): %s", e)
        return None, ""
    try:
        engine = GraphComputeEngine()
        client = getattr(engine, "_client", None)
        if client is None:
            return None, ""
        return client, (getattr(engine, "graph_name", None) or _DEFAULT_GRAPH)
    except Exception as e:  # noqa: BLE001 — engine unreachable
        logger.debug("KG ingest: engine unreachable: %s", e)
        return None, ""


def _write_nodes(
    client: Any,
    graph: str,
    nodes: list[dict[str, Any]],
    relationships: list[dict[str, Any]] | None,
    *,
    source: str,
    domain: str,
) -> dict[str, int] | None:
    """Self-contained txn fallback: MERGE nodes in one txn, then add edges."""
    nodes = [n for n in nodes if n.get("id")]
    if not nodes:
        return None
    try:
        txn = client.txn.begin(graph=graph)
        for node in nodes:
            props = {k: v for k, v in node.items() if k != "id" and v is not None}
            props.setdefault("source", source)
            props.setdefault("domain", domain)
            client.txn.add_node(txn, node["id"], props)
        committed = client.txn.commit(txn)
    except Exception as e:  # noqa: BLE001 — engine/txn failure is non-fatal
        logger.warning("KG ingest: txn failed: %s", e)
        return None
    if not committed:
        logger.warning("KG ingest: txn not committed (conflict)")
        return None

    edges = 0
    for rel in relationships or []:
        try:
            client.edges.add(
                rel["source"], rel["target"], {"type": rel.get("type", "RELATED")}
            )
            edges += 1
        except Exception as e:  # noqa: BLE001 — pure edge link, best-effort
            logger.debug("KG ingest: edge skipped: %s", e)

    logger.info("KG ingest: wrote %d nodes, %d edges", len(nodes), edges)
    return {"nodes": len(nodes), "edges": edges}


def ingest_entities(
    entities: list[dict[str, Any]],
    relationships: list[dict[str, Any]] | None = None,
    *,
    source: str = _SOURCE,
    domain: str = _DOMAIN,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int] | None:
    """Write typed OWL nodes (+ edges) into epistemic-graph via the fast engine client.

    ``entities``: ``[{"id":..., "type":<owl:Class>, ...props}]``.
    ``relationships``: ``[{"source":id, "target":id, "type":<link>}]``.
    Returns ``{"nodes":n, "edges":m}`` or ``None`` (no engine / failure; never raises).
    Prefers the shared primitive; ``client``/``graph`` may be injected (tests).
    """
    entities = [e for e in (entities or []) if e.get("id")]
    if not entities:
        return None
    if client is None:
        try:
            from agent_utilities.knowledge_graph.memory.native_ingest import (
                ingest_entities as _shared,
            )

            return _shared(
                entities, relationships, source=source, domain=domain, graph=graph
            )
        except Exception as e:  # noqa: BLE001 — fall back to local txn path
            logger.debug("shared ingest_entities unavailable: %s", e)
        client, graph = _client()
    if client is None:
        return None
    return _write_nodes(
        client,
        graph or _DEFAULT_GRAPH,
        entities,
        relationships,
        source=source,
        domain=domain,
    )


def ingest_documents(
    documents: list[dict[str, Any]],
    *,
    source: str = _SOURCE,
    domain: str = _DOMAIN,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int] | None:
    """Write text records as ``:Document`` nodes (semantic-search fodder).

    Each doc: ``{"id":..., "text":..., "title"?:..., "source_uri"?:..., ...props}``.
    Returns ``{"nodes":n, "edges":0}`` or ``None``.
    """
    if client is None:
        try:
            from agent_utilities.knowledge_graph.memory.native_ingest import (
                ingest_documents as _shared,
            )

            return _shared(documents, source=source, domain=domain, graph=graph)
        except Exception as e:  # noqa: BLE001 — fall back to local txn path
            logger.debug("shared ingest_documents unavailable: %s", e)
        client, graph = _client()
    if client is None:
        return None
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    nodes: list[dict[str, Any]] = []
    for doc in documents or []:
        did = doc.get("id")
        text = doc.get("text") or doc.get("content")
        if not did or not text:
            continue
        node = {k: v for k, v in doc.items() if k not in ("content",) and v is not None}
        node["id"] = did
        node["type"] = "Document"
        node["text"] = text
        node.setdefault("created_at", now)
        nodes.append(node)
    if not nodes:
        return None
    return _write_nodes(
        client, graph or _DEFAULT_GRAPH, nodes, None, source=source, domain=domain
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
) -> dict[str, int] | None:
    """Map Listmonk campaign records → :Campaign nodes (+ :SubscriptionList /
    :EmailTemplate links) and their bodies → :Document nodes, and ingest both."""
    entities: list[dict[str, Any]] = []
    relationships: list[dict[str, Any]] = []
    documents: list[dict[str, Any]] = []
    for camp in _as_list(campaigns):
        cid = camp.get("id")
        if cid is None:
            continue
        node_id = f"listmonk:campaign:{cid}"
        entities.append(
            {
                "id": node_id,
                "type": "Campaign",
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
                    "type": "SubscriptionList",
                    "name": lst.get("name") if isinstance(lst, dict) else None,
                }
            )
            relationships.append(
                {
                    "source": node_id,
                    "target": f"listmonk:list:{lid}",
                    "type": "targetsList",
                }
            )
        tid = camp.get("template_id")
        if tid:
            entities.append({"id": f"listmonk:template:{tid}", "type": "EmailTemplate"})
            relationships.append(
                {
                    "source": node_id,
                    "target": f"listmonk:template:{tid}",
                    "type": "usesTemplate",
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
            relationships.append(
                {"source": node_id, "target": doc_id, "type": "hasBody"}
            )
    ent_res = ingest_entities(entities, relationships, client=client, graph=graph)
    doc_res = ingest_documents(documents, client=client, graph=graph)
    return _merge(ent_res, doc_res)


def ingest_lists(
    lists: Any,
    *,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int] | None:
    """Map Listmonk list records → :SubscriptionList nodes and ingest."""
    entities: list[dict[str, Any]] = []
    for lst in _as_list(lists):
        lid = lst.get("id")
        if lid is None:
            continue
        entities.append(
            {
                "id": f"listmonk:list:{lid}",
                "type": "SubscriptionList",
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
) -> dict[str, int] | None:
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
                "type": "Subscriber",
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
                    "type": "subscribedToList",
                }
            )
    return ingest_entities(entities, relationships, client=client, graph=graph)


def _merge(a: dict[str, int] | None, b: dict[str, int] | None) -> dict[str, int] | None:
    if a is None:
        return b
    if b is None:
        return a
    return {
        "nodes": a.get("nodes", 0) + b.get("nodes", 0),
        "edges": a.get("edges", 0) + b.get("edges", 0),
    }
