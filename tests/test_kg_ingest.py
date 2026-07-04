"""Native epistemic-graph typed-node + document ingestion — Wire-First coverage.

Exercises the real ``ingest_entities`` / ``ingest_documents`` / ``ingest_campaigns`` /
``ingest_lists`` / ``ingest_subscribers`` seam with a fake engine client (no engine
required), asserting the txn add_node/commit + edge calls and the Listmonk record →
:Campaign / :SubscriptionList / :Subscriber / :EmailTemplate / :Document mapping.
CONCEPT:AU-KG.ingest.enterprise-source-extractor.
"""

from __future__ import annotations

from listmonk_api.kg_ingest import (
    ingest_campaigns,
    ingest_documents,
    ingest_entities,
    ingest_lists,
    ingest_subscribers,
)


class _FakeTxn:
    def __init__(self):
        self.nodes = {}
        self.committed = False

    def begin(self, graph=None):
        self.graph = graph
        return "txn-1"

    def add_node(self, txn, node_id, props):
        self.nodes[node_id] = props

    def commit(self, txn):
        self.committed = True
        return True


class _FakeEdges:
    def __init__(self):
        self.edges = []

    def add(self, src, dst, props):
        self.edges.append((src, dst, props))


class _FakeClient:
    def __init__(self):
        self.txn = _FakeTxn()
        self.edges = _FakeEdges()


def test_ingest_entities_writes_nodes_and_edges():
    c = _FakeClient()
    res = ingest_entities(
        [
            {"id": "a", "type": "Campaign", "name": "c"},
            {"id": "b", "type": "SubscriptionList"},
        ],
        [{"source": "a", "target": "b", "type": "targetsList"}],
        client=c,
        graph="__commons__",
    )
    assert res == {"nodes": 2, "edges": 1}
    assert c.txn.committed is True
    assert set(c.txn.nodes) == {"a", "b"}
    # provenance is stamped
    assert c.txn.nodes["a"]["source"] == "listmonk-api"
    assert c.txn.nodes["a"]["domain"] == "listmonk"
    assert c.edges.edges == [("a", "b", {"type": "targetsList"})]


def test_ingest_documents_writes_document_nodes():
    c = _FakeClient()
    res = ingest_documents(
        [{"id": "listmonk:campaign:1:body", "text": "<h1>Hi</h1>", "title": "Hi"}],
        client=c,
        graph="__commons__",
    )
    assert res == {"nodes": 1, "edges": 0}
    node = c.txn.nodes["listmonk:campaign:1:body"]
    assert node["type"] == "Document"
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
    assert camp["type"] == "Campaign"
    assert camp["campaignStatus"] == "running"
    assert camp["subject"] == "News"
    assert camp["externalToolId"] == "42"
    assert c.txn.nodes["listmonk:list:3"]["type"] == "SubscriptionList"
    assert c.txn.nodes["listmonk:template:5"]["type"] == "EmailTemplate"
    assert c.txn.nodes["listmonk:campaign:42:body"]["type"] == "Document"
    edge_types = {e[2]["type"] for e in c.edges.edges}
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
    assert node["type"] == "SubscriptionList"
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
    assert node["type"] == "Subscriber"
    assert node["email"] == "jane@example.com"
    assert node["subscriberStatus"] == "enabled"
    assert c.edges.edges == [
        ("listmonk:subscriber:9", "listmonk:list:3", {"type": "subscribedToList"})
    ]


def test_ingest_noops_without_engine():
    # No injected client + no reachable engine -> clean no-op.
    assert ingest_entities([{"id": "a", "type": "Campaign"}]) is None


def test_ingest_empty_is_noop():
    assert ingest_entities([], client=_FakeClient()) is None
    assert ingest_campaigns([], client=_FakeClient()) is None
    assert ingest_lists([], client=_FakeClient()) is None
    assert ingest_subscribers([], client=_FakeClient()) is None
