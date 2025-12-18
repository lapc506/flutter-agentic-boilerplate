# Observability Stack Scripts

Scripts ejecutables para instrumentación con OpenTelemetry en Node.js y Rust.

## 📁 Estructura

```
scripts/
├── nodejs/              # Node.js instrumentation
│   ├── instrumentation.js
│   ├── userService.js
│   └── package.json
└── rust/                # Rust instrumentation
    ├── src/
    │   ├── telemetry.rs
    │   ├── services/
    │   │   └── user_service.rs
    │   ├── main.rs
    │   └── lib.rs
    └── Cargo.toml
```

## 🚀 Quick Start

### Node.js Instrumentation

```bash
cd nodejs
npm install

# En tu aplicación, importa al inicio:
require('./instrumentation');

# O con variables de entorno:
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318/v1/traces node app.js
```

### Rust Instrumentation

```bash
cd rust

# Compilar
cargo build --release

# Ejecutar
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318/v1/traces ./target/release/observability-rust

# O usar como librería en tu proyecto
```

## 📊 Características

### Node.js

- ✅ Auto-instrumentation para HTTP, Express, PostgreSQL, Redis
- ✅ Custom spans
- ✅ OTLP exporter
- ✅ Resource attributes (service name, version, environment)

### Rust

- ✅ OpenTelemetry tracing
- ✅ Custom spans con attributes
- ✅ OTLP exporter
- ✅ Structured logging con tracing-subscriber
- ✅ Ejemplo de servicio con spans personalizados

## 🔧 Configuración

### Variables de Entorno

**Node.js y Rust:**
- `OTEL_EXPORTER_OTLP_ENDPOINT`: Endpoint OTLP (default: http://localhost:4318/v1/traces)
- `SERVICE_NAME`: Nombre del servicio
- `SERVICE_VERSION`: Versión del servicio
- `ENV` o `NODE_ENV`: Environment (development, production, etc.)

## 📖 Documentación Completa

Ver [`../SKILL.md`](../SKILL.md) para documentación completa sobre:
- Prometheus metrics
- Grafana dashboards
- Jaeger tracing
- OpenTelemetry best practices
- Rust instrumentation avanzada

