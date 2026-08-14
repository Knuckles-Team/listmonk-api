"""Native epistemic-graph typed-node + document ingestion — Wire-First coverage.

Exercises the real ``ingest_entities`` / ``ingest_documents`` / ``ingest_campaigns`` /
``ingest_lists`` / ``ingest_subscribers`` seam with a fake engine client (no engine
required), asserting the txn add_node/commit + edge calls and the Listmonk record →
:Campaign / :SubscriptionList / :Subscriber / :EmailTemplate / :Document mapping.
CONCEPT:AU-KG.ingest.enterprise-source-extractor.
"""

from __future__ import annotations

from typing import Any

import msgpack
import pytest
from listmonk_api.kg_ingest import (
    ingest_campaigns,
    ingest_documents,
    ingest_entities,
    ingest_lists,
    ingest_subscribers,
)

from agent_utilities.knowledge_graph.memory.native_ingest import NativeIngestError
from agent_utilities.security.brain_context import ActorContext, use_actor
from agent_utilities.models.company_brain import ActorType
from agent_utilities.knowledge_graph.core.session import GraphSession, use_session


@pytest.fixture(autouse=True)
def _governed_session():
    actor = ActorContext(
        actor_id="subject:opaque:synthetic",
        actor_type=ActorType.AUTOMATED_SERVICE,
        roles=(),
        tenant_id="tenant:opaque:synthetic",
        authenticated=True,
    )
    session = GraphSession(
        actor=actor,
        tenant=actor.tenant_id,
        scopes=frozenset({"kg:write"}),
        graph="graph:opaque:synthetic",
        policy_version="policy:opaque:synthetic",
        audience="epistemic-graph",
    )
    with use_actor(actor), use_session(session):
        yield


class _FakeNodes:
    def __init__(self) -> None:
        self.values: dict[str, dict[str, Any]] = {}

    def properties(self, node_id: str) -> dict[str, Any] | None:
        return self.values.get(node_id)

    def list(self) -> list[tuple[str, dict[str, Any]]]:
        return list(self.values.items())


class _FakeChanges:
    def __init__(self, nodes: _FakeNodes) -> None:
        self.nodes = nodes
        self.edges: list[tuple[str, str, dict[str, Any]]] = []
        self.applied: list[dict[str, Any]] = []
        self.records: dict[str, dict[str, Any]] = {}
        self.versions: dict[str, dict[str, Any]] = {}

    def get(self, envelope_id: str) -> dict[str, Any] | None:
        return self.records.get(envelope_id)

    def content_version(self, object_id: str) -> dict[str, Any] | None:
        return self.versions.get(object_id)

    def cursor(self, _source: str, _partition: str = "") -> None:
        return None

    def apply(self, envelope: dict[str, Any]) -> dict[str, Any]:
        self.applied.append(envelope)
        mutation = envelope["mutation"]
        for operation in mutation["operations"]:
            method = operation["method"]
            params = method["params"]
            properties = msgpack.unpackb(params["properties_msgpack"], raw=False)
            if method["method"] == "AddNode":
                self.nodes.values[params["node_id"]] = properties
            elif method["method"] == "AddEdge":
                self.edges.append(
                    (params["source_id"], params["target_id"], properties)
                )
        version = envelope["content_version"]
        self.versions[version["object_id"]] = version
        self.records[envelope["envelope_id"]] = envelope
        return {
            "batch_id": mutation["batch_id"],
            "replayed": False,
            "projection_pending": False,
        }


class _FakeRdf:
    def validate_shacl(self, _shapes: str, _data_graph: str) -> dict[str, Any]:
        return {"conforms": True, "results": []}


class _FakeClient:
    def __init__(self) -> None:
        self.nodes = _FakeNodes()
        self.changes = _FakeChanges(self.nodes)
        self.rdf = _FakeRdf()

    @staticmethod
    def supports(operation: str) -> bool:
        return operation == "ApplyChangeEnvelope"


def test_ingest_entities_writes_nodes_and_edges():
    c = _FakeClient()
    res = ingest_entities(
        [
            {"id": "a", "node_type": "Campaign", "name": "c"},
            {"id": "b", "node_type": "SubscriptionList"},
        ],
        [{"source": "a", "target": "b", "relationship": "targetsList"}],
        client=c,
    )
    assert res == {"nodes": 2, "edges": 1}
    assert len(c.changes.applied) == 1
    assert set(c.nodes.values) == {"a", "b"}
    # provenance is stamped
    assert c.nodes.values["a"]["source"] == "listmonk-api"
    assert c.nodes.values["a"]["domain"] == "listmonk"
    assert c.changes.edges == [("a", "b", {"relationship": "targetsList"})]


def test_ingest_documents_writes_document_nodes():
    c = _FakeClient()
    res = ingest_documents(
        [{"id": "listmonk:campaign:1:body", "text": "<h1>Hi</h1>", "title": "Hi"}],
        client=c,
    )
    assert res == {"nodes": 1, "edges": 0}
    node = c.nodes.values["listmonk:campaign:1:body"]
    assert node["node_type"] == "Document"
    assert node["text"] == "<h1>Hi</h1>"
    assert node["needs_enrichment"] is True  # stamped


def test_ingest_campaigns_maps_campaign_list_template_and_body():
    c = _FakeClient()
    res = ingest_campaigns(
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
        client=c,
    )
    # 1 campaign + 1 list + 1 template = 3 entity nodes, + 1 document node = 4
    assert res == {"nodes": 4, "edges": 3}
    camp = c.nodes.values["listmonk:campaign:42"]
    assert camp["node_type"] == "Campaign"
    assert camp["campaignStatus"] == "running"
    assert camp["subject"] == "News"
    assert camp["externalToolId"] == "42"
    assert c.nodes.values["listmonk:list:3"]["node_type"] == "SubscriptionList"
    assert c.nodes.values["listmonk:template:5"]["node_type"] == "EmailTemplate"
    assert c.nodes.values["listmonk:campaign:42:body"]["node_type"] == "Document"
    edge_types = {e[2]["relationship"] for e in c.changes.edges}
    assert edge_types == {"targetsList", "usesTemplate", "hasBody"}


def test_ingest_lists_maps_subscription_list():
    c = _FakeClient()
    res = ingest_lists(
        {
            "results": [
                {"id": 3, "name": "Product", "type": "public", "optin": "double"}
            ]
        },
        client=c,
    )
    assert res == {"nodes": 1, "edges": 0}
    node = c.nodes.values["listmonk:list:3"]
    assert node["node_type"] == "SubscriptionList"
    assert node["listType"] == "public"
    assert node["optinType"] == "double"


def test_ingest_subscribers_maps_subscriber_and_membership():
    c = _FakeClient()
    res = ingest_subscribers(
        [
            {
                "id": 9,
                "name": "Jane",
                "email": "jane@example.com",
                "status": "enabled",
                "lists": [{"id": 3}],
            }
        ],
        client=c,
    )
    assert res == {"nodes": 1, "edges": 1}
    node = c.nodes.values["listmonk:subscriber:9"]
    assert node["node_type"] == "Subscriber"
    # native_ingest's governed PII scrubber redacts email-shaped values.
    assert node["email"] == "[REDACTED_EMAIL]"
    assert node["subscriberStatus"] == "enabled"
    assert c.changes.edges == [
        ("listmonk:subscriber:9", "listmonk:list:3", {"relationship": "subscribedToList"})
    ]


def test_retired_structural_alias_is_rejected():
    with pytest.raises(NativeIngestError, match="canonical node_type"):
        ingest_entities([{"id": "a", "type": "Campaign"}], client=_FakeClient())


def test_empty_native_ingest_is_rejected():
    with pytest.raises(NativeIngestError, match="at least one entity"):
        ingest_entities([], client=_FakeClient())
