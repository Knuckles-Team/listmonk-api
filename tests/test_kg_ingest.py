"""Epistemic-graph typed-node + document ingestion -- Wire-First coverage for listmonk-api.

Exercises the real ``ingest_entities`` / ``ingest_documents`` / ``ingest_campaigns`` /
``ingest_lists`` / ``ingest_subscribers`` seam against a fake ``agent_connector_sdk.ingest``
transport (no engine required). The real SDK request builder
(``agent_connector_sdk.ingest.request.build_request``) still runs, so a malformed change
set and the PII privacy guard are still exercised by the SDK's own contract, not
re-derived here; only the final network commit is faked.
CONCEPT:AU-KG.ingest.enterprise-source-extractor.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest
from agent_connector_sdk.ingest import IngestError, KnowledgeIngest
from epistemic_graph.generated.source_ingestion import SourceIngestionRequest

from listmonk_api.kg_ingest import (
    ingest_campaigns,
    ingest_documents,
    ingest_entities,
    ingest_lists,
    ingest_subscribers,
)


class _FakeTransport:
    """Records every submitted request; no epistemic-graph engine required."""

    def __init__(self) -> None:
        self.requests: list[SourceIngestionRequest] = []

    async def source_status(self, _connector: str, _stream: str) -> Any:
        return SimpleNamespace(accepted_checkpoint=None)

    async def submit(self, request: SourceIngestionRequest) -> Any:
        self.requests.append(request)
        return SimpleNamespace(
            affected_count=len(request.records),
            relationship_count=len(request.relationships),
        )

    async def store_blob(self, _data: bytes) -> str:
        raise AssertionError("listmonk-api ingestion carries no media")


@pytest.fixture
def ingest() -> tuple[KnowledgeIngest, _FakeTransport]:
    transport = _FakeTransport()
    return KnowledgeIngest(transport, loop=None), transport


@pytest.mark.asyncio
async def test_ingest_entities_writes_nodes_and_edges(ingest):
    service, transport = ingest
    res = await ingest_entities(
        [
            {"id": "a", "node_type": "Campaign", "name": "c"},
            {"id": "b", "node_type": "SubscriptionList"},
        ],
        [{"source": "a", "target": "b", "relationship": "targetsList"}],
        ingest=service,
    )
    assert res == {"nodes": 2, "edges": 1}
    assert len(transport.requests) == 1
    request = transport.requests[0]
    record_ids = {record.record_id for record in request.records}
    assert record_ids == {"a", "b"}
    a_record = next(r for r in request.records if r.record_id == "a")
    assert a_record.payload["name"] == "c"
    assert request.relationships[0].relation_reference.endswith(
        "resources/Campaign/relations/targetsList"
    )


@pytest.mark.asyncio
async def test_ingest_documents_writes_document_nodes(ingest):
    service, transport = ingest
    res = await ingest_documents(
        [{"id": "listmonk:campaign:1:body", "text": "<h1>Hi</h1>", "title": "Hi"}],
        ingest=service,
    )
    assert res == {"nodes": 1, "edges": 0}
    record = next(
        r for r in transport.requests[0].records
        if r.record_id == "listmonk:campaign:1:body"
    )
    assert record.payload["text"] == "<h1>Hi</h1>"
    assert record.payload["title"] == "Hi"


@pytest.mark.asyncio
async def test_ingest_campaigns_maps_campaign_list_template_and_body(ingest):
    service, transport = ingest
    res = await ingest_campaigns(
        [
            {
                "id": 42,
                "name": "July",
                "subject": "News",
                "status": "running",
                "from_email": "news@example.com",
                "template_id": 5,
                "body": "<p>hello</p>",
                "lists": [{"id": 3, "name": "Product"}],
            }
        ],
        ingest=service,
    )
    # 1 campaign + 1 list + 1 template = 3 entity nodes, + 1 document node = 4
    assert res == {"nodes": 4, "edges": 3}
    # entities and the document body commit together in one transaction, since
    # the document's :hasBody relationship names the campaign as its source.
    assert len(transport.requests) == 1
    request = transport.requests[0]
    all_records = request.records
    all_relationships = request.relationships
    camp = next(r for r in all_records if r.record_id == "listmonk:campaign:42")
    assert camp.payload["campaignStatus"] == "running"
    assert camp.payload["subject"] == "News"
    assert camp.payload["externalToolId"] == "42"
    assert any(r.record_id == "listmonk:list:3" for r in all_records)
    assert any(r.record_id == "listmonk:template:5" for r in all_records)
    body = next(
        r for r in all_records if r.record_id == "listmonk:campaign:42:body"
    )
    assert body.payload["text"] == "<p>hello</p>"
    edge_types = {r.relation_reference.rsplit("/", 1)[-1] for r in all_relationships}
    assert edge_types == {"targetsList", "usesTemplate", "hasBody"}


@pytest.mark.asyncio
async def test_ingest_lists_maps_subscription_list(ingest):
    service, transport = ingest
    res = await ingest_lists(
        {
            "results": [
                {"id": 3, "name": "Product", "type": "public", "optin": "double"}
            ]
        },
        ingest=service,
    )
    assert res == {"nodes": 1, "edges": 0}
    record = transport.requests[0].records[0]
    assert record.record_id == "listmonk:list:3"
    assert record.payload["listType"] == "public"
    assert record.payload["optinType"] == "double"


@pytest.mark.asyncio
async def test_ingest_subscribers_maps_subscriber_and_membership(ingest):
    service, transport = ingest
    res = await ingest_subscribers(
        [
            {
                "id": 9,
                "name": "Jane",
                "email": "jane@example.com",
                "status": "enabled",
                "lists": [{"id": 3}],
            }
        ],
        ingest=service,
    )
    assert res == {"nodes": 1, "edges": 1}
    request = transport.requests[0]
    record = next(
        r for r in request.records if r.record_id == "listmonk:subscriber:9"
    )
    # the SDK's PersistencePrivacyGuard redacts email-shaped values by default.
    assert record.payload["email"] == "[REDACTED_EMAIL]"
    assert record.payload["subscriberStatus"] == "enabled"
    assert request.relationships[0].source.record_id == "listmonk:subscriber:9"
    assert request.relationships[0].target.record_id == "listmonk:list:3"


@pytest.mark.asyncio
async def test_retired_structural_alias_is_rejected(ingest):
    service, _transport = ingest
    with pytest.raises(IngestError, match="node_type"):
        await ingest_entities([{"id": "a", "type": "Campaign"}], ingest=service)


@pytest.mark.asyncio
async def test_empty_ingest_is_rejected(ingest):
    service, _transport = ingest
    with pytest.raises(IngestError, match="at least one entity"):
        await ingest_entities([], ingest=service)
