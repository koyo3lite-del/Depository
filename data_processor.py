"""
Data processing module with performance issues
This module demonstrates common performance anti-patterns
"""
import time
import json


def process_user_data(users):
    """Process user data with inefficient loops"""
    result = []
    # Inefficiency 1: Multiple passes through data
    for user in users:
        if user['active']:
            result.append(user)
    
    # Inefficiency 2: Unnecessary second loop
    final_result = []
    for user in result:
        user['processed'] = True
        final_result.append(user)
    
    return final_result


def find_duplicates(items):
    """Find duplicate items - inefficient O(n²) algorithm"""
    duplicates = []
    # Inefficiency 3: Nested loops creating O(n²) complexity
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if items[i] == items[j] and items[i] not in duplicates:
                duplicates.append(items[i])
    return duplicates


def calculate_statistics(numbers):
    """Calculate statistics with redundant operations"""
    # Inefficiency 4: Sorting multiple times
    sorted_nums = sorted(numbers)
    min_val = sorted_nums[0]
    
    sorted_nums = sorted(numbers)
    max_val = sorted_nums[-1]
    
    sorted_nums = sorted(numbers)
    median = sorted_nums[len(sorted_nums) // 2]
    
    # Inefficiency 5: Inefficient sum calculation
    total = 0
    for num in numbers:
        total += num
    average = total / len(numbers)
    
    return {
        'min': min_val,
        'max': max_val,
        'median': median,
        'average': average
    }


def filter_and_transform(data, threshold):
    """Filter and transform data inefficiently"""
    # Inefficiency 6: Building string with concatenation
    result_str = ""
    for item in data:
        if item > threshold:
            result_str = result_str + str(item) + ","
    
    return result_str.rstrip(',')


def load_and_process_json(filename):
    """Load JSON file inefficiently"""
    # Inefficiency 7: Reading file line by line when full read would work
    lines = []
    with open(filename, 'r') as f:
        for line in f:
            lines.append(line)
    
    content = ''.join(lines)
    data = json.loads(content)
    
    # Inefficiency 8: Deep copying when not needed
    result = []
    for item in data:
        new_item = {}
        for key in item:
            new_item[key] = item[key]
        result.append(new_item)
    
    return result


def search_in_list(large_list, target):
    """Search for items inefficiently"""
    # Inefficiency 9: Linear search on potentially large list
    found_items = []
    for item in large_list:
        if item == target:
            found_items.append(item)
    return found_items


class DataCache:
    """A poorly implemented cache"""
    def __init__(self):
        self.cache = []  # Inefficiency 10: Using list instead of dict for cache
    
    def get(self, key):
        """Get item from cache - O(n) lookup"""
        for item in self.cache:
            if item[0] == key:
                return item[1]
        return None
    
    def set(self, key, value):
        """Set item in cache - also O(n) to check existence"""
        # Remove if exists
        for i, item in enumerate(self.cache):
            if item[0] == key:
                self.cache.pop(i)
                break
        self.cache.append((key, value))


def process_large_dataset(data):
    """Process large dataset with memory inefficiency"""
    # Inefficiency 11: Loading everything into memory at once
    results = []
    intermediate = []
    
    for item in data:
        # Inefficiency 12: Unnecessary intermediate storage
        intermediate.append(item * 2)
    
    for item in intermediate:
        if item > 10:
            results.append(item)
    
    return results


def generate_report(records):
    """Generate report with inefficient string operations"""
    # Inefficiency 13: String concatenation in loop
    report = "Report\n"
    report += "=" * 50 + "\n"
    
    for record in records:
        report += f"ID: {record['id']}\n"
        report += f"Name: {record['name']}\n"
        report += f"Value: {record['value']}\n"
        report += "-" * 50 + "\n"
    
    return report
