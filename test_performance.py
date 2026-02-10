"""
Test file demonstrating performance improvements.
Validates that optimized code produces same results but faster.
"""

import unittest
import time
import tempfile
import os
from slow_code_example import SlowDataProcessor, simulate_n_plus_one_query, inefficient_data_structure_choice
from optimized_code_example import (
    OptimizedDataProcessor, 
    optimized_query_with_join,
    efficient_data_structure_choice,
    LazyEvaluation
)


class PerformanceTest(unittest.TestCase):
    """Test that optimized code produces correct results and is faster."""
    
    def setUp(self):
        self.slow_processor = SlowDataProcessor()
        self.fast_processor = OptimizedDataProcessor()
        self.test_data = list(range(100))
    
    def test_string_concatenation_correctness(self):
        """Verify both implementations produce same result."""
        items = list(range(10))
        slow_result = self.slow_processor.inefficient_string_concatenation(items)
        fast_result = self.fast_processor.efficient_string_concatenation(items)
        self.assertEqual(slow_result, fast_result)
    
    def test_string_concatenation_performance(self):
        """Verify optimized version is significantly faster."""
        items = list(range(1000))
        
        start = time.time()
        self.slow_processor.inefficient_string_concatenation(items)
        slow_time = time.time() - start
        
        start = time.time()
        self.fast_processor.efficient_string_concatenation(items)
        fast_time = time.time() - start
        
        # Optimized should be at least 2x faster (conservative estimate)
        speedup = slow_time / fast_time
        print(f"\nString concatenation speedup: {speedup:.2f}x")
        self.assertGreater(speedup, 2.0, f"Expected speedup > 2x, got {speedup:.2f}x")
    
    def test_list_building_correctness(self):
        """Verify both implementations produce same result."""
        n = 100
        slow_result = self.slow_processor.inefficient_list_building(n)
        fast_result = self.fast_processor.efficient_list_building(n)
        self.assertEqual(slow_result, fast_result)
    
    def test_list_building_performance(self):
        """Verify optimized version is significantly faster."""
        n = 1000
        
        start = time.time()
        self.slow_processor.inefficient_list_building(n)
        slow_time = time.time() - start
        
        start = time.time()
        self.fast_processor.efficient_list_building(n)
        fast_time = time.time() - start
        
        speedup = slow_time / fast_time
        print(f"\nList building speedup: {speedup:.2f}x")
        self.assertGreater(speedup, 10.0, f"Expected speedup > 10x, got {speedup:.2f}x")
    
    def test_filtering_correctness(self):
        """Verify filtering produces same result."""
        data = list(range(100))
        slow_result = self.slow_processor.unnecessary_list_copies(data)
        fast_result = self.fast_processor.efficient_filtering(data)
        self.assertEqual(slow_result, fast_result)
    
    def test_membership_testing_correctness(self):
        """Verify membership testing produces same result."""
        items = list(range(100))
        search_items = list(range(50, 150))
        
        slow_result = self.slow_processor.inefficient_membership_testing(items, search_items)
        fast_result = self.fast_processor.efficient_membership_testing(items, search_items)
        
        self.assertEqual(sorted(slow_result), sorted(fast_result))
    
    def test_membership_testing_performance(self):
        """Verify optimized membership testing is much faster."""
        items = list(range(1000))
        search_items = list(range(500, 1500))
        
        start = time.time()
        self.slow_processor.inefficient_membership_testing(items, search_items)
        slow_time = time.time() - start
        
        start = time.time()
        self.fast_processor.efficient_membership_testing(items, search_items)
        fast_time = time.time() - start
        
        speedup = slow_time / fast_time
        print(f"\nMembership testing speedup: {speedup:.2f}x")
        self.assertGreater(speedup, 5.0, f"Expected speedup > 5x, got {speedup:.2f}x")
    
    def test_cached_computation_correctness(self):
        """Verify cached computation produces same results."""
        n = 50
        slow_result = self.slow_processor.repeated_computation(n)
        fast_result = self.fast_processor.cached_computation(n)
        self.assertEqual(slow_result, fast_result)
    
    def test_cached_computation_performance(self):
        """Verify cached computation is dramatically faster."""
        n = 100
        
        # Clear cache before timing
        self.fast_processor._efficient_calculation.cache_clear()
        
        start = time.time()
        self.slow_processor.repeated_computation(n)
        slow_time = time.time() - start
        
        self.fast_processor._efficient_calculation.cache_clear()
        start = time.time()
        self.fast_processor.cached_computation(n)
        fast_time = time.time() - start
        
        speedup = slow_time / fast_time
        print(f"\nCached computation speedup: {speedup:.2f}x")
        # This should have significant speedup due to memoization
        self.assertGreater(speedup, 5.0, f"Expected speedup > 5x, got {speedup:.2f}x")
    
    def test_file_reading_correctness(self):
        """Verify file reading produces same results."""
        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            temp_file = f.name
            f.write("line1\nline2\nline3\n")
        
        try:
            slow_result = self.slow_processor.inefficient_file_reading(temp_file)
            fast_result = self.fast_processor.efficient_file_reading(temp_file)
            self.assertEqual(slow_result, fast_result)
        finally:
            os.unlink(temp_file)
    
    def test_nested_loops_correctness(self):
        """Verify nested loops optimization produces valid results."""
        items = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        slow_result = self.slow_processor.nested_loops_without_break(items)
        fast_result = self.fast_processor.optimized_nested_loops(items)
        
        # Check that all pairs sum to 10
        for pair in fast_result:
            self.assertEqual(sum(pair), 10)
        
        # Fast version should find valid pairs (might be different order/count)
        self.assertGreater(len(fast_result), 0)
    
    def test_dictionary_access_correctness(self):
        """Verify dictionary access produces same results."""
        data_dict = {i: i*2 for i in range(100)}
        keys = list(range(0, 150, 3))
        
        slow_result = self.slow_processor.inefficient_dictionary_access(data_dict, keys)
        fast_result = self.fast_processor.efficient_dictionary_access(data_dict, keys)
        
        # Results should be equivalent (non-zero values)
        self.assertEqual(sorted(slow_result), sorted(fast_result))
    
    def test_query_optimization_correctness(self):
        """Verify query optimization produces same results."""
        slow_result = simulate_n_plus_one_query()
        fast_result = optimized_query_with_join()
        
        self.assertEqual(len(slow_result), len(fast_result))
        self.assertEqual(len(slow_result), 500)  # 100 users * 5 posts each
    
    def test_data_structure_choice_correctness(self):
        """Verify data structure choice produces same results."""
        slow_result = inefficient_data_structure_choice()
        fast_result = efficient_data_structure_choice()
        
        self.assertEqual(slow_result, fast_result)
        self.assertEqual(len(slow_result), 500)
    
    def test_data_structure_choice_performance(self):
        """Verify deque is faster than list for popleft operations."""
        start = time.time()
        inefficient_data_structure_choice()
        slow_time = time.time() - start
        
        start = time.time()
        efficient_data_structure_choice()
        fast_time = time.time() - start
        
        speedup = slow_time / fast_time
        print(f"\nData structure choice speedup: {speedup:.2f}x")
        self.assertGreater(speedup, 1.5, f"Expected speedup > 1.5x, got {speedup:.2f}x")
    
    def test_lazy_evaluation_correctness(self):
        """Verify lazy evaluation with generators works correctly."""
        lazy = LazyEvaluation()
        items = list(range(20))
        
        # Convert generator to list for comparison
        result = list(lazy.filter_and_transform(items))
        expected = [item * 2 for item in items if item % 2 == 0]
        
        self.assertEqual(result, expected)
    
    def test_lazy_evaluation_memory_efficiency(self):
        """Verify generator doesn't create intermediate list."""
        lazy = LazyEvaluation()
        items = range(1000000)  # Large range
        
        # Generator should not materialize the entire list
        gen = lazy.filter_and_transform(items)
        
        # We can process it item by item without loading all into memory
        first_five = []
        for i, item in enumerate(gen):
            if i >= 5:
                break
            first_five.append(item)
        
        self.assertEqual(len(first_five), 5)
        self.assertEqual(first_five, [0, 4, 8, 12, 16])


class AlgorithmComplexityTest(unittest.TestCase):
    """Test to verify algorithm complexity improvements."""
    
    def test_nested_loop_complexity(self):
        """Verify O(n) solution is much faster than O(n²) for large inputs."""
        slow_processor = SlowDataProcessor()
        fast_processor = OptimizedDataProcessor()
        
        items = list(range(500))
        
        start = time.time()
        slow_result = slow_processor.nested_loops_without_break(items)
        slow_time = time.time() - start
        
        start = time.time()
        fast_result = fast_processor.optimized_nested_loops(items)
        fast_time = time.time() - start
        
        speedup = slow_time / fast_time
        print(f"\nNested loops optimization speedup: {speedup:.2f}x")
        
        # Should show dramatic improvement for larger datasets
        self.assertGreater(speedup, 5.0, f"Expected speedup > 5x, got {speedup:.2f}x")


def run_performance_suite():
    """Run all performance tests and report results."""
    print("=" * 70)
    print("PERFORMANCE OPTIMIZATION TEST SUITE")
    print("=" * 70)
    
    # Run tests
    suite = unittest.TestLoader().loadTestsFromTestCase(PerformanceTest)
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(AlgorithmComplexityTest))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("=" * 70)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_performance_suite()
    exit(0 if success else 1)
