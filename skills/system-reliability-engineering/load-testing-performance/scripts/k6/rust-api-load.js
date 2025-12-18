/**
 * k6 Load Test for Rust API
 * 
 * Optimized load test for Rust backend APIs.
 * Expects lower latency due to Rust performance.
 * 
 * Usage:
 *   k6 run rust-api-load.js
 *   k6 run rust-api-load.js --env BASE_URL=http://localhost:8080
 */

import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate, Trend } from 'k6/metrics';

const errorRate = new Rate('errors');
const requestDuration = new Trend('request_duration');

export const options = {
  stages: [
    { duration: '2m', target: 100 },
    { duration: '5m', target: 100 },
    { duration: '2m', target: 200 },
    { duration: '5m', target: 200 },
    { duration: '2m', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(95)<50', 'p(99)<100'], // Rust should be faster
    http_req_failed: ['rate<0.01'],
  },
};

export default function () {
  const baseUrl = __ENV.BASE_URL || 'http://localhost:8080';
  
  // Test health endpoint
  const healthCheck = http.get(`${baseUrl}/health`, {
    tags: { name: 'HealthCheck' },
  });
  check(healthCheck, {
    'health check status 200': (r) => r.status === 200,
  });

  // Test API endpoint
  const startTime = Date.now();
  const response = http.get(`${baseUrl}/api/users`, {
    headers: {
      'Content-Type': 'application/json',
    },
    tags: { name: 'GetUsers' },
  });
  
  const duration = Date.now() - startTime;
  
  const success = check(response, {
    'status is 200': (r) => r.status === 200,
    'response time < 50ms': (r) => r.timings.duration < 50,
    'has users': (r) => {
      try {
        const data = JSON.parse(r.body);
        return data.users && data.users.length > 0;
      } catch {
        return false;
      }
    },
  });

  errorRate.add(!success);
  requestDuration.add(duration);

  sleep(1);
}

