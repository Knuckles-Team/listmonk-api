"""Basic startup smoke tests."""

import subprocess
import sys

import pytest


def test_module_runnable():
    """Package module should be runnable with --help or similar."""
    import pathlib
    import tomllib

    root = pathlib.Path(__file__).resolve().parent.parent
    project = tomllib.loads((root / "pyproject.toml").read_text())
    pkg_name = project["project"]["name"].replace("-", "_")
    result = subprocess.run(
        [sys.executable, "-c", f"import {pkg_name}"],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, f"Import failed: {result.stderr}"
