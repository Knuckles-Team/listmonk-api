#!/usr/bin/env python

import importlib
import inspect
from typing import Any
import warnings

# Suppress RequestsDependencyWarning due to chardet 6.x / requests 2.32.x mismatch
# Centralized here to ensure it runs before any sub-package imports
warnings.filterwarnings("ignore", message=".*urllib3.*or chardet.*")

__all__: list[str] = []

CORE_MODULES: list[str] = [
    "listmonk_api.api_client",
    "listmonk_api.models",
]

OPTIONAL_MODULES = {
    "listmonk_api.agent_server": "agent_server",
    "listmonk_api.mcp_server": "mcp_server",
}


def _expose_members(module):
    """Expose public classes and functions from a module into globals and __all__."""
    for name, obj in inspect.getmembers(module):
        if (inspect.isclass(obj) or inspect.isfunction(obj)) and not name.startswith(
            "_"
        ):
            globals()[name] = obj
            if name not in __all__:
                __all__.append(name)


# Eagerly import core modules (keeps API wrappers fast & light)
for module_name in CORE_MODULES:
    if module_name:
        module = importlib.import_module(module_name)
        _expose_members(module)

# Dynamic/lazy loading of optional modules (agent_server, mcp_server)
_loaded_optional_modules: dict[str, Any] = {}


def _import_module_safely(module_name: str):
    """Try to import a module and return it, or None if not available."""
    try:
        return importlib.import_module(module_name)
    except ImportError:
        return None


#: Maps a lazy availability-flag attribute to the substring that identifies
#: its module in ``OPTIONAL_MODULES``.
_AVAILABILITY_FLAG_MODULES = {
    "_MCP_AVAILABLE": "mcp_server",
    "_AGENT_AVAILABLE": "agent_server",
}


def _module_availability(module_substring: str) -> bool:
    """Whether the ``OPTIONAL_MODULES`` entry matching ``module_substring`` imports."""
    module_key = next((k for k in OPTIONAL_MODULES if module_substring in k), None)
    if module_key is None:
        return False
    return _import_module_safely(module_key) is not None


def _load_optional_module(module_name: str):
    """Import (once, cached) and expose an optional module's public members."""
    if module_name not in _loaded_optional_modules:
        module = _import_module_safely(module_name)
        if module is not None:
            _loaded_optional_modules[module_name] = module
            _expose_members(module)
    return _loaded_optional_modules.get(module_name)


def _find_optional_attr(name: str) -> Any:
    """Look ``name`` up across every optional module, importing each lazily."""
    for module_name in OPTIONAL_MODULES:
        module = _load_optional_module(module_name)
        if module is not None and hasattr(module, name):
            return getattr(module, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __getattr__(name: str) -> Any:
    if name in _AVAILABILITY_FLAG_MODULES:
        return _module_availability(_AVAILABILITY_FLAG_MODULES[name])
    return _find_optional_attr(name)


def __dir__() -> list[str]:
    return sorted(list(globals().keys()) + __all__)
