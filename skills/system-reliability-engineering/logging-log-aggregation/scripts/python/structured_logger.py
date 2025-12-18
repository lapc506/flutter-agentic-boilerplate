#!/usr/bin/env python3
"""
Structured Logger for Python

Structured logging with JSON output for centralized logging systems.

Usage:
    from structured_logger import get_logger
    
    logger = get_logger(service='my-service')
    logger.info('User created', extra={
        'user_id': '12345',
        'trace_id': request.headers.get('X-Trace-Id'),
        'http_method': request.method,
        'http_path': request.path,
        'http_status': 201,
        'duration_ms': 45,
    })
"""

import json
import logging
import sys
from datetime import datetime
from typing import Dict, Any, Optional


class StructuredFormatter(logging.Formatter):
    """JSON formatter for structured logging."""
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        log_data = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'level': record.levelname,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
        }
        
        # Add extra fields from record
        for key, value in record.__dict__.items():
            if key not in [
                'name', 'msg', 'args', 'created', 'filename', 'funcName',
                'levelname', 'levelno', 'lineno', 'module', 'msecs',
                'message', 'pathname', 'process', 'processName', 'relativeCreated',
                'thread', 'threadName', 'exc_info', 'exc_text', 'stack_info'
            ]:
                log_data[key] = value
        
        # Add exception info if present
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)
        
        # Add stack trace if present
        if record.stack_info:
            log_data['stack'] = self.formatStack(record.stack_info)
        
        return json.dumps(log_data)


def get_logger(
    name: Optional[str] = None,
    service: Optional[str] = None,
    environment: Optional[str] = None,
    version: Optional[str] = None,
    level: str = 'INFO'
) -> logging.Logger:
    """
    Get a structured logger instance.
    
    Args:
        name: Logger name (default: __name__)
        service: Service name (default: from env or 'application')
        environment: Environment (default: from env or 'development')
        version: Application version (default: from env or '1.0.0')
        level: Log level (default: 'INFO')
        
    Returns:
        Configured logger instance
    """
    import os
    
    logger = logging.getLogger(name or __name__)
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Create formatter
    formatter = StructuredFormatter()
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler for errors
    error_handler = logging.FileHandler('logs/error.log')
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    logger.addHandler(error_handler)
    
    # File handler for all logs
    file_handler = logging.FileHandler('logs/combined.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Add default metadata
    service_name = service or os.getenv('SERVICE_NAME', 'application')
    env = environment or os.getenv('ENVIRONMENT', 'development')
    app_version = version or os.getenv('APP_VERSION', '1.0.0')
    
    # Add adapter to inject default metadata
    class ContextAdapter(logging.LoggerAdapter):
        def process(self, msg, kwargs):
            kwargs.setdefault('extra', {})
            kwargs['extra'].setdefault('service', service_name)
            kwargs['extra'].setdefault('environment', env)
            kwargs['extra'].setdefault('version', app_version)
            return msg, kwargs
    
    return ContextAdapter(logger, {})


# Convenience functions
def log_user_event(logger: logging.Logger, event: str, user_id: str, **metadata):
    """Log a user event."""
    logger.info(event, extra={
        'user_id': user_id,
        **metadata,
    })


def log_http_request(
    logger: logging.Logger,
    method: str,
    path: str,
    status: int,
    duration_ms: float,
    trace_id: Optional[str] = None,
    span_id: Optional[str] = None,
    **metadata
):
    """Log an HTTP request."""
    logger.info('HTTP request', extra={
        'http_method': method,
        'http_path': path,
        'http_status': status,
        'duration_ms': duration_ms,
        'trace_id': trace_id,
        'span_id': span_id,
        **metadata,
    })


def log_error(logger: logging.Logger, error: Exception, **context):
    """Log an error with context."""
    logger.error('Error occurred', extra={
        'error': str(error),
        'error_type': type(error).__name__,
        **context,
    }, exc_info=True)


def log_database_query(
    logger: logging.Logger,
    query: str,
    duration_ms: float,
    success: bool = True
):
    """Log a database query."""
    level = logging.INFO if success else logging.ERROR
    logger.log(level, 'Database query', extra={
        'query': query[:200],  # Truncate long queries
        'duration_ms': duration_ms,
        'success': success,
    })


# Default logger instance
logger = get_logger()


# CLI usage
if __name__ == '__main__':
    import os
    
    # Create logs directory
    os.makedirs('logs', exist_ok=True)
    
    # Example usage
    logger.info('Application started', extra={
        'port': os.getenv('PORT', '3000'),
        'python_version': sys.version,
    })
    
    logger.info('User created', extra={
        'user_id': '12345',
        'email': 'user@example.com',
        'trace_id': 'abc-123',
        'span_id': 'span-456',
        'http_method': 'POST',
        'http_path': '/api/users',
        'http_status': 201,
        'duration_ms': 45,
    })
    
    logger.error('Database connection failed', extra={
        'error': 'Connection timeout',
        'database': 'users-db',
        'retry_attempt': 3,
        'trace_id': 'abc-123',
    })

