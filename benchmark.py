#!/usr/bin/env python3
"""
Visual performance comparison script.
Runs all benchmarks and displays results in an easy-to-read format.
"""

import time
import sys
from slow_code_example import SlowDataProcessor, simulate_n_plus_one_query, inefficient_data_structure_choice
from optimized_code_example import OptimizedDataProcessor, optimized_query_with_join, efficient_data_structure_choice


def format_time(seconds):
    """Format time in appropriate units."""
    if seconds < 0.001:
        return f"{seconds * 1000000:.2f} μs"
    elif seconds < 1:
        return f"{seconds * 1000:.2f} ms"
    else:
        return f"{seconds:.2f} s"


def print_header():
    """Print benchmark header."""
    print("=" * 80)
    print(" " * 20 + "PERFORMANCE OPTIMIZATION BENCHMARKS")
    print("=" * 80)
    print()


def print_benchmark_result(name, slow_time, fast_time, test_size):
    """Print a single benchmark result."""
    speedup = slow_time / fast_time if fast_time > 0 else float('inf')
    
    print(f"\n{name}")
    print("-" * 80)
    print(f"  Test size:      {test_size:,}")
    print(f"  Slow version:   {format_time(slow_time)}")
    print(f"  Fast version:   {format_time(fast_time)}")
    print(f"  Speedup:        {speedup:.2f}x faster")
    
    # Visual bar chart
    bar_length = 50
    if speedup > 1:
        slow_bar = "█" * bar_length
        fast_bar = "█" * max(1, int(bar_length / speedup))
        print(f"  Visual:         Slow: {slow_bar}")
        print(f"                  Fast: {fast_bar}")
    
    return speedup


def run_benchmarks():
    """Run all performance benchmarks."""
    print_header()
    
    slow_processor = SlowDataProcessor()
    fast_processor = OptimizedDataProcessor()
    
    speedups = []
    
    # 1. String Concatenation
    print("\n📊 BENCHMARK 1: String Concatenation")
    test_size = 1000
    items = list(range(test_size))
    
    start = time.time()
    slow_processor.inefficient_string_concatenation(items)
    slow_time = time.time() - start
    
    start = time.time()
    fast_processor.efficient_string_concatenation(items)
    fast_time = time.time() - start
    
    speedup = print_benchmark_result("String Concatenation", slow_time, fast_time, test_size)
    speedups.append(("String Concatenation", speedup))
    
    # 2. List Building
    print("\n\n📊 BENCHMARK 2: List Building")
    test_size = 1000
    
    start = time.time()
    slow_processor.inefficient_list_building(test_size)
    slow_time = time.time() - start
    
    start = time.time()
    fast_processor.efficient_list_building(test_size)
    fast_time = time.time() - start
    
    speedup = print_benchmark_result("List Building", slow_time, fast_time, test_size)
    speedups.append(("List Building", speedup))
    
    # 3. Membership Testing
    print("\n\n📊 BENCHMARK 3: Membership Testing")
    items = list(range(1000))
    search_items = list(range(500, 1500))
    test_size = len(items) * len(search_items)
    
    start = time.time()
    slow_processor.inefficient_membership_testing(items, search_items)
    slow_time = time.time() - start
    
    start = time.time()
    fast_processor.efficient_membership_testing(items, search_items)
    fast_time = time.time() - start
    
    speedup = print_benchmark_result("Membership Testing", slow_time, fast_time, test_size)
    speedups.append(("Membership Testing", speedup))
    
    # 4. Filtering
    print("\n\n📊 BENCHMARK 4: List Filtering")
    data = list(range(1000))
    test_size = len(data)
    
    start = time.time()
    slow_processor.unnecessary_list_copies(data)
    slow_time = time.time() - start
    
    start = time.time()
    fast_processor.efficient_filtering(data)
    fast_time = time.time() - start
    
    speedup = print_benchmark_result("List Filtering", slow_time, fast_time, test_size)
    speedups.append(("List Filtering", speedup))
    
    # 5. Cached Computation
    print("\n\n📊 BENCHMARK 5: Cached Computation (Fibonacci)")
    test_size = 100
    
    start = time.time()
    slow_processor.repeated_computation(test_size)
    slow_time = time.time() - start
    
    fast_processor._efficient_calculation.cache_clear()
    start = time.time()
    fast_processor.cached_computation(test_size)
    fast_time = time.time() - start
    
    speedup = print_benchmark_result("Cached Computation", slow_time, fast_time, test_size)
    speedups.append(("Cached Computation", speedup))
    
    # 6. Nested Loops
    print("\n\n📊 BENCHMARK 6: Nested Loops (Finding Pairs)")
    items = list(range(500))
    test_size = len(items) ** 2
    
    start = time.time()
    slow_processor.nested_loops_without_break(items)
    slow_time = time.time() - start
    
    start = time.time()
    fast_processor.optimized_nested_loops(items)
    fast_time = time.time() - start
    
    speedup = print_benchmark_result("Nested Loops Optimization", slow_time, fast_time, test_size)
    speedups.append(("Nested Loops", speedup))
    
    # 7. Data Structure Choice
    print("\n\n📊 BENCHMARK 7: Data Structure Choice (Deque vs List)")
    test_size = 1000
    
    start = time.time()
    inefficient_data_structure_choice()
    slow_time = time.time() - start
    
    start = time.time()
    efficient_data_structure_choice()
    fast_time = time.time() - start
    
    speedup = print_benchmark_result("Data Structure Choice", slow_time, fast_time, test_size)
    speedups.append(("Data Structure", speedup))
    
    # Summary
    print("\n\n")
    print("=" * 80)
    print(" " * 30 + "SUMMARY")
    print("=" * 80)
    print()
    print("Optimization                      Speedup")
    print("-" * 80)
    
    total_speedup = 1.0
    for name, speedup in speedups:
        print(f"{name:35} {speedup:6.2f}x")
        total_speedup *= speedup
    
    avg_speedup = total_speedup ** (1.0 / len(speedups))
    
    print("-" * 80)
    print(f"{'Geometric Mean Speedup':35} {avg_speedup:6.2f}x")
    print("=" * 80)
    print()
    
    # Final message
    print("✅ All benchmarks completed successfully!")
    print(f"✨ Average performance improvement: {avg_speedup:.2f}x faster")
    print()
    print("💡 Tip: Run 'python test_performance.py' to verify correctness")
    print("📚 See README.md for detailed explanations of each optimization")
    print()


if __name__ == "__main__":
    try:
        run_benchmarks()
    except KeyboardInterrupt:
        print("\n\n⚠️  Benchmark interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error during benchmark: {e}")
        sys.exit(1)
