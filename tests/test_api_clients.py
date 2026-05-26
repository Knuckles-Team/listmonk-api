import pytest
from unittest.mock import Mock, patch
from requests import Response, HTTPError
from listmonk_api.api_client import ListmonkAPI
from listmonk_api.models import (
    CampaignCreateRequest,
    CampaignStatusRequest,
    ImportSubscribersRequest,
    ListCreateRequest,
    ListEditRequest,
    MediaUploadRequest,
    SubscriberCreateRequest,
    TransactionalMessageRequest,
)


@pytest.fixture
def mock_session():
    """Patches requests.Session used by BaseApiClient."""
    with patch(
        "listmonk_api.api.api_client_base.requests.Session"
    ) as mock_session_class:
        session = Mock()
        mock_session_class.return_value = session
        yield session


@pytest.fixture
def client(mock_session):
    """Returns a ListmonkAPI client."""
    return ListmonkAPI(url="http://mock-listmonk", token="mock-token")


# ==============================================================================
# Base API Client Tests
# ==============================================================================


def test_base_client_init(mock_session, client):
    mock_session.headers.update.assert_called_with(
        {"Authorization": "Bearer mock-token", "Content-Type": "application/json"}
    )


def test_base_client_http_verbs(mock_session, client):
    # GET
    mock_resp = Mock(spec=Response)
    mock_session.get.return_value = mock_resp
    res = client.get("/test")
    assert res == mock_resp
    mock_session.get.assert_called_with("http://mock-listmonk/test")

    # POST
    mock_session.post.return_value = mock_resp
    res = client.post("/test", json={"a": 1})
    assert res == mock_resp
    mock_session.post.assert_called_with("http://mock-listmonk/test", json={"a": 1})

    # PUT
    mock_session.put.return_value = mock_resp
    res = client.put("/test", json={"b": 2})
    assert res == mock_resp
    mock_session.put.assert_called_with("http://mock-listmonk/test", json={"b": 2})

    # DELETE
    mock_session.delete.return_value = mock_resp
    res = client.delete("/test")
    assert res == mock_resp
    mock_session.delete.assert_called_with("http://mock-listmonk/test")


# ==============================================================================
# Campaigns API Tests
# ==============================================================================


def test_get_campaigns_dict_return(mock_session, client):
    # Mock pagination: X-Total-Pages = 2
    mock_resp_init = Mock(spec=Response)
    mock_resp_init.headers = {"X-Total-Pages": "2"}

    mock_resp_page1 = Mock(spec=Response)
    mock_resp_page1.json.return_value = {
        "data": {"results": [{"id": 1, "name": "Campaign 1"}]}
    }

    mock_resp_page2 = Mock(spec=Response)
    mock_resp_page2.json.return_value = {
        "data": {"results": [{"id": 2, "name": "Campaign 2"}]}
    }

    mock_session.get.side_effect = [mock_resp_init, mock_resp_page1, mock_resp_page2]

    results = client.get_campaigns(
        query={"status": "draft"}, order_by="created_at", order="desc"
    )
    assert len(results) == 2
    assert results[0]["id"] == 1
    assert results[1]["id"] == 2

    # Check that sorting parameters were constructed correctly
    mock_session.get.assert_any_call("http://mock-listmonk/campaigns?per_page=100")
    mock_session.get.assert_any_call(
        "http://mock-listmonk/campaigns?per_page=100&order_by=created_at&order=desc&page=1",
        json={"status": "draft"},
    )


def test_get_campaigns_list_and_other_returns(mock_session, client):
    mock_resp_init = Mock(spec=Response)
    mock_resp_init.headers = {}  # No X-Total-Pages default to 1

    # First test returning list directly
    mock_resp_page_list = Mock(spec=Response)
    mock_resp_page_list.json.return_value = [{"id": 3}]

    mock_session.get.side_effect = [mock_resp_init, mock_resp_page_list]
    results = client.get_campaigns(max_pages=1)
    assert results == [{"id": 3}]

    # Second test returning string or other type directly
    mock_resp_page_str = Mock(spec=Response)
    mock_resp_page_str.json.return_value = "raw response"
    mock_session.get.side_effect = [mock_resp_init, mock_resp_page_str]
    results = client.get_campaigns(max_pages=1)
    assert results == ["raw response"]


def test_campaign_endpoints(mock_session, client):
    mock_resp = Mock(spec=Response)
    mock_resp.json.return_value = {"success": True}
    mock_session.get.return_value = mock_resp
    mock_session.post.return_value = mock_resp
    mock_session.put.return_value = mock_resp
    mock_session.delete.return_value = mock_resp

    assert client.get_campaign(42) == {"success": True}
    mock_session.get.assert_called_with("http://mock-listmonk/campaigns/42")

    assert client.get_campaign_preview(42) == {"success": True}
    mock_session.get.assert_called_with("http://mock-listmonk/campaigns/42/preview")

    assert client.get_campaign_stats(42) == {"success": True}
    mock_session.get.assert_called_with(
        "http://mock-listmonk/campaigns/42/running/stats"
    )

    # Create Campaign
    data = CampaignCreateRequest(
        name="Test Campaign",
        subject="Hello",
        lists=[1],
        from_email="noreply@test.com",
        send_type="regular",
        content_type="plain",
        body="Welcome!",
    )
    assert client.create_campaign(data) == {"success": True}
    mock_session.post.assert_called_with(
        "http://mock-listmonk/campaigns",
        json={
            "name": "Test Campaign",
            "subject": "Hello",
            "lists": [1],
            "from_email": "noreply@test.com",
            "send_type": "regular",
            "content_type": "plain",
            "body": "Welcome!",
        },
    )

    # Set Campaign Status
    status_data = CampaignStatusRequest(status="running")
    assert client.set_campaign_status(42, status_data) == {"success": True}
    mock_session.put.assert_called_with(
        "http://mock-listmonk/campaigns/42/status", json={"status": "running"}
    )

    # Delete Campaign
    assert client.delete_campaign(42) == {"success": True}
    mock_session.delete.assert_called_with("http://mock-listmonk/campaigns/42")


# ==============================================================================
# Import API Tests
# ==============================================================================


def test_import_endpoints(mock_session, client):
    mock_resp = Mock(spec=Response)
    mock_resp.json.return_value = {"success": True}
    mock_session.get.return_value = mock_resp
    mock_session.post.return_value = mock_resp
    mock_session.delete.return_value = mock_resp

    assert client.get_subscriber_import_status() == {"success": True}
    mock_session.get.assert_called_with("http://mock-listmonk/import/subscribers")

    assert client.get_subscriber_import_logs() == {"success": True}
    mock_session.get.assert_called_with("http://mock-listmonk/import/subscribers/logs")

    import_data = ImportSubscribersRequest(
        file="base64-content", mode="subscribe", lists=[1]
    )
    assert client.import_subscribers(import_data) == {"success": True}
    mock_session.post.assert_called_with(
        "http://mock-listmonk/import/subscribers",
        json={
            "file": "base64-content",
            "mode": "subscribe",
            "delim": ",",
            "lists": [1],
            "overwrite": True,
        },
    )

    assert client.delete_subscriber_import() == {"success": True}
    mock_session.delete.assert_called_with(
        "http://mock-listmonk/import/subscribers/logs"
    )


# ==============================================================================
# Lists API Tests
# ==============================================================================


def test_get_lists_pagination(mock_session, client):
    mock_resp_init = Mock(spec=Response)
    mock_resp_init.headers = {"X-Total-Pages": "1"}

    mock_resp_page = Mock(spec=Response)
    mock_resp_page.json.return_value = {
        "data": {"results": [{"id": 1, "name": "List A"}]}
    }

    mock_session.get.side_effect = [mock_resp_init, mock_resp_page]

    results = client.get_lists(query={"type": "public"}, order_by="name", order="asc")
    assert len(results) == 1
    assert results[0]["name"] == "List A"
    mock_session.get.assert_any_call(
        "http://mock-listmonk/lists?per_page=100&order_by=name&order=asc&page=1",
        json={"type": "public"},
    )

    # Test returning list directly
    mock_resp_list = Mock(spec=Response)
    mock_resp_list.json.return_value = [{"id": 2}]
    mock_session.get.side_effect = [mock_resp_init, mock_resp_list]
    results = client.get_lists()
    assert results == [{"id": 2}]

    # Test returning scalar directly
    mock_resp_raw = Mock(spec=Response)
    mock_resp_raw.json.return_value = "raw list"
    mock_session.get.side_effect = [mock_resp_init, mock_resp_raw]
    results = client.get_lists()
    assert results == ["raw list"]


def test_lists_endpoints(mock_session, client):
    mock_resp = Mock(spec=Response)
    mock_resp.json.return_value = {"success": True}
    mock_session.get.return_value = mock_resp
    mock_session.post.return_value = mock_resp
    mock_session.put.return_value = mock_resp

    assert client.get_list(5) == {"success": True}
    mock_session.get.assert_called_with("http://mock-listmonk/lists/5")

    create_data = ListCreateRequest(name="New List", type="public", optin="single")
    assert client.create_list(create_data) == {"success": True}
    mock_session.post.assert_called_with(
        "http://mock-listmonk/lists",
        json={"name": "New List", "type": "public", "optin": "single"},
    )

    edit_data = ListEditRequest(name="Edited List")
    assert client.edit_list(5, edit_data) == {"success": True}
    mock_session.put.assert_called_with(
        "http://mock-listmonk/lists/5", json={"name": "Edited List"}
    )


# ==============================================================================
# Media API Tests
# ==============================================================================


def test_media_endpoints(mock_session, client):
    mock_resp = Mock(spec=Response)
    mock_resp.json.return_value = {"success": True}
    mock_session.get.return_value = mock_resp
    mock_session.post.return_value = mock_resp
    mock_session.delete.return_value = mock_resp

    assert client.get_media(10) == {"success": True}
    mock_session.get.assert_called_with("http://mock-listmonk/media")

    upload_data = MediaUploadRequest(file="base64-file-data")
    assert client.upload_media(upload_data) == {"success": True}
    mock_session.post.assert_called_with(
        "http://mock-listmonk/media", json={"file": "base64-file-data"}
    )

    assert client.delete_media(10) == {"success": True}
    mock_session.delete.assert_called_with("http://mock-listmonk/media/10")


# ==============================================================================
# Subscribers API Tests
# ==============================================================================


def test_get_subscribers_pagination(mock_session, client):
    mock_resp_init = Mock(spec=Response)
    mock_resp_init.headers = {"X-Total-Pages": "1"}

    mock_resp_page = Mock(spec=Response)
    mock_resp_page.json.return_value = {
        "data": {"results": [{"id": 1, "email": "a@b.com"}]}
    }

    mock_session.get.side_effect = [mock_resp_init, mock_resp_page]

    # Test single and multiple list ID query constructions
    results = client.get_subscribers(list_id=5, query={"status": "enabled"})
    assert len(results) == 1
    mock_session.get.assert_any_call(
        "http://mock-listmonk/subscribers?per_page=100&list_id=5&page=1",
        json={"status": "enabled"},
    )

    mock_session.get.side_effect = [mock_resp_init, mock_resp_page]
    results = client.get_subscribers(list_id=[5, 6])
    assert len(results) == 1
    mock_session.get.assert_any_call(
        "http://mock-listmonk/subscribers?per_page=100&list_id=5&list_id=6&page=1",
        json=None,
    )

    # Test returning list directly
    mock_resp_list = Mock(spec=Response)
    mock_resp_list.json.return_value = [{"id": 2}]
    mock_session.get.side_effect = [mock_resp_init, mock_resp_list]
    results = client.get_subscribers()
    assert results == [{"id": 2}]

    # Test returning scalar directly
    mock_resp_raw = Mock(spec=Response)
    mock_resp_raw.json.return_value = "raw subscriber"
    mock_session.get.side_effect = [mock_resp_init, mock_resp_raw]
    results = client.get_subscribers()
    assert results == ["raw subscriber"]


def test_subscriber_endpoints(mock_session, client):
    mock_resp = Mock(spec=Response)
    mock_resp.json.return_value = {"success": True}
    mock_session.get.return_value = mock_resp
    mock_session.post.return_value = mock_resp

    assert client.get_subscriber(100) == {"success": True}
    mock_session.get.assert_called_with("http://mock-listmonk/subscribers/100")

    assert client.get_subscribers_from_list(5) == {"success": True}
    mock_session.get.assert_called_with("http://mock-listmonk/subscribers/lists/5")

    create_data = SubscriberCreateRequest(
        email="test@test.com", name="Test User", status="enabled"
    )
    assert client.create_subscriber(create_data) == {"success": True}
    mock_session.post.assert_called_with(
        "http://mock-listmonk/subscribers",
        json={
            "email": "test@test.com",
            "name": "Test User",
            "status": "enabled",
            "preconfirm_subscriptions": True,
        },
    )


# ==============================================================================
# Templates API Tests
# ==============================================================================


def test_templates_endpoints(mock_session, client):
    mock_resp_init = Mock(spec=Response)
    mock_resp_init.headers = {"X-Total-Pages": "1"}

    mock_resp_page = Mock(spec=Response)
    mock_resp_page.json.return_value = {
        "data": {"results": [{"id": 1, "name": "Template A"}]}
    }

    mock_session.get.side_effect = [mock_resp_init, mock_resp_page]
    results = client.get_templates()
    assert len(results) == 1
    assert results[0]["name"] == "Template A"

    # Test returning list directly for templates
    mock_resp_list = Mock(spec=Response)
    mock_resp_list.json.return_value = [{"id": 2}]
    mock_session.get.side_effect = [mock_resp_init, mock_resp_list]
    results = client.get_templates()
    assert results == [{"id": 2}]

    # Test returning raw scalar directly for templates
    mock_resp_raw = Mock(spec=Response)
    mock_resp_raw.json.return_value = "raw template"
    mock_session.get.side_effect = [mock_resp_init, mock_resp_raw]
    results = client.get_templates()
    assert results == ["raw template"]

    mock_resp = Mock(spec=Response)
    mock_resp.json.return_value = {"success": True}
    mock_session.get.side_effect = None
    mock_session.get.return_value = mock_resp
    mock_session.put.return_value = mock_resp
    mock_session.delete.return_value = mock_resp

    assert client.get_template(5) == {"success": True}
    mock_session.get.assert_called_with("http://mock-listmonk/templates/5")

    assert client.get_template_preview(5) == {"success": True}
    mock_session.get.assert_called_with("http://mock-listmonk/templates/5/preview")

    assert client.set_default_template(5) == {"success": True}
    mock_session.put.assert_called_with("http://mock-listmonk/templates/5/default")

    assert client.delete_template(5) == {"success": True}
    mock_session.delete.assert_called_with("http://mock-listmonk/templates/5")


# ==============================================================================
# Transactional API Tests
# ==============================================================================


def test_transactional_endpoint(mock_session, client):
    mock_resp = Mock(spec=Response)
    mock_resp.json.return_value = {"success": True}
    mock_session.post.return_value = mock_resp

    tx_data = TransactionalMessageRequest(
        template_id=2, subscriber_email="user@test.com", data={"first_name": "Test"}
    )
    assert client.transactional_message(tx_data) == {"success": True}
    mock_session.post.assert_called_with(
        "http://mock-listmonk/tx",
        json={
            "template_id": 2,
            "subscriber_email": "user@test.com",
            "data": {"first_name": "Test"},
        },
    )
