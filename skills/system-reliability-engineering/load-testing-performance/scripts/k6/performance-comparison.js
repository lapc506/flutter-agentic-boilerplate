/**
 * k6 Performance Comparison Test
 * 
 * Compare performance between different backend implementations.
 * 
 * Usage:
 *   k6 run performance-comparison.js
 *   k6 run performance-comparison.js \
 *     --env RUST_API=http://rust-api:8080 \
 *     --env NODE_API=http://node-api:3000
 */

import http from 'k6/http';
import { check } from 'k6';
import { Trend } from 'k6/metrics';

const rustApiDuration = new Trend('rust_api_duration');
const nodeApiDuration = new Trend('node_api_duration');

export const options = {
  vus: 50,
  duration: '5m',
};

export default function () {
  const rustApiUrl = __ENV.RUST_API || 'http://rust-api:8080';
  const nodeApiUrl = __ENV.NODE_API || 'http://node-api:3000';
  
  // Test Rust backend
  const rustStart = Date.now();
  const rustResponse = http.get(`${rustApiUrl}/api/data`);
  rustApiDuration.add(Date.now() - rustStart);
  
  check(rustResponse, {
    'rust api status 200': (r) => r.status === 200,
  });

  // Test Node.js backend (comparison)
  const nodeStart = Date.now();
  const nodeResponse = http.get(`${nodeApiUrl}/api/data`);
  nodeApiDuration.add(Date.now() - nodeStart);
  
  check(nodeResponse, {
    'node api status 200': (r) => r.status === 200,
  });
}

