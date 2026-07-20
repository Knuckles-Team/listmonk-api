"""Native epistemic-graph typed-node + document ingestion — Wire-First coverage.

Exercises the real ``ingest_entities`` / ``ingest_documents`` / ``ingest_campaigns`` /
``ingest_lists`` / ``ingest_subscribers`` seam with a fake engine client (no engine
required), asserting the txn add_node/commit + edge calls and the Listmonk record →
:Campaign / :SubscriptionList / :Subscriber / :EmailTemplate / :Document mapping.
CONCEPT:AU-KG.ingest.enterprise-source-extractor.
"""

from __future__ import annotations

import pytest
from listmonk_api.kg_ingest import (
    ingest_campaigns,
    ingest_documents,
    ingest_entities,
    ingest_lists,
    ingest_subscribers,
)

from agent_utilities.knowledge_graph.memory.native_ingest import NativeIngestError


class _FakeTxn:
    def __init__(self):
        self.nodes = {}
        self.edges = []
        self.committed = False

    def begin(self, graph=None):
        self.graph = graph
        return "txn-1"

    def add_node(self, txn, node_id, props):
        self.nodes[node_id] = props

    def add_edge(self, txn, source, target, props):
        self.edges.append((source, target, props))

    def commit(self, txn):
        self.committed = True
        return True


class _FakeClient:
    def __init__(self):
        self.txn = _FakeTxn()


def test_ingest_entities_writes_nodes_and_edges():
    c = _FakeClient()
    res = ingest_entities(
        [
            {"id": "a", "node_type": "Campaign", "name": "c"},
            {"id": "b", "node_type": "SubscriptionList"},
        ],
        [{"source": "a", "target": "b", "relationship": "targetsList"}],
        client=c,
        graph="__commons__",
    )
    assert res == {"nodes": 2, "edges": 1}
    assert c.txn.committed is True
    assert set(c.txn.nodes) == {"a", "b"}
    # provenance is stamped
    assert c.txn.nodes["a"]["source"] == "listmonk-api"
    assert c.txn.nodes["a"]["domain"] == "listmonk"
    assert c.txn.edges == [("a", "b", {"relationship": "targetsList"})]


def test_ingest_documents_writes_document_nodes():
    c = _FakeClient()
    res = ingest_documents(
        [{"id": "listmonk:campaign:1:body", "text": "<h1>Hi</h1>", "title": "Hi"}],
        client=c,
        graph="__commons__",
    )
    assert res == {"nodes": 1, "edges": 0}
    node = c.txn.nodes["listmonk:campaign:1:body"]
    assert node["node_type"] == "Document"
    assert node["text"] == "<h1>Hi</h1>"
    assert node["created_at"]  # stamped


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
        graph="__commons__",
    )
    # 1 campaign + 1 list + 1 template = 3 entity nodes, + 1 document node = 4
    assert res == {"nodes": 4, "edges": 3}
    camp = c.txn.nodes["listmonk:campaign:42"]
    assert camp["node_type"] == "Campaign"
    assert camp["campaignStatus"] == "running"
    assert camp["subject"] == "News"
    assert camp["externalToolId"] == "42"
    assert c.txn.nodes["listmonk:list:3"]["node_type"] == "SubscriptionList"
    assert c.txn.nodes["listmonk:template:5"]["node_type"] == "EmailTemplate"
    assert c.txn.nodes["listmonk:campaign:42:body"]["node_type"] == "Document"
    edge_types = {e[2]["relationship"] for e in c.txn.edges}
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
        graph="__commons__",
    )
    assert res == {"nodes": 1, "edges": 0}
    node = c.txn.nodes["listmonk:list:3"]
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
        graph="__commons__",
    )
    assert res == {"nodes": 1, "edges": 1}
    node = c.txn.nodes["listmonk:subscriber:9"]
    assert node["node_type"] == "Subscriber"
    assert node["email"] == "jane@example.com"
    assert node["subscriberStatus"] == "enabled"
    assert c.txn.edges == [
        ("listmonk:subscriber:9", "listmonk:list:3", {"relationship": "subscribedToList"})
    ]


def test_retired_structural_alias_is_rejected():
    with pytest.raises(NativeIngestError, match="canonical node_type"):
        ingest_entities([{"id": "a", "type": "Campaign"}], client=_FakeClient())


def test_empty_native_ingest_is_rejected():
    with pytest.raises(NativeIngestError, match="at least one entity"):
        ingest_entities([], client=_FakeClient())
