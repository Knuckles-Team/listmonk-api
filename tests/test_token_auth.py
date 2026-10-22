"""listmonk API-user authentication header (no network)."""

from unittest.mock import Mock, patch

import pytest

from listmonk_api.api.api_client_base import build_authorization
from listmonk_api.api_client import ListmonkAPI


def _headers(token, username=None):
    with patch("listmonk_api.api.api_client_base.requests.Session") as session_cls:
        session = Mock()
        session_cls.return_value = session
        ListmonkAPI(url="http://mock-listmonk", token=token, username=username)
        return session.headers.update.call_args.args[0]


@pytest.mark.spec("CONN-LISTMONK-API-R001")
def test_header_uses_token_scheme_with_username():
    assert _headers("abc", "arbora-mcp")["Authorization"] == "token arbora-mcp:abc"


@pytest.mark.spec("CONN-LISTMONK-API-R001")
def test_header_never_uses_bearer():
    assert not _headers("abc", "u")["Authorization"].startswith("Bearer")


@pytest.mark.spec("CONN-LISTMONK-API-R002")
def test_combined_user_token_is_used_as_given():
    assert build_authorization("arbora-mcp:abc", "ignored") == "token arbora-mcp:abc"


@pytest.mark.spec("CONN-LISTMONK-API-R002")
def test_token_without_username_is_sent_as_given():
    assert build_authorization("abc") == "token abc"


@pytest.mark.spec("CONN-LISTMONK-API-R003")
def test_auth_client_reads_listmonk_username(monkeypatch):
    import listmonk_api.auth as auth

    monkeypatch.setenv("LISTMONK_URL", "http://mock-listmonk")
    monkeypatch.setenv("LISTMONK_TOKEN", "abc")
    monkeypatch.setenv("LISTMONK_USERNAME", "arbora-mcp")
    monkeypatch.setattr(auth, "_client", None)
    with patch("listmonk_api.api.api_client_base.requests.Session") as session_cls:
        session = Mock()
        session_cls.return_value = session
        auth.get_client()
        sent = session.headers.update.call_args.args[0]
    monkeypatch.setattr(auth, "_client", None)
    assert sent["Authorization"] == "token arbora-mcp:abc"
