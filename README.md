# Performance Optimization Guide

This repository demonstrates common performance anti-patterns in Python and their optimized solutions. Each example includes detailed explanations of the problem, solution, and expected performance improvements.

## Overview

This guide covers the following performance optimization topics:

1. **String Concatenation Optimization**
2. **Efficient List Operations**
3. **Proper Data Structure Selection**
4. **Membership Testing Optimization**
5. **Caching and Memoization**
6. **File I/O Best Practices**
7. **Algorithm Complexity Improvements**
8. **Batch Processing Patterns**
9. **Lazy Evaluation with Generators**
10. **Database Query Optimization (N+1 Problem)**

## Quick Start

```bash
# Run visual performance benchmarks with detailed comparison
python benchmark.py

# Run the slow code examples
python slow_code_example.py

# Run the optimized code examples with benchmarks
python optimized_code_example.py

# Run the comprehensive test suite
python test_performance.py
```

## Performance Issues and Solutions

### 1. String Concatenation (O(n²) → O(n))

**❌ Inefficient Pattern:**
```python
result = ""
for item in items:
    result = result + str(item) + ","  # Creates new string each time
```

**✅ Optimized Solution:**
```python
result = ",".join(str(item) for item in items)
```

**Performance Gain:** 10-100x faster for large lists
**Memory Savings:** Significantly reduced due to fewer temporary string objects

### 2. List Building (O(n²) → O(n))

**❌ Inefficient Pattern:**
```python
result = []
for i in range(n):
    result = result + [i]  # Creates new list each iteration
```

**✅ Optimized Solution:**
```python
result = list(range(n))  # Or use list comprehension
# Alternative: result = [i for i in range(n)]
```

**Performance Gain:** 100x faster for n=1000
**Why:** List concatenation with `+` creates a new list object each time, while `append()` or list comprehensions grow the list efficiently.

### 3. Membership Testing (O(n·m) → O(n+m))

**❌ Inefficient Pattern:**
```python
found = []
for search_item in search_items:
    if search_item in items:  # O(n) lookup in list
        found.append(search_item)
```

**✅ Optimized Solution:**
```python
items_set = set(items)  # O(n) to create set
found = [item for item in search_items if item in items_set]  # O(1) lookup
```

**Performance Gain:** 1000x faster for large lists
**Why:** Set lookup is O(1) on average vs O(n) for list lookup

### 4. Caching Expensive Computations

**❌ Inefficient Pattern:**
```python
def expensive_calculation(n):
    if n <= 1:
        return n
    return expensive_calculation(n-1) + expensive_calculation(n-2)
```

**✅ Optimized Solution:**
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def efficient_calculation(n):
    if n <= 1:
        return n
    return efficient_calculation(n-1) + efficient_calculation(n-2)
```

**Performance Gain:** Exponential speedup (O(2ⁿ) → O(n))
**Why:** Memoization prevents recalculating the same values repeatedly

### 5. File I/O Optimization

**❌ Inefficient Pattern:**
```python
# Reading file multiple times
lines = []
with open(filename, 'r') as f:
    for line in f:
        lines.append(line.strip())

processed = []
with open(filename, 'r') as f:  # Opening again!
    for line in f:
        processed.append(line.upper().strip())
```

**✅ Optimized Solution:**
```python
# Single pass processing
with open(filename, 'r') as f:
    processed = [line.upper().strip() for line in f]
```

**Performance Gain:** 2x faster, reduces I/O operations
**Why:** Single file open/close, single iteration

### 6. Algorithm Optimization (Finding Pairs)

**❌ Inefficient Pattern (O(n²)):**
```python
pairs = []
for i in range(len(items)):
    for j in range(len(items)):
        if items[i] + items[j] == 10:
            pairs.append((items[i], items[j]))
```

**✅ Optimized Solution (O(n)):**
```python
pairs = []
seen = set()
for item in items:
    complement = 10 - item
    if complement in seen:
        pairs.append((complement, item))
    seen.add(item)
```

**Performance Gain:** O(n) vs O(n²), 1000x faster for n=1000
**Why:** Single pass with hash table lookup instead of nested loops

### 7. Dictionary Access Optimization

**❌ Inefficient Pattern:**
```python
results = []
for key in keys:
    if key in data_dict:      # First lookup
        value = data_dict[key]  # Second lookup
        if value is not None:
            results.append(value)
```

**✅ Optimized Solution:**
```python
results = [data_dict.get(key, 0) for key in keys if data_dict.get(key, 0)]
# Or better yet:
results = [v for k in keys if (v := data_dict.get(k))]  # Python 3.8+
```

**Performance Gain:** 2x faster
**Why:** Single dictionary lookup instead of two

### 8. Data Structure Selection

**❌ Inefficient Pattern:**
```python
items = list(range(1000))
while len(items) > 500:
    items.pop(0)  # O(n) operation for lists
```

**✅ Optimized Solution:**
```python
from collections import deque

items = deque(range(1000))
while len(items) > 500:
    items.popleft()  # O(1) operation for deques
```

**Performance Gain:** 1000x faster for large lists
**Why:** Deques are optimized for operations at both ends

### 9. Lazy Evaluation with Generators

**Memory-Efficient Pattern:**
```python
def process_large_file(filename):
    """Generator that yields processed lines one at a time."""
    with open(filename, 'r') as f:
        for line in f:
            yield line.upper().strip()

# Use it:
for processed_line in process_large_file('huge_file.txt'):
    # Process one line at a time, not loading entire file
    handle_line(processed_line)
```

**Benefits:**
- Constant memory usage regardless of file size
- Start processing immediately without waiting for full load
- Can handle files larger than available RAM

### 10. N+1 Query Problem

**❌ Inefficient Pattern:**
```python
# Getting all users
users = User.query.all()

# Then making separate query for each user's posts
all_posts = []
for user in users:
    posts = Post.query.filter_by(user_id=user.id).all()  # N queries!
    all_posts.extend(posts)
```

**✅ Optimized Solution:**
```python
# Single query with JOIN
posts = Post.query.join(User).all()

# Or use eager loading:
users = User.query.options(joinedload(User.posts)).all()
```

**Performance Gain:** 100x faster for 100 users
**Why:** 1 database query instead of N+1 queries

## Performance Testing

### Visual Benchmarks

Run the comprehensive benchmark suite with visual results:

```bash
python benchmark.py
```

Sample output:
```
================================================================================
                    PERFORMANCE OPTIMIZATION BENCHMARKS
================================================================================

📊 BENCHMARK 1: String Concatenation
--------------------------------------------------------------------------------
  Test size:      1,000
  Slow version:   369.07 μs
  Fast version:   99.42 μs
  Speedup:        3.71x faster
  Visual:         Slow: ██████████████████████████████████████████████████
                  Fast: █████████████

...

================================================================================
                              SUMMARY
================================================================================
Optimization                      Speedup
--------------------------------------------------------------------------------
String Concatenation                  3.71x
List Building                        76.20x
Membership Testing                   80.31x
Nested Loops                        211.62x
--------------------------------------------------------------------------------
Geometric Mean Speedup               20.08x
================================================================================
```

### Detailed Comparison

Run the detailed benchmarks:

```python
python optimized_code_example.py
```

### Test Suite

Run the comprehensive test suite with correctness validation:

```python
python test_performance.py
```

## Best Practices Summary

### General Guidelines

1. **Choose the right data structure:**
   - `set` for membership testing
   - `deque` for queue operations
   - `dict` for key-value lookups
   - `list` for indexed access

2. **Use built-in functions and methods:**
   - They are highly optimized (written in C)
   - `join()`, `map()`, `filter()` are faster than manual loops

3. **Avoid premature optimization:**
   - Profile first, optimize bottlenecks
   - Readability sometimes trumps micro-optimizations
   - Use `cProfile` or `line_profiler` to identify slow code

4. **Cache expensive operations:**
   - Use `@lru_cache` for pure functions
   - Implement custom caching for complex scenarios
   - Consider Redis/Memcached for distributed caching

5. **Be memory conscious:**
   - Use generators for large datasets
   - Process in batches when possible
   - Clean up resources explicitly

6. **Database optimization:**
   - Use indexes on frequently queried columns
   - Avoid N+1 queries with proper JOINs
   - Use bulk operations for multiple inserts/updates
   - Consider connection pooling

7. **Algorithm complexity matters:**
   - O(n) is better than O(n²)
   - O(log n) is better than O(n)
   - O(1) is the goal for critical operations

## Profiling Tools

### Python Built-in Profilers

```python
import cProfile
import pstats

# Profile your code
cProfile.run('your_function()', 'profile_stats')

# Analyze results
stats = pstats.Stats('profile_stats')
stats.sort_stats('cumulative')
stats.print_stats(10)  # Top 10 slowest functions
```

### Line Profiler

```bash
pip install line_profiler

# Decorate functions with @profile
python -m line_profiler script.py.lprof
```

### Memory Profiler

```bash
pip install memory_profiler

# Decorate functions with @profile
python -m memory_profiler script.py
```

## Common Pitfalls

1. **Global variables** - Slow lookup, hard to optimize
2. **Importing inside functions** - Import at module level
3. **Using `+` for string concatenation** - Use `join()`
4. **Not using list comprehensions** - They're faster than loops
5. **Ignoring algorithmic complexity** - O(n²) won't scale
6. **Deep recursion** - Use iteration or tail recursion optimization
7. **Not closing resources** - Use context managers (`with` statement)

## Contributing

Found more performance patterns to document? Feel free to contribute!

## License

This is an educational resource demonstrating performance optimization techniques.

## References

- [Python Performance Tips](https://wiki.python.org/moin/PythonSpeed/PerformanceTips)
- [Time Complexity](https://www.bigocheatsheet.com/)
- [Python Data Structures](https://docs.python.org/3/tutorial/datastructures.html)
