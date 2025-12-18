/**
 * k6 Basic Load Test
 * 
 * Basic load test script for API endpoints.
 * 
 * Usage:
 *   k6 run basic-load.js
 *   k6 run basic-load.js --env API_TOKEN=your-token
 *   k6 run basic-load.js --env BASE_URL=https://api.example.com
 */

import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate, Trend } from 'k6/metrics';

// Custom metrics
const errorRate = new Rate('errors');
const requestDuration = new Trend('request_duration');

export const options = {
  stages: [
    { duration: '2m', target: 100 },  // Ramp up to 100 users
    { duration: '5m', target: 100 },  // Stay at 100 users
    { duration: '2m', target: 200 },  // Ramp up to 200 users
    { duration: '5m', target: 200 },  // Stay at 200 users
    { duration: '2m', target: 0 },    // Ramp down to 0 users
  ],
  thresholds: {
    http_req_duration: ['p(95)<500', 'p(99)<1000'], // 95% under 500ms, 99% under 1s
    http_req_failed: ['rate<0.01'],                  // Error rate under 1%
    errors: ['rate<0.01'],
  },
};

export default function () {
  const baseUrl = __ENV.BASE_URL || 'https://api.example.com';
  const apiToken = __ENV.API_TOKEN || '';

  // Test endpoint
  const response = http.get(`${baseUrl}/api/v1/users`, {
    headers: {
      'Authorization': apiToken ? `Bearer ${apiToken}` : '',
    },
  });

  // Check response
  const success = check(response, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
    'has data': (r) => {
      try {
        const body = JSON.parse(r.body);
        return body.data && body.data.length > 0;
      } catch {
        return false;
      }
    },
  });

  errorRate.add(!success);
  requestDuration.add(response.timings.duration);

  sleep(1);
}

