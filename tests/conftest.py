"""Shared test fixtures for Listmonk Api."""

import pytest


@pytest.fixture
def mock_env(monkeypatch):
    """Set standard test environment variables."""
    monkeypatch.setenv("LISTMONK_URL", "https://test.example.com")
    monkeypatch.setenv("LISTMONK_TOKEN", "test-token-12345")
