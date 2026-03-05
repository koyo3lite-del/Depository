"""
Memory management for the system.
"""

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Memory:
    """Manages system memory and state."""
    
    def __init__(self):
        """Initialize the memory system."""
        self.store = {}
        logger.info("Memory system initialized")
    
    def save(self, key, value):
        """Save a value to memory."""
        self.store[key] = value
        logger.info(f"Saved {key} to memory")
    
    def load(self, key):
        """Load a value from memory."""
        return self.store.get(key)
    
    def clear(self):
        """Clear all memory."""
        self.store.clear()
        logger.info("Memory cleared")
