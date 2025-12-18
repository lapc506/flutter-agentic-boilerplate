/**
 * Structured Logger for Node.js
 * 
 * Winston-based structured logger with JSON output for centralized logging.
 * 
 * Usage:
 *   const logger = require('./structured-logger');
 *   logger.info('User created', { userId: '123', email: 'user@example.com' });
 * 
 * Or as a module:
 *   const { createLogger } = require('./structured-logger');
 *   const logger = createLogger({ service: 'my-service' });
 */

const winston = require('winston');
const path = require('path');
const fs = require('fs');

// Ensure logs directory exists
const logsDir = path.join(process.cwd(), 'logs');
if (!fs.existsSync(logsDir)) {
  fs.mkdirSync(logsDir, { recursive: true });
}

/**
 * Create a structured logger instance.
 * 
 * @param {Object} options - Logger options
 * @param {string} options.service - Service name
 * @param {string} options.environment - Environment (development, production, etc.)
 * @param {string} options.version - Application version
 * @param {string} options.logLevel - Log level (default: 'info')
 * @returns {winston.Logger} Winston logger instance
 */
function createLogger(options = {}) {
  const {
    service = 'application',
    environment = process.env.NODE_ENV || 'development',
    version = process.env.APP_VERSION || '1.0.0',
    logLevel = process.env.LOG_LEVEL || 'info',
  } = options;

  const logger = winston.createLogger({
    level: logLevel,
    format: winston.format.combine(
      winston.format.timestamp(),
      winston.format.errors({ stack: true }),
      winston.format.json()
    ),
    defaultMeta: {
      service,
      environment,
      version,
    },
    transports: [
      // Console output (JSON format)
      new winston.transports.Console({
        format: winston.format.json(),
      }),
      // Error log file
      new winston.transports.File({
        filename: path.join(logsDir, 'error.log'),
        level: 'error',
        maxsize: 10485760, // 10MB
        maxFiles: 5,
      }),
      // Combined log file
      new winston.transports.File({
        filename: path.join(logsDir, 'combined.log'),
        maxsize: 10485760, // 10MB
        maxFiles: 5,
      }),
    ],
    // Handle exceptions and rejections
    exceptionHandlers: [
      new winston.transports.File({
        filename: path.join(logsDir, 'exceptions.log'),
      }),
    ],
    rejectionHandlers: [
      new winston.transports.File({
        filename: path.join(logsDir, 'rejections.log'),
      }),
    ],
  });

  return logger;
}

// Default logger instance
const logger = createLogger();

// Example usage functions
function logUserEvent(event, userId, metadata = {}) {
  logger.info(event, {
    userId,
    ...metadata,
  });
}

function logHttpRequest(req, res, durationMs) {
  logger.info('HTTP request', {
    traceId: req.headers['x-trace-id'],
    spanId: req.headers['x-span-id'],
    httpMethod: req.method,
    httpPath: req.path,
    httpStatus: res.statusCode,
    durationMs,
    userAgent: req.headers['user-agent'],
    ip: req.ip || req.connection.remoteAddress,
  });
}

function logError(error, context = {}) {
  logger.error('Error occurred', {
    error: error.message,
    stack: error.stack,
    ...context,
  });
}

function logDatabaseQuery(query, durationMs, success = true) {
  const level = success ? 'info' : 'error';
  logger[level]('Database query', {
    query: query.substring(0, 200), // Truncate long queries
    durationMs,
    success,
  });
}

// Export
module.exports = {
  createLogger,
  logger,
  logUserEvent,
  logHttpRequest,
  logError,
  logDatabaseQuery,
};

// CLI usage example
if (require.main === module) {
  // Example usage
  logger.info('Application started', {
    port: process.env.PORT || 3000,
    nodeVersion: process.version,
  });

  logger.info('User created', {
    userId: '12345',
    email: 'user@example.com',
    traceId: 'abc-123',
    spanId: 'span-456',
    httpMethod: 'POST',
    httpPath: '/api/users',
    httpStatus: 201,
    durationMs: 45,
  });

  logger.error('Database connection failed', {
    error: 'Connection timeout',
    database: 'users-db',
    retryAttempt: 3,
    traceId: 'abc-123',
  });
}

