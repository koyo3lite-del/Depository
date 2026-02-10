"""Tests for the orchestrator module."""

import pytest
from crystalclearhouse.orchestrator import Orchestrator


def test_orchestrator_initialization():
    """Test that orchestrator initializes correctly."""
    orchestrator = Orchestrator()
    assert orchestrator is not None
    assert orchestrator.agents == []


def test_orchestrator_has_run_method():
    """Test that orchestrator has run method."""
    orchestrator = Orchestrator()
    assert hasattr(orchestrator, 'run')
    assert callable(orchestrator.run)
