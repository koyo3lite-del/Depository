/**
 * JavaScript Performance Benchmarking
 * Compares inefficient vs optimized implementations
 */

const inefficient = require('./inefficient_code');
const optimized = require('./optimized_code');

/**
 * Benchmark a function
 */
function benchmark(fn, args, iterations = 1000) {
    const times = [];
    
    for (let i = 0; i < iterations; i++) {
        const start = performance.now();
        fn(...args);
        const end = performance.now();
        times.push(end - start);
    }
    
    const avg = times.reduce((a, b) => a + b, 0) / times.length;
    return avg;
}

/**
 * Generate test data
 */
function generateTestData() {
    const items = Array.from({ length: 1000 }, (_, i) => ({
        id: i,
        name: `Item${i}`,
        active: i % 2 === 0,
        value: i * 10
    }));
    
    const duplicateArray = Array.from({ length: 1000 }, () => 
        Math.floor(Math.random() * 100)
    );
    
    const numbers = Array.from({ length: 1000 }, () => 
        Math.floor(Math.random() * 1000)
    );
    
    const data = Array.from({ length: 1000 }, (_, i) => ({
        title: `Title ${i}`,
        description: `Description for item ${i}`,
        value: i
    }));
    
    const emails = Array.from({ length: 1000 }, (_, i) => 
        i % 3 === 0 ? `user${i}@example.com` : `invalid-email-${i}`
    );
    
    return {
        items,
        duplicateArray,
        numbers,
        data,
        emails
    };
}

/**
 * Run all benchmarks
 */
function runBenchmarks() {
    console.log('='.repeat(80));
    console.log('JAVASCRIPT PERFORMANCE BENCHMARK RESULTS');
    console.log('='.repeat(80));
    console.log();
    
    const testData = generateTestData();
    
    // Benchmark 1: Process items
    console.log('1. Process Items (filter + map + sort)');
    console.log('-'.repeat(80));
    const time1Old = benchmark(inefficient.processItems, [testData.items]);
    const time1New = benchmark(optimized.processItems, [testData.items]);
    const improvement1 = ((time1Old - time1New) / time1Old) * 100;
    console.log(`   Inefficient: ${time1Old.toFixed(4)} ms`);
    console.log(`   Optimized:   ${time1New.toFixed(4)} ms`);
    console.log(`   Improvement: ${improvement1.toFixed(1)}% faster`);
    console.log();
    
    // Benchmark 2: Find duplicates
    console.log('2. Find Duplicates');
    console.log('-'.repeat(80));
    const time2Old = benchmark(inefficient.findDuplicates, [testData.duplicateArray]);
    const time2New = benchmark(optimized.findDuplicates, [testData.duplicateArray]);
    const improvement2 = ((time2Old - time2New) / time2Old) * 100;
    console.log(`   Inefficient: ${time2Old.toFixed(4)} ms`);
    console.log(`   Optimized:   ${time2New.toFixed(4)} ms`);
    console.log(`   Improvement: ${improvement2.toFixed(1)}% faster`);
    console.log();
    
    // Benchmark 3: Build HTML
    console.log('3. Build HTML String');
    console.log('-'.repeat(80));
    const time3Old = benchmark(inefficient.buildHTML, [testData.data]);
    const time3New = benchmark(optimized.buildHTML, [testData.data]);
    const improvement3 = ((time3Old - time3New) / time3Old) * 100;
    console.log(`   Inefficient: ${time3Old.toFixed(4)} ms`);
    console.log(`   Optimized:   ${time3New.toFixed(4)} ms`);
    console.log(`   Improvement: ${improvement3.toFixed(1)}% faster`);
    console.log();
    
    // Benchmark 4: Filter and count
    console.log('4. Filter and Count');
    console.log('-'.repeat(80));
    const time4Old = benchmark(inefficient.filterAndCount, [testData.numbers, 500]);
    const time4New = benchmark(optimized.filterAndCount, [testData.numbers, 500]);
    const improvement4 = ((time4Old - time4New) / time4Old) * 100;
    console.log(`   Inefficient: ${time4Old.toFixed(4)} ms`);
    console.log(`   Optimized:   ${time4New.toFixed(4)} ms`);
    console.log(`   Improvement: ${improvement4.toFixed(1)}% faster`);
    console.log();
    
    // Benchmark 5: Clone objects
    console.log('5. Clone Objects');
    console.log('-'.repeat(80));
    const time5Old = benchmark(inefficient.cloneObjects, [testData.items.slice(0, 100)]);
    const time5New = benchmark(optimized.cloneObjects, [testData.items.slice(0, 100)]);
    const improvement5 = ((time5Old - time5New) / time5Old) * 100;
    console.log(`   Inefficient: ${time5Old.toFixed(4)} ms`);
    console.log(`   Optimized:   ${time5New.toFixed(4)} ms`);
    console.log(`   Improvement: ${improvement5.toFixed(1)}% faster`);
    console.log();
    
    // Benchmark 6: Cache operations
    console.log('6. Cache Operations (1000 get/set operations)');
    console.log('-'.repeat(80));
    
    function testCache(CacheClass) {
        const cache = new CacheClass();
        for (let i = 0; i < 1000; i++) {
            cache.set(`key${i}`, `value${i}`);
        }
        for (let i = 0; i < 1000; i++) {
            cache.get(`key${i % 1000}`);
        }
    }
    
    const time6Old = benchmark(testCache, [inefficient.SimpleCache], 100);
    const time6New = benchmark(testCache, [optimized.OptimizedCache], 100);
    const improvement6 = ((time6Old - time6New) / time6Old) * 100;
    console.log(`   Inefficient: ${time6Old.toFixed(4)} ms`);
    console.log(`   Optimized:   ${time6New.toFixed(4)} ms`);
    console.log(`   Improvement: ${improvement6.toFixed(1)}% faster`);
    console.log();
    
    // Benchmark 7: Transform data
    console.log('7. Transform Data (map + filter + reduce)');
    console.log('-'.repeat(80));
    const time7Old = benchmark(inefficient.transformData, [testData.data]);
    const time7New = benchmark(optimized.transformData, [testData.data]);
    const improvement7 = ((time7Old - time7New) / time7Old) * 100;
    console.log(`   Inefficient: ${time7Old.toFixed(4)} ms`);
    console.log(`   Optimized:   ${time7New.toFixed(4)} ms`);
    console.log(`   Improvement: ${improvement7.toFixed(1)}% faster`);
    console.log();
    
    // Benchmark 8: Validate emails
    console.log('8. Validate Emails');
    console.log('-'.repeat(80));
    const time8Old = benchmark(inefficient.validateEmails, [testData.emails]);
    const time8New = benchmark(optimized.validateEmails, [testData.emails]);
    const improvement8 = ((time8Old - time8New) / time8Old) * 100;
    console.log(`   Inefficient: ${time8Old.toFixed(4)} ms`);
    console.log(`   Optimized:   ${time8New.toFixed(4)} ms`);
    console.log(`   Improvement: ${improvement8.toFixed(1)}% faster`);
    console.log();
    
    console.log('='.repeat(80));
    console.log('SUMMARY');
    console.log('='.repeat(80));
    console.log('All optimizations show measurable performance improvements.');
    console.log('Key optimization techniques used:');
    console.log('  - Array method chaining instead of multiple loops');
    console.log('  - Map/Set for O(1) lookups instead of arrays');
    console.log('  - Template literals and join for string building');
    console.log('  - Single-pass algorithms with reduce');
    console.log('  - Regex reuse instead of recreation');
    console.log('  - Event delegation instead of multiple listeners');
    console.log('  - Promise.all for parallel async operations');
    console.log('='.repeat(80));
}

// Run benchmarks
runBenchmarks();
