/**
 * Optimized JavaScript module
 * Demonstrates performance best practices in Node.js/JavaScript
 */

/**
 * Process array with efficient chaining
 * Optimization 1: Single pass using method chaining
 */
function processItems(items) {
    return items
        .filter(item => item.active)
        .map(item => ({ ...item, processed: true }))
        .sort((a, b) => a.id - b.id);
}

/**
 * Find duplicates with O(n) complexity using Set
 * Optimization 2: Use Set for O(n) instead of nested loops
 */
function findDuplicates(arr) {
    const seen = new Set();
    const duplicates = new Set();
    
    for (const item of arr) {
        if (seen.has(item)) {
            duplicates.add(item);
        } else {
            seen.add(item);
        }
    }
    
    return Array.from(duplicates);
}

/**
 * Efficient DOM manipulation
 * Optimization 3: Use DocumentFragment to minimize reflows
 */
function updateList(items) {
    const container = document.getElementById('list-container');
    
    // Clear efficiently
    container.innerHTML = '';
    
    // Build DOM in memory first using DocumentFragment
    const fragment = document.createDocumentFragment();
    
    for (const item of items) {
        const div = document.createElement('div');
        div.textContent = item;
        fragment.appendChild(div);
    }
    
    // Single reflow
    container.appendChild(fragment);
}

/**
 * Efficient string building using array join
 * Optimization 4: Use array and join instead of concatenation
 */
function buildHTML(data) {
    return data.map(item => 
        `<div class="item">
            <h3>${item.title}</h3>
            <p>${item.description}</p>
        </div>`
    ).join('');
}

/**
 * Efficient array operations using native methods
 * Optimization 5: Use built-in array methods
 */
function filterAndCount(numbers, threshold) {
    const filtered = numbers.filter(num => num > threshold);
    return { 
        filtered, 
        count: filtered.length 
    };
}

/**
 * Avoid memory leaks with proper closure management
 * Optimization 6: Only capture necessary variables
 */
function createProcessor(largeData) {
    const cache = new Map();
    
    return {
        process: function(key) {
            if (cache.has(key)) {
                return cache.get(key);
            }
            // Only access largeData when needed
            const result = largeData[key];
            cache.set(key, result);
            return result;
        },
        // Add cleanup method
        clear: function() {
            cache.clear();
        }
    };
}

/**
 * Efficient object operations using structured cloning
 * Optimization 7: Use structuredClone or spread for shallow copy
 */
function cloneObjects(objects) {
    // For shallow copy
    return objects.map(obj => ({ ...obj }));
    
    // For deep copy (modern browsers/Node.js 17+)
    // return structuredClone(objects);
}

/**
 * Efficient async operations with Promise.all
 * Optimization 8: Parallel async calls
 */
async function fetchUserData(userIds) {
    // All requests execute in parallel
    const promises = userIds.map(id => 
        fetch(`/api/users/${id}`).then(res => res.json())
    );
    
    return Promise.all(promises);
}

/**
 * Efficient event handling with delegation
 * Optimization 9: Use event delegation instead of multiple listeners
 */
function attachClickHandlers(items) {
    const container = document.getElementById('items-container');
    
    // Single listener on parent
    container.addEventListener('click', function(event) {
        const itemElement = event.target.closest('[data-item-index]');
        if (itemElement) {
            const index = itemElement.dataset.itemIndex;
            console.log(`Clicked item ${index}`);
        }
    });
}

/**
 * Efficient cache using Map
 * Optimization 10: Use Map for O(1) lookups
 */
class OptimizedCache {
    constructor(maxSize = 100) {
        this.cache = new Map();
        this.maxSize = maxSize;
    }
    
    get(key) {
        return this.cache.get(key);
    }
    
    set(key, value) {
        // Simple LRU: if at capacity, remove oldest
        if (this.cache.size >= this.maxSize && !this.cache.has(key)) {
            const firstKey = this.cache.keys().next().value;
            this.cache.delete(firstKey);
        }
        this.cache.set(key, value);
    }
    
    has(key) {
        return this.cache.has(key);
    }
    
    clear() {
        this.cache.clear();
    }
}

/**
 * Efficient data transformation with single pass
 * Optimization 11: Single reduce operation
 */
function transformData(data) {
    return data.reduce((sum, item) => {
        const value = item.value;
        return value > 0 ? sum + (value * value) : sum;
    }, 0);
}

/**
 * Efficient regex usage
 * Optimization 12: Create regex once outside loop
 */
function validateEmails(emails) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emails.filter(email => emailRegex.test(email));
}

/**
 * Additional optimizations
 */

/**
 * Debounce function for expensive operations
 * Optimization 13: Debounce to reduce function calls
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Throttle function for rate limiting
 * Optimization 14: Throttle to control execution rate
 */
function throttle(func, limit) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

/**
 * Memoization for expensive computations
 * Optimization 15: Cache results of pure functions
 */
function memoize(fn) {
    const cache = new Map();
    return function(...args) {
        const key = JSON.stringify(args);
        if (cache.has(key)) {
            return cache.get(key);
        }
        const result = fn.apply(this, args);
        cache.set(key, result);
        return result;
    };
}

/**
 * Lazy loading for large datasets
 * Optimization 16: Load data on demand
 */
function* lazyLoadData(data, chunkSize = 100) {
    for (let i = 0; i < data.length; i += chunkSize) {
        yield data.slice(i, i + chunkSize);
    }
}

/**
 * Efficient array chunking
 * Optimization 17: Process data in batches
 */
function chunkArray(array, size) {
    return Array.from(
        { length: Math.ceil(array.length / size) },
        (_, i) => array.slice(i * size, (i + 1) * size)
    );
}

module.exports = {
    processItems,
    findDuplicates,
    updateList,
    buildHTML,
    filterAndCount,
    createProcessor,
    cloneObjects,
    fetchUserData,
    attachClickHandlers,
    OptimizedCache,
    transformData,
    validateEmails,
    debounce,
    throttle,
    memoize,
    lazyLoadData,
    chunkArray
};
