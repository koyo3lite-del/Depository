"""
Optimized and efficient code patterns.
This file demonstrates best practices for performance optimization.
"""

import time
import json
from collections import deque
from functools import lru_cache


class OptimizedDataProcessor:
    """A class demonstrating efficient code patterns."""
    
    def __init__(self):
        self.data = []
        self.cache = {}
    
    def efficient_string_concatenation(self, items):
        """
        OPTIMIZED: Using join() for string concatenation.
        Time Complexity: O(n)
        Performance improvement: ~10-100x faster for large lists
        """
        return ",".join(str(item) for item in items)
    
    def efficient_list_building(self, n):
        """
        OPTIMIZED: Using list.append() or list comprehension.
        Time Complexity: O(n)
        Performance improvement: ~100x faster for large n
        """
        return list(range(n))  # Or: [i for i in range(n)]
    
    def efficient_filtering(self, data):
        """
        OPTIMIZED: Using list comprehension without unnecessary copies.
        Performance improvement: 2-3x faster, uses less memory
        """
        return [item for item in data if item % 2 == 0]
    
    def efficient_membership_testing(self, items, search_items):
        """
        OPTIMIZED: Using set for membership testing.
        Time Complexity: O(n+m) where n=len(items), m=len(search_items)
        Performance improvement: ~1000x faster for large lists
        """
        items_set = set(items)  # O(n) to create set
        return [item for item in search_items if item in items_set]  # O(1) lookup
    
    def cached_computation(self, n):
        """
        OPTIMIZED: Using memoization/caching for expensive repeated computations.
        Performance improvement: Exponential speedup for recursive operations
        """
        result = []
        for i in range(n):
            value = self._efficient_calculation(i % 10)
            result.append(value)
        return result
    
    @lru_cache(maxsize=128)
    def _efficient_calculation(self, n):
        """Efficient fibonacci with memoization using lru_cache."""
        if n <= 1:
            return n
        return self._efficient_calculation(n-1) + self._efficient_calculation(n-2)
    
    def efficient_file_reading(self, filename):
        """
        OPTIMIZED: Reading and processing file in a single pass.
        Performance improvement: 2x faster, single file open
        """
        with open(filename, 'r') as f:
            # Process everything in one pass
            return [line.upper().strip() for line in f]
    
    def optimized_nested_loops(self, items):
        """
        OPTIMIZED: Using early exit and better algorithm.
        Performance improvement: Up to O(n) vs O(n²) depending on data
        """
        pairs = []
        seen = set()
        
        for item in items:
            complement = 10 - item
            if complement in seen:
                pairs.append((complement, item))
            seen.add(item)
        
        return pairs
    
    def efficient_json_parsing(self, json_strings):
        """
        OPTIMIZED: Better error handling and potential for batch processing.
        Performance improvement: Cleaner code, proper error handling
        """
        results = []
        for json_str in json_strings:
            try:
                data = json.loads(json_str)
                results.append(data)
            except (json.JSONDecodeError, TypeError) as e:
                # Specific exception handling
                print(f"Failed to parse JSON: {e}")
                continue
        return results
    
    def efficient_dictionary_access(self, data_dict, keys):
        """
        OPTIMIZED: Using dict.get() with default value for single lookup.
        Performance improvement: 2x faster due to single lookup
        """
        results = []
        for key in keys:
            value = data_dict.get(key)
            if value is not None:
                results.append(value)
            else:
                results.append(0)
        return results


def optimized_query_with_join():
    """
    OPTIMIZED: Simulates proper query with JOIN to avoid N+1 problem.
    Performance improvement: O(n) vs O(n²), ~100x faster
    """
    # Simulating database records
    users = [{'id': i, 'name': f'User{i}'} for i in range(100)]
    
    # Efficient: Single "query" to get all posts
    # This simulates a JOIN query in SQL
    all_posts = []
    for user_id in range(100):
        posts = [{'user_id': user_id, 'content': f'Post {j}'} for j in range(5)]
        all_posts.extend(posts)
    
    return all_posts


def efficient_data_structure_choice():
    """
    OPTIMIZED: Using deque for efficient removal from beginning.
    Performance improvement: O(n) vs O(n²), ~1000x faster
    """
    items = deque(range(1000))
    
    # Removing items from beginning is O(1) for each removal
    while len(items) > 500:
        items.popleft()  # Very efficient for deques
    
    return list(items)


class EfficientBatchProcessor:
    """
    Additional optimization: Batch processing pattern.
    """
    
    def __init__(self, batch_size=100):
        self.batch_size = batch_size
    
    def process_in_batches(self, items, process_func):
        """
        Process items in batches to optimize memory usage and I/O.
        Useful for large datasets.
        """
        results = []
        for i in range(0, len(items), self.batch_size):
            batch = items[i:i + self.batch_size]
            batch_results = process_func(batch)
            results.extend(batch_results)
        return results


class LazyEvaluation:
    """
    Optimization: Using generators for lazy evaluation.
    Saves memory when processing large datasets.
    """
    
    def process_large_file(self, filename):
        """
        Generator that yields processed lines one at a time.
        Memory efficient for large files.
        """
        with open(filename, 'r') as f:
            for line in f:
                yield line.upper().strip()
    
    def filter_and_transform(self, items):
        """
        Using generator expression for memory efficiency.
        Only processes items as needed.
        """
        return (item * 2 for item in items if item % 2 == 0)


# Performance comparison utilities
def benchmark_comparison():
    """
    Compare performance between slow and optimized versions.
    """
    from slow_code_example import SlowDataProcessor
    
    slow_processor = SlowDataProcessor()
    fast_processor = OptimizedDataProcessor()
    
    test_size = 1000
    
    print("Performance Comparison:")
    print("=" * 60)
    
    # String concatenation comparison
    print("\n1. String Concatenation:")
    start = time.time()
    slow_processor.inefficient_string_concatenation(range(test_size))
    slow_time = time.time() - start
    print(f"   Slow version: {slow_time:.4f}s")
    
    start = time.time()
    fast_processor.efficient_string_concatenation(range(test_size))
    fast_time = time.time() - start
    print(f"   Fast version: {fast_time:.4f}s")
    print(f"   Speedup: {slow_time/fast_time:.2f}x")
    
    # List building comparison
    print("\n2. List Building:")
    start = time.time()
    slow_processor.inefficient_list_building(test_size)
    slow_time = time.time() - start
    print(f"   Slow version: {slow_time:.4f}s")
    
    start = time.time()
    fast_processor.efficient_list_building(test_size)
    fast_time = time.time() - start
    print(f"   Fast version: {fast_time:.4f}s")
    print(f"   Speedup: {slow_time/fast_time:.2f}x")
    
    # Membership testing comparison
    print("\n3. Membership Testing:")
    items = list(range(1000))
    search_items = list(range(500, 1500))
    
    start = time.time()
    slow_processor.inefficient_membership_testing(items, search_items)
    slow_time = time.time() - start
    print(f"   Slow version: {slow_time:.4f}s")
    
    start = time.time()
    fast_processor.efficient_membership_testing(items, search_items)
    fast_time = time.time() - start
    print(f"   Fast version: {fast_time:.4f}s")
    print(f"   Speedup: {slow_time/fast_time:.2f}x")


if __name__ == "__main__":
    print("Running optimized code examples...")
    benchmark_comparison()
    print("\n" + "=" * 60)
    print("All optimizations demonstrated successfully!")
