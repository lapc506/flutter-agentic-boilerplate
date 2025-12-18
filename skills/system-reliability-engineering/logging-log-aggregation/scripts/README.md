# Logging & Log Aggregation Scripts

Scripts ejecutables para structured logging y log management.

## 📁 Estructura

```
scripts/
├── nodejs/              # Node.js structured logging
│   ├── structured-logger.js
│   └── package.json
└── python/              # Python structured logging & archiving
    ├── structured_logger.py
    ├── log_archiver.py
    └── requirements.txt
```

## 🚀 Quick Start

### Node.js Structured Logging

```bash
cd nodejs
npm install

# Test the logger
node structured-logger.js

# Use in your application
const { logger } = require('./structured-logger');
logger.info('User created', { userId: '123', email: 'user@example.com' });
```

### Python Structured Logging

```bash
cd python

# Test the logger
python structured_logger.py

# Use in your application
from structured_logger import get_logger

logger = get_logger(service='my-service')
logger.info('User created', extra={
    'user_id': '12345',
    'trace_id': 'abc-123',
    'http_method': 'POST',
    'http_path': '/api/users',
    'http_status': 201,
    'duration_ms': 45,
})
```

### Log Archiving

```bash
cd python
pip install -r requirements.txt

# Archive logs older than retention period
python log_archiver.py archive \
  --s3-bucket my-logs-bucket \
  --log-dir /var/log/app \
  --retention-days 30

# Dry run (see what would be archived)
python log_archiver.py archive \
  --s3-bucket my-logs-bucket \
  --log-dir /var/log/app \
  --retention-days 30 \
  --dry-run

# Restore archived logs
python log_archiver.py restore \
  --s3-bucket my-logs-bucket \
  --date 2024-01-15 \
  --s3-prefix logs \
  --output-dir /tmp/restored
```

## 📊 Características

### Structured Logger

- ✅ JSON format output
- ✅ Timestamps automáticos
- ✅ Context injection (service, environment, version)
- ✅ File handlers (error.log, combined.log)
- ✅ Exception handling
- ✅ Convenience functions para eventos comunes

### Log Archiver

- ✅ Compresión automática (gzip)
- ✅ Upload a S3
- ✅ Restauración de logs archivados
- ✅ Dry-run mode
- ✅ Retención configurable

## 🔧 Configuración

### Variables de Entorno

**Node.js:**
- `NODE_ENV`: Environment (development, production)
- `APP_VERSION`: Application version
- `LOG_LEVEL`: Log level (debug, info, warn, error)

**Python:**
- `SERVICE_NAME`: Service name
- `ENVIRONMENT`: Environment
- `APP_VERSION`: Application version
- `LOG_LEVEL`: Log level (DEBUG, INFO, WARNING, ERROR)

**AWS (Log Archiver):**
- AWS credentials configuradas vía AWS CLI, variables de entorno, o IAM role

## 📖 Documentación Completa

Ver [`../SKILL.md`](../SKILL.md) para documentación completa sobre:
- Structured logging best practices
- Loki configuration
- Promtail setup
- Elasticsearch + Fluentd
- LogQL queries
- Retention policies

