/**
 * k6 Stress Test
 * 
 * Stress test to find system breaking points.
 * Gradually increases load beyond normal capacity.
 * 
 * Usage:
 *   k6 run stress-test.js
 *   k6 run stress-test.js --env BASE_URL=https://api.example.com
 */

import http from 'k6/http';
import { check } from 'k6';

export const options = {
  stages: [
    { duration: '2m', target: 100 },
    { duration: '5m', target: 100 },
    { duration: '2m', target: 200 },
    { duration: '5m', target: 200 },
    { duration: '2m', target: 300 },
    { duration: '5m', target: 300 },
    { duration: '2m', target: 400 },
    { duration: '5m', target: 400 },
    { duration: '10m', target: 0 }, // Recovery
  ],
  thresholds: {
    http_req_failed: ['rate<0.05'], // Allow up to 5% errors under stress
    http_req_duration: ['p(95)<2000'], // Relaxed under stress
  },
};

export default function () {
  const baseUrl = __ENV.BASE_URL || 'https://api.example.com';
  
  const response = http.get(`${baseUrl}/api/v1/data`);
  
  check(response, {
    'status is 200': (r) => r.status === 200,
  });
}

