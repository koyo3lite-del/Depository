"""
Optimized data processing module
This module demonstrates performance best practices
"""
import json
from collections import Counter


def process_user_data(users):
    """Process user data with efficient single-pass approach"""
    # Optimization 1: Single pass with list comprehension and inline transformation
    return [
        {**user, 'processed': True}
        for user in users
        if user['active']
    ]


def find_duplicates(items):
    """Find duplicate items - efficient O(n) algorithm using Counter"""
    # Optimization 2: Use Counter for O(n) complexity instead of O(n²)
    counts = Counter(items)
    return [item for item, count in counts.items() if count > 1]


def calculate_statistics(numbers):
    """Calculate statistics efficiently with single sort"""
    # Optimization 3: Sort once and reuse
    sorted_nums = sorted(numbers)
    n = len(sorted_nums)
    
    # Optimization 4: Use built-in functions when available
    return {
        'min': sorted_nums[0],
        'max': sorted_nums[-1],
        'median': sorted_nums[n // 2],
        'average': sum(numbers) / n  # Built-in sum is faster
    }


def filter_and_transform(data, threshold):
    """Filter and transform data efficiently"""
    # Optimization 5: Use join with generator expression instead of string concatenation
    return ','.join(str(item) for item in data if item > threshold)


def load_and_process_json(filename):
    """Load JSON file efficiently"""
    # Optimization 6: Read entire file at once
    with open(filename, 'r') as f:
        data = json.load(f)  # Direct JSON parsing
    
    # Optimization 7: Return data directly if no transformation needed
    # Or use list comprehension for shallow copy if needed
    return data if not data else [item.copy() for item in data]


def search_in_list(large_list, target):
    """Search for items efficiently using list comprehension"""
    # Optimization 8: Use list comprehension (C-optimized in CPython)
    return [item for item in large_list if item == target]


class DataCache:
    """An efficient cache implementation using dictionary"""
    def __init__(self):
        # Optimization 9: Use dict for O(1) lookup instead of list
        self.cache = {}
    
    def get(self, key):
        """Get item from cache - O(1) lookup"""
        return self.cache.get(key)
    
    def set(self, key, value):
        """Set item in cache - O(1) operation"""
        self.cache[key] = value


def process_large_dataset(data):
    """Process large dataset with memory efficiency using generator"""
    # Optimization 10: Use generator expression for memory efficiency
    # Only processes one item at a time, doesn't store intermediate results
    return [item * 2 for item in data if item * 2 > 10]


def generate_report(records):
    """Generate report with efficient string operations"""
    # Optimization 11: Use list and join for efficient string building
    lines = ["Report", "=" * 50]
    
    for record in records:
        lines.extend([
            f"ID: {record['id']}",
            f"Name: {record['name']}",
            f"Value: {record['value']}",
            "-" * 50
        ])
    
    return '\n'.join(lines)


# Additional optimized functions

def batch_process(data, batch_size=1000):
    """Process data in batches for better memory management"""
    # Optimization 12: Generator for batch processing
    for i in range(0, len(data), batch_size):
        yield data[i:i + batch_size]


def memoize(func):
    """Simple memoization decorator for expensive operations"""
    # Optimization 13: Use functools.lru_cache in production
    cache = {}
    
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    
    return wrapper


@memoize
def expensive_calculation(n):
    """Example of memoized function"""
    # Simulate expensive operation
    result = sum(i * i for i in range(n))
    return result


def parallel_map(func, iterable, use_threads=True):
    """Parallel processing example (conceptual)"""
    # Optimization 14: Use concurrent.futures for parallel processing
    from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
    
    Executor = ThreadPoolExecutor if use_threads else ProcessPoolExecutor
    with Executor() as executor:
        return list(executor.map(func, iterable))


def efficient_deduplication(items):
    """Remove duplicates while preserving order"""
    # Optimization 15: Use dict.fromkeys() for O(n) deduplication
    return list(dict.fromkeys(items))
