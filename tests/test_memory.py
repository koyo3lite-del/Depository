"""Tests for the memory module."""

import pytest
from crystalclearhouse.memory import Memory


def test_memory_initialization():
    """Test that memory initializes correctly."""
    memory = Memory()
    assert memory is not None
    assert memory.store == {}


def test_memory_save_and_load():
    """Test saving and loading data."""
    memory = Memory()
    memory.save("test_key", "test_value")
    assert memory.load("test_key") == "test_value"


def test_memory_clear():
    """Test clearing memory."""
    memory = Memory()
    memory.save("key1", "value1")
    memory.save("key2", "value2")
    memory.clear()
    assert memory.store == {}
    assert memory.load("key1") is None
