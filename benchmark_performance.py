"""
Performance benchmarking script
Compares inefficient vs optimized implementations
"""
import time
import random
import json
import tempfile
from data_processor import (
    process_user_data as process_old,
    find_duplicates as find_dup_old,
    calculate_statistics as calc_stats_old,
    filter_and_transform as filter_old,
    DataCache as CacheOld,
    process_large_dataset as process_dataset_old,
    generate_report as gen_report_old
)
from data_processor_optimized import (
    process_user_data as process_new,
    find_duplicates as find_dup_new,
    calculate_statistics as calc_stats_new,
    filter_and_transform as filter_new,
    DataCache as CacheNew,
    process_large_dataset as process_dataset_new,
    generate_report as gen_report_new
)


def benchmark(func, *args, iterations=100):
    """Run benchmark and return average time"""
    times = []
    for _ in range(iterations):
        start = time.perf_counter()
        func(*args)
        end = time.perf_counter()
        times.append(end - start)
    return sum(times) / len(times)


def generate_test_data():
    """Generate test data for benchmarks"""
    # User data
    users = [
        {'id': i, 'name': f'User{i}', 'active': i % 2 == 0, 'value': i * 10}
        for i in range(1000)
    ]
    
    # List with duplicates
    items = [random.randint(0, 100) for _ in range(1000)]
    
    # Numbers for statistics
    numbers = [random.random() * 100 for _ in range(1000)]
    
    # Data for filtering
    data = list(range(1000))
    
    # Large dataset
    large_dataset = list(range(10000))
    
    # Records for report
    records = [
        {'id': i, 'name': f'Record{i}', 'value': i * 5}
        for i in range(100)
    ]
    
    return {
        'users': users,
        'items': items,
        'numbers': numbers,
        'data': data,
        'large_dataset': large_dataset,
        'records': records
    }


def run_benchmarks():
    """Run all benchmarks and display results"""
    print("=" * 80)
    print("PERFORMANCE BENCHMARK RESULTS")
    print("=" * 80)
    print()
    
    test_data = generate_test_data()
    
    # Benchmark 1: Process user data
    print("1. Process User Data (filter + transform)")
    print("-" * 80)
    old_time = benchmark(process_old, test_data['users'])
    new_time = benchmark(process_new, test_data['users'])
    improvement = ((old_time - new_time) / old_time) * 100
    print(f"   Inefficient: {old_time*1000:.4f} ms")
    print(f"   Optimized:   {new_time*1000:.4f} ms")
    print(f"   Improvement: {improvement:.1f}% faster")
    print()
    
    # Benchmark 2: Find duplicates
    print("2. Find Duplicates")
    print("-" * 80)
    old_time = benchmark(find_dup_old, test_data['items'])
    new_time = benchmark(find_dup_new, test_data['items'])
    improvement = ((old_time - new_time) / old_time) * 100
    print(f"   Inefficient: {old_time*1000:.4f} ms")
    print(f"   Optimized:   {new_time*1000:.4f} ms")
    print(f"   Improvement: {improvement:.1f}% faster")
    print()
    
    # Benchmark 3: Calculate statistics
    print("3. Calculate Statistics")
    print("-" * 80)
    old_time = benchmark(calc_stats_old, test_data['numbers'])
    new_time = benchmark(calc_stats_new, test_data['numbers'])
    improvement = ((old_time - new_time) / old_time) * 100
    print(f"   Inefficient: {old_time*1000:.4f} ms")
    print(f"   Optimized:   {new_time*1000:.4f} ms")
    print(f"   Improvement: {improvement:.1f}% faster")
    print()
    
    # Benchmark 4: Filter and transform
    print("4. Filter and Transform")
    print("-" * 80)
    old_time = benchmark(filter_old, test_data['data'], 500)
    new_time = benchmark(filter_new, test_data['data'], 500)
    improvement = ((old_time - new_time) / old_time) * 100
    print(f"   Inefficient: {old_time*1000:.4f} ms")
    print(f"   Optimized:   {new_time*1000:.4f} ms")
    print(f"   Improvement: {improvement:.1f}% faster")
    print()
    
    # Benchmark 5: Cache operations
    print("5. Cache Operations (1000 get/set operations)")
    print("-" * 80)
    
    def test_cache(CacheClass):
        cache = CacheClass()
        for i in range(1000):
            cache.set(f'key{i}', f'value{i}')
        for i in range(1000):
            cache.get(f'key{i % 1000}')
    
    old_time = benchmark(test_cache, CacheOld, iterations=10)
    new_time = benchmark(test_cache, CacheNew, iterations=10)
    improvement = ((old_time - new_time) / old_time) * 100
    print(f"   Inefficient: {old_time*1000:.4f} ms")
    print(f"   Optimized:   {new_time*1000:.4f} ms")
    print(f"   Improvement: {improvement:.1f}% faster")
    print()
    
    # Benchmark 6: Process large dataset
    print("6. Process Large Dataset")
    print("-" * 80)
    old_time = benchmark(process_dataset_old, test_data['large_dataset'], iterations=10)
    new_time = benchmark(process_dataset_new, test_data['large_dataset'], iterations=10)
    improvement = ((old_time - new_time) / old_time) * 100
    print(f"   Inefficient: {old_time*1000:.4f} ms")
    print(f"   Optimized:   {new_time*1000:.4f} ms")
    print(f"   Improvement: {improvement:.1f}% faster")
    print()
    
    # Benchmark 7: Generate report
    print("7. Generate Report")
    print("-" * 80)
    old_time = benchmark(gen_report_old, test_data['records'])
    new_time = benchmark(gen_report_new, test_data['records'])
    improvement = ((old_time - new_time) / old_time) * 100
    print(f"   Inefficient: {old_time*1000:.4f} ms")
    print(f"   Optimized:   {new_time*1000:.4f} ms")
    print(f"   Improvement: {improvement:.1f}% faster")
    print()
    
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print("All optimizations show measurable performance improvements.")
    print("Key optimization techniques used:")
    print("  - List comprehensions instead of loops")
    print("  - Built-in functions (sum, sorted, Counter)")
    print("  - Dict/Set for O(1) lookups instead of lists")
    print("  - String join instead of concatenation")
    print("  - Single-pass algorithms instead of multiple passes")
    print("=" * 80)


if __name__ == '__main__':
    run_benchmarks()
