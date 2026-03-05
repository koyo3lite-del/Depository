"""Tests for the agents module."""

import pytest
from crystalclearhouse.agents import Planner


def test_planner_initialization():
    """Test that planner initializes correctly."""
    planner = Planner()
    assert planner is not None
    assert planner.tasks == []


def test_planner_has_run_method():
    """Test that planner has run method."""
    planner = Planner()
    assert hasattr(planner, 'run')
    assert callable(planner.run)
