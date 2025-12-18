/**
 * k6 Advanced Scenarios Test
 * 
 * Advanced load test with multiple scenarios simulating different user behaviors.
 * 
 * Usage:
 *   k6 run advanced-scenarios.js
 *   k6 run advanced-scenarios.js --env SCENARIO=browse_products
 */

import http from 'k6/http';
import { check, sleep } from 'k6';
import { SharedArray } from 'k6/data';

// Shared test data (optional - create test-data/users.json)
// const users = new SharedArray('users', function () {
//   return JSON.parse(open('./test-data/users.json'));
// });

// Mock users for testing
const users = [
  { id: '1', email: 'user1@example.com' },
  { id: '2', email: 'user2@example.com' },
  { id: '3', email: 'user3@example.com' },
];

export const options = {
  scenarios: {
    // Browse products (high volume, low intensity)
    browse_products: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '5m', target: 100 },
        { duration: '10m', target: 100 },
        { duration: '5m', target: 0 },
      ],
      gracefulRampDown: '30s',
    },

    // Checkout (low volume, high intensity)
    checkout: {
      executor: 'constant-arrival-rate',
      rate: 10, // 10 iterations per second
      timeUnit: '1s',
      duration: '20m',
      preAllocatedVUs: 5,
      maxVUs: 20,
    },

    // Search (medium volume, medium intensity)
    search: {
      executor: 'shared-iterations',
      vus: 50,
      iterations: 10000,
      maxDuration: '30m',
    },
  },
  thresholds: {
    http_req_duration: ['p(95)<500'],
    http_req_failed: ['rate<0.01'],
    'http_req_duration{browse_products}': ['p(95)<300'],
    'http_req_duration{checkout}': ['p(95)<1000'],
  },
};

export default function () {
  const scenario = __ENV.SCENARIO || __VU;
  const baseUrl = __ENV.BASE_URL || 'https://api.example.com';
  
  // Determine scenario based on VU or environment variable
  const scenarioName = __ENV.SCENARIO || 
    (__VU <= 100 ? 'browse_products' : 
     __VU <= 120 ? 'checkout' : 'search');
  
  switch (scenarioName) {
    case 'browse_products':
      browseProducts(baseUrl);
      break;
    case 'checkout':
      checkout(baseUrl);
      break;
    case 'search':
      search(baseUrl);
      break;
  }
}

function browseProducts(baseUrl) {
  const response = http.get(`${baseUrl}/products`, {
    tags: { name: 'BrowseProducts' },
  });
  
  check(response, {
    'status is 200': (r) => r.status === 200,
  });
  
  sleep(Math.random() * 3 + 1); // Random sleep 1-4s
}

function checkout(baseUrl) {
  const user = users[Math.floor(Math.random() * users.length)];
  
  const response = http.post(
    `${baseUrl}/checkout`,
    JSON.stringify({
      userId: user.id,
      items: [{ productId: '123', quantity: 1 }],
    }),
    {
      headers: { 'Content-Type': 'application/json' },
      tags: { name: 'Checkout' },
    }
  );
  
  check(response, {
    'status is 200': (r) => r.status === 200,
    'checkout successful': (r) => {
      try {
        const body = JSON.parse(r.body);
        return body.orderId !== null && body.orderId !== undefined;
      } catch {
        return false;
      }
    },
  });
}

function search(baseUrl) {
  const query = ['laptop', 'phone', 'tablet'][Math.floor(Math.random() * 3)];
  
  const response = http.get(
    `${baseUrl}/search?q=${query}`,
    { tags: { name: 'Search' } }
  );
  
  check(response, {
    'status is 200': (r) => r.status === 200,
    'has results': (r) => {
      try {
        const body = JSON.parse(r.body);
        return body.results && body.results.length > 0;
      } catch {
        return false;
      }
    },
  });
  
  sleep(0.5);
}

