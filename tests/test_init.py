import sys
import pytest
from unittest.mock import patch, MagicMock
import listmonk_api


def test_init_available_flags():
    # Test _MCP_AVAILABLE and _AGENT_AVAILABLE dynamic checks
    assert listmonk_api._MCP_AVAILABLE is True
    assert listmonk_api._AGENT_AVAILABLE is True


def test_init_lazy_loading():
    # Test lazy loading of mcp_server and agent_server attributes
    assert listmonk_api.mcp_server is not None
    assert listmonk_api.agent_server is not None


def test_init_attribute_error():
    # Test getting a non-existent attribute raises AttributeError
    with pytest.raises(
        AttributeError, match="has no attribute 'non_existent_attribute'"
    ):
        _ = listmonk_api.non_existent_attribute


def test_init_dir():
    # Test dynamic __dir__
    attrs = dir(listmonk_api)
    assert "mcp_server" in attrs
    assert "agent_server" in attrs
    assert "CORE_MODULES" in attrs


def test_init_import_error_handling():
    # Test when optional modules are not available / fail to import
    with patch("listmonk_api.__init__.importlib.import_module") as mock_import:
        mock_import.side_effect = ImportError("Could not import module")

        # Freshly test safely importing under the hood
        from listmonk_api.__init__ import _import_module_safely

        res = _import_module_safely("listmonk_api.non_existent")
        assert res is None


def test_init_avail_flags_when_unavailable():
    # Test _MCP_AVAILABLE and _AGENT_AVAILABLE when modules raise ImportError
    with patch("listmonk_api.__init__._import_module_safely") as mock_import_safely:
        mock_import_safely.return_value = None

        # Direct call to __getattr__ for flags
        from listmonk_api.__init__ import __getattr__

        assert __getattr__("_MCP_AVAILABLE") is False
        assert __getattr__("_AGENT_AVAILABLE") is False
