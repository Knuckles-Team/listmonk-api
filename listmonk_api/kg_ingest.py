"""Epistemic-graph ingestion for Listmonk records and documents.

CONCEPT:AU-KG.ingest.enterprise-source-extractor. The listmonk-api connector pushes
campaigns/lists/subscribers into the ONE epistemic-graph knowledge graph as **typed
OWL nodes** (``:Campaign``, ``:SubscriptionList``, ``:Subscriber``, ``:EmailTemplate``)
+ text bodies as ``:Document`` nodes, through ``agent_connector_sdk.ingest`` -- the
generated ``SourceIngest`` client, not a local ingestion helper.
"""

from __future__ import annotations

import logging
from typing import Any

from agent_connector_sdk.ingest import (
    ChangeSet,
    Document,
    Entity,
    IngestBinding,
    IngestError,
    KnowledgeIngest,
    Relationship,
    current_ingest,
)

logger = logging.getLogger("listmonk_api.kg")

_BINDING = IngestBinding(connector="listmonk-api", stream="listmonk")

_ENTITY_RESERVED_KEYS = frozenset({"id", "node_type"})
_RELATIONSHIP_RESERVED_KEYS = frozenset({"source", "target", "relationship"})
_DOCUMENT_RESERVED_KEYS = frozenset({"id", "text", "title", "source_uri"})


def _to_entity(record: dict[str, Any]) -> Entity:
    return Entity(
        id=record.get("id"),
        node_type=record.get("node_type"),
        properties={
            key: value
            for key, value in record.items()
            if key not in _ENTITY_RESERVED_KEYS
        },
    )


def _to_relationship(record: dict[str, Any]) -> Relationship:
    properties = {
        key: value
        for key, value in record.items()
        if key not in _RELATIONSHIP_RESERVED_KEYS
    }
    return Relationship(
        source=record["source"],
        target=record["target"],
        relationship=record["relationship"],
        properties=properties or None,
    )


def _to_document(record: dict[str, Any]) -> Document:
    return Document(
        id=record["id"],
        text=record["text"],
        title=record.get("title"),
        source_uri=record.get("source_uri"),
        properties={
            key: value
            for key, value in record.items()
            if key not in _DOCUMENT_RESERVED_KEYS
        },
    )


async def _submit(
    *,
    entities: tuple[Entity, ...] = (),
    documents: tuple[Document, ...] = (),
    relationships: tuple[Relationship, ...] = (),
    ingest: KnowledgeIngest | None = None,
) -> dict[str, int]:
    change_set = ChangeSet(
        entities=entities, documents=documents, relationships=relationships
    )
    service = ingest or current_ingest()
    receipt = await service.submit(_BINDING, change_set)
    return {"nodes": receipt.affected_count, "edges": receipt.relationship_count}


async def ingest_entities(
    entities: list[dict[str, Any]],
    relationships: list[dict[str, Any]] | None = None,
    *,
    ingest: KnowledgeIngest | None = None,
) -> dict[str, int]:
    """Write typed OWL nodes (+ edges) into epistemic-graph via the SDK ingest facade.

    Uses canonical ``node_type`` / ``relationship`` structural fields and surfaces
    a malformed change set or a refused commit as ``IngestError``.
    """
    if not entities:
        raise IngestError("ingest_entities needs at least one entity")
    return await _submit(
        entities=tuple(_to_entity(entity) for entity in entities),
        relationships=tuple(
            _to_relationship(relationship) for relationship in relationships or ()
        ),
        ingest=ingest,
    )


async def ingest_documents(
    documents: list[dict[str, Any]],
    relationships: list[dict[str, Any]] | None = None,
    *,
    ingest: KnowledgeIngest | None = None,
) -> dict[str, int]:
    """Write text records as canonical ``:Document`` nodes (+ edges).

    ``relationships`` uses the same canonical ``source``/``target``/``relationship``
    shape as :func:`ingest_entities`; document nodes and their links commit together.
    """
    if not documents:
        raise IngestError("ingest_documents needs at least one document")
    return await _submit(
        documents=tuple(_to_document(document) for document in documents),
        relationships=tuple(
            _to_relationship(relationship) for relationship in relationships or ()
        ),
        ingest=ingest,
    )


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


async def ingest_campaigns(
    campaigns: Any,
    *,
    ingest: KnowledgeIngest | None = None,
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
        entities.append(_campaign_entity(camp, cid, node_id))

        list_entities, list_relationships = _campaign_list_links(camp, node_id)
        entities.extend(list_entities)
        relationships.extend(list_relationships)

        template_entity, template_relationship = _campaign_template_link(camp, node_id)
        if template_entity is not None:
            entities.append(template_entity)
            relationships.append(template_relationship)

        document, document_relationship = _campaign_body_document(camp, cid, node_id)
        if document is not None:
            documents.append(document)
            document_relationships.append(document_relationship)
    if not entities:
        raise IngestError("ingest_entities needs at least one entity")
    # Entities and their document bodies commit in one transaction: a document's
    # :hasBody relationship names a campaign entity as its source, and the SDK's
    # request builder only resolves a relationship endpoint's node_type from
    # entities present in the SAME change set (or an explicit EntityRef) -- so
    # splitting this into two separate submits (entities, then documents) would
    # make the :hasBody edge's source type unresolvable.
    return await _submit(
        entities=tuple(_to_entity(entity) for entity in entities),
        documents=tuple(_to_document(document) for document in documents),
        relationships=tuple(
            _to_relationship(relationship)
            for relationship in (*relationships, *document_relationships)
        ),
        ingest=ingest,
    )


async def ingest_lists(
    lists: Any,
    *,
    ingest: KnowledgeIngest | None = None,
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
    return await ingest_entities(entities, ingest=ingest)


async def ingest_subscribers(
    subscribers: Any,
    *,
    ingest: KnowledgeIngest | None = None,
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
    return await ingest_entities(entities, relationships, ingest=ingest)
