/**
 * Example User Service with Custom Spans
 * 
 * Example service demonstrating custom spans and tracing.
 * 
 * Usage:
 *   const { getUserById } = require('./userService');
 *   const user = await getUserById('123');
 */

const { trace } = require('@opentelemetry/api');
const { SpanStatusCode } = require('@opentelemetry/api');

const tracer = trace.getTracer('user-service');

/**
 * Get user by ID with custom span.
 * 
 * @param {string} userId - User ID
 * @returns {Promise<Object>} User object
 */
async function getUserById(userId) {
  const span = tracer.startSpan('getUserById', {
    attributes: {
      'user.id': userId,
      'operation.type': 'read',
    },
  });

  try {
    span.addEvent('Fetching user from database');
    
    // Simulate database query
    const user = await fetchUserFromDatabase(userId);
    
    span.setAttribute('user.found', !!user);
    span.setStatus({ code: SpanStatusCode.OK });
    
    return user;
  } catch (error) {
    span.setStatus({
      code: SpanStatusCode.ERROR,
      message: error.message,
    });
    span.recordException(error);
    throw error;
  } finally {
    span.end();
  }
}

/**
 * Simulated database query.
 * 
 * @param {string} userId - User ID
 * @returns {Promise<Object>} User object
 */
async function fetchUserFromDatabase(userId) {
  // Simulate async database operation
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        id: userId,
        name: 'John Doe',
        email: 'john@example.com',
      });
    }, 100);
  });
}

module.exports = {
  getUserById,
};

