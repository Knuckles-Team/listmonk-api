import sys
import pytest
from unittest.mock import patch, MagicMock
import listmonk_api






def test_init_attribute_error():
    # Test getting a non-existent attribute raises AttributeError
    with pytest.raises(
        AttributeError, match="has no attribute 'non_existent_attribute'"
    ):
        _ = listmonk_api.non_existent_attribute




def test_init_import_error_handling():
    # Test when optional modules are not available / fail to import
    with patch("listmonk_api.__init__.importlib.import_module") as mock_import:
        mock_import.side_effect = ImportError("Could not import module")

        # Freshly test safely importing under the hood
        from listmonk_api.__init__ import _import_module_safely

        res = _import_module_safely("listmonk_api.non_existent")
        assert res is None


