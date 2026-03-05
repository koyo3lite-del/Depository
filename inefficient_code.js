/**
 * JavaScript module with performance issues
 * Demonstrates common performance anti-patterns in Node.js/JavaScript
 */

/**
 * Process array with inefficient loops
 * Inefficiency 1: Multiple iterations over same data
 */
function processItems(items) {
    // First pass: filter
    const filtered = [];
    for (let i = 0; i < items.length; i++) {
        if (items[i].active) {
            filtered.push(items[i]);
        }
    }
    
    // Second pass: map
    const mapped = [];
    for (let i = 0; i < filtered.length; i++) {
        mapped.push({
            ...filtered[i],
            processed: true
        });
    }
    
    // Third pass: sort
    const sorted = [];
    for (let i = 0; i < mapped.length; i++) {
        sorted.push(mapped[i]);
    }
    sorted.sort((a, b) => a.id - b.id);
    
    return sorted;
}

/**
 * Find duplicates with O(n²) complexity
 * Inefficiency 2: Nested loops
 */
function findDuplicates(arr) {
    const duplicates = [];
    for (let i = 0; i < arr.length; i++) {
        for (let j = i + 1; j < arr.length; j++) {
            if (arr[i] === arr[j] && !duplicates.includes(arr[i])) {
                duplicates.push(arr[i]);
            }
        }
    }
    return duplicates;
}

/**
 * Inefficient DOM manipulation
 * Inefficiency 3: Multiple reflows and repaints
 */
function updateList(items) {
    const container = document.getElementById('list-container');
    
    // Clearing items one by one
    while (container.firstChild) {
        container.removeChild(container.firstChild);
    }
    
    // Adding items one by one (causes multiple reflows)
    for (let i = 0; i < items.length; i++) {
        const div = document.createElement('div');
        div.textContent = items[i];
        container.appendChild(div);  // Reflow on each append
    }
}

/**
 * Inefficient string building
 * Inefficiency 4: String concatenation in loop
 */
function buildHTML(data) {
    let html = '';
    for (let i = 0; i < data.length; i++) {
        html += '<div class="item">';
        html += '<h3>' + data[i].title + '</h3>';
        html += '<p>' + data[i].description + '</p>';
        html += '</div>';
    }
    return html;
}

/**
 * Inefficient array operations
 * Inefficiency 5: Using wrong array methods
 */
function filterAndCount(numbers, threshold) {
    let count = 0;
    const filtered = [];
    
    // Inefficient: manual iteration when array methods exist
    for (let i = 0; i < numbers.length; i++) {
        if (numbers[i] > threshold) {
            filtered.push(numbers[i]);
            count++;
        }
    }
    
    return { filtered, count };
}

/**
 * Memory leak through closure
 * Inefficiency 6: Unintentional closure retention
 */
function createProcessor(largeData) {
    const cache = new Map();
    
    return {
        process: function(key) {
            // Closure holds reference to largeData even if not needed
            if (cache.has(key)) {
                return cache.get(key);
            }
            const result = largeData[key];
            cache.set(key, result);
            return result;
        }
    };
}

/**
 * Inefficient object operations
 * Inefficiency 7: Deep copying manually
 */
function cloneObjects(objects) {
    const cloned = [];
    
    for (let i = 0; i < objects.length; i++) {
        const obj = {};
        // Manual property copy
        for (const key in objects[i]) {
            if (objects[i].hasOwnProperty(key)) {
                if (typeof objects[i][key] === 'object' && objects[i][key] !== null) {
                    obj[key] = JSON.parse(JSON.stringify(objects[i][key]));
                } else {
                    obj[key] = objects[i][key];
                }
            }
        }
        cloned.push(obj);
    }
    
    return cloned;
}

/**
 * Inefficient async operations
 * Inefficiency 8: Sequential async calls
 */
async function fetchUserData(userIds) {
    const users = [];
    
    // Each request waits for previous to complete
    for (let i = 0; i < userIds.length; i++) {
        const response = await fetch(`/api/users/${userIds[i]}`);
        const user = await response.json();
        users.push(user);
    }
    
    return users;
}

/**
 * Inefficient event handling
 * Inefficiency 9: Multiple event listeners instead of delegation
 */
function attachClickHandlers(items) {
    items.forEach((item, index) => {
        const element = document.getElementById(`item-${index}`);
        element.addEventListener('click', function() {
            console.log(`Clicked item ${index}`);
            // Handler function
        });
    });
}

/**
 * Poor cache implementation
 * Inefficiency 10: Array-based cache instead of Map/Object
 */
class SimpleCache {
    constructor() {
        this.cache = [];  // Using array for O(n) lookups
    }
    
    get(key) {
        for (let i = 0; i < this.cache.length; i++) {
            if (this.cache[i].key === key) {
                return this.cache[i].value;
            }
        }
        return null;
    }
    
    set(key, value) {
        // O(n) search to check if key exists
        for (let i = 0; i < this.cache.length; i++) {
            if (this.cache[i].key === key) {
                this.cache[i].value = value;
                return;
            }
        }
        this.cache.push({ key, value });
    }
}

/**
 * Inefficient data transformation
 * Inefficiency 11: Multiple passes and intermediate arrays
 */
function transformData(data) {
    // First pass: extract values
    const values = [];
    for (let i = 0; i < data.length; i++) {
        values.push(data[i].value);
    }
    
    // Second pass: filter
    const filtered = [];
    for (let i = 0; i < values.length; i++) {
        if (values[i] > 0) {
            filtered.push(values[i]);
        }
    }
    
    // Third pass: square
    const squared = [];
    for (let i = 0; i < filtered.length; i++) {
        squared.push(filtered[i] * filtered[i]);
    }
    
    // Fourth pass: sum
    let sum = 0;
    for (let i = 0; i < squared.length; i++) {
        sum += squared[i];
    }
    
    return sum;
}

/**
 * Inefficient regex usage
 * Inefficiency 12: Creating regex in loop
 */
function validateEmails(emails) {
    const valid = [];
    
    for (let i = 0; i < emails.length; i++) {
        // Creating new regex object in each iteration
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (emailRegex.test(emails[i])) {
            valid.push(emails[i]);
        }
    }
    
    return valid;
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
    SimpleCache,
    transformData,
    validateEmails
};
