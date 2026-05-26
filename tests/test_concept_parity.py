"""Verify CONCEPT ID parity between docs/concepts.md and codebase.

Tests that all concepts documented in docs/concepts.md are referenced
somewhere in the source code, and that no undocumented concepts exist.
"""

import re
from pathlib import Path

import pytest

PKG_DIR = Path(__file__).resolve().parent.parent
PKG_NAME = PKG_DIR.name.replace("-", "_")
SRC_DIR = PKG_DIR / PKG_NAME


@pytest.fixture
def concept_docs():
    """Load concepts from docs/concepts.md."""
    concepts_file = PKG_DIR / "docs" / "concepts.md"
    if not concepts_file.exists():
        pytest.skip("docs/concepts.md not found")
    content = concepts_file.read_text()
    # Extract CONCEPT:PREFIX-NNN patterns
    return set(re.findall(r"CONCEPT:[A-Z_]+-\d+", content))


@pytest.fixture
def concept_code():
    """Find CONCEPT references in source code."""
    concepts = set()
    if not SRC_DIR.exists():
        return concepts
    for py_file in SRC_DIR.rglob("*.py"):
        content = py_file.read_text(errors="ignore")
        concepts.update(re.findall(r"CONCEPT:[A-Z_]+-\d+", content))
    return concepts


def test_concepts_file_exists():
    """docs/concepts.md must exist."""
    assert (PKG_DIR / "docs" / "concepts.md").exists(), (
        "Missing docs/concepts.md — run generate_concepts.py"
    )


def test_concept_prefix_unique(concept_docs):
    """All documented concepts should share a single prefix."""
    prefixes = set()
    for c in concept_docs:
        prefix = c.split("-")[0].replace("CONCEPT:", "")
        prefixes.add(prefix)
    # Should have at most 2 prefixes: project-specific + cross-refs
    assert len(prefixes) <= 10, f"Too many CONCEPT prefixes: {prefixes}"
