"""
Example of slow and inefficient code patterns.
This file demonstrates common performance anti-patterns.
"""

import time
import json


class SlowDataProcessor:
    """A class demonstrating inefficient code patterns."""
    
    def __init__(self):
        self.data = []
        self.cache = {}
    
    def inefficient_string_concatenation(self, items):
        """
        INEFFICIENT: Using + operator in a loop for string concatenation.
        Time Complexity: O(n²) due to string immutability
        """
        result = ""
        for item in items:
            result = result + str(item) + ","  # Creates new string each iteration
        return result.rstrip(",")
    
    def inefficient_list_building(self, n):
        """
        INEFFICIENT: Repeatedly using list concatenation instead of append.
        Time Complexity: O(n²)
        """
        result = []
        for i in range(n):
            result = result + [i]  # Creates new list each iteration
        return result
    
    def unnecessary_list_copies(self, data):
        """
        INEFFICIENT: Creating unnecessary copies of lists.
        """
        # Making full copies when slicing or filtering
        filtered = []
        for item in data[:]:  # Unnecessary copy
            if item % 2 == 0:
                filtered = filtered + [item]  # Inefficient concatenation
        return filtered
    
    def inefficient_membership_testing(self, items, search_items):
        """
        INEFFICIENT: Using list for membership testing.
        Time Complexity: O(n*m) where n=len(items), m=len(search_items)
        """
        found = []
        for search_item in search_items:
            if search_item in items:  # O(n) lookup in list
                found.append(search_item)
        return found
    
    def repeated_computation(self, n):
        """
        INEFFICIENT: Computing the same expensive value repeatedly without caching.
        """
        result = []
        for i in range(n):
            # Expensive computation done repeatedly
            value = self._expensive_calculation(i % 10)
            result.append(value)
        return result
    
    def _expensive_calculation(self, n):
        """Simulate expensive calculation."""
        # Inefficient recursive fibonacci without memoization
        if n <= 1:
            return n
        return self._expensive_calculation(n-1) + self._expensive_calculation(n-2)
    
    def inefficient_file_reading(self, filename):
        """
        INEFFICIENT: Reading file line by line when processing all at once.
        Opens and closes file multiple times.
        """
        lines = []
        # Reading line by line unnecessarily
        with open(filename, 'r') as f:
            for line in f:
                lines.append(line.strip())
        
        # Processing requires reopening file
        processed = []
        with open(filename, 'r') as f:
            for line in f:
                processed.append(line.upper().strip())
        
        return processed
    
    def nested_loops_without_break(self, items):
        """
        INEFFICIENT: Not using early exit in nested loops.
        """
        pairs = []
        for i in range(len(items)):
            for j in range(len(items)):
                if items[i] + items[j] == 10:
                    pairs.append((items[i], items[j]))
                    # Should break here if only finding first match
        return pairs
    
    def inefficient_json_parsing(self, json_strings):
        """
        INEFFICIENT: Parsing JSON repeatedly instead of batch processing.
        """
        results = []
        for json_str in json_strings:
            try:
                data = json.loads(json_str)
                results.append(data)
            except:
                pass  # Bare except is also bad practice
        return results
    
    def inefficient_dictionary_access(self, data_dict, keys):
        """
        INEFFICIENT: Not using dict.get() with defaults, causing multiple lookups.
        """
        results = []
        for key in keys:
            if key in data_dict:  # First lookup
                value = data_dict[key]  # Second lookup
                if value is not None:
                    results.append(value)
            else:
                results.append(0)  # Default value
        return results


def simulate_n_plus_one_query():
    """
    INEFFICIENT: Simulates N+1 query problem common in database operations.
    """
    # Simulating database records
    users = [{'id': i, 'name': f'User{i}'} for i in range(100)]
    
    # Inefficient: Making separate "query" for each user's posts
    all_posts = []
    for user in users:
        # This simulates a separate database query for each user
        posts = [{'user_id': user['id'], 'content': f'Post {j}'} for j in range(5)]
        all_posts.extend(posts)
    
    return all_posts


def inefficient_data_structure_choice():
    """
    INEFFICIENT: Using wrong data structure for the task.
    Using list for frequent removals from middle.
    """
    items = list(range(1000))
    
    # Removing items from beginning is O(n) for each removal
    while len(items) > 500:
        items.pop(0)  # Very inefficient for lists
    
    return items


if __name__ == "__main__":
    processor = SlowDataProcessor()
    
    print("Running slow code examples...")
    
    # Test inefficient string concatenation
    start = time.time()
    result = processor.inefficient_string_concatenation(range(1000))
    print(f"String concatenation took: {time.time() - start:.4f}s")
    
    # Test inefficient list building
    start = time.time()
    result = processor.inefficient_list_building(1000)
    print(f"List building took: {time.time() - start:.4f}s")
    
    # Test repeated computation
    start = time.time()
    result = processor.repeated_computation(100)
    print(f"Repeated computation took: {time.time() - start:.4f}s")
    
    print("\nAll slow examples completed.")
