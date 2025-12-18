# Load Testing & Performance Scripts

Scripts ejecutables para load testing, profiling y capacity planning.

## 📁 Estructura

```
scripts/
├── k6/                    # k6 load test scripts
│   ├── basic-load.js
│   ├── advanced-scenarios.js
│   ├── stress-test.js
│   ├── rust-api-load.js
│   └── performance-comparison.js
├── nodejs/               # Node.js profiling tools
│   ├── performance-profiler.js
│   ├── memory-profiler.js
│   └── package.json
├── rust/                 # Rust benchmarks
│   ├── benches/
│   │   └── my_benchmark.rs
│   └── Cargo.toml
└── python/               # Python capacity planning
    ├── capacity_calculator.py
    └── requirements.txt
```

## 🚀 Quick Start

### k6 Load Tests

```bash
# Instalar k6
# macOS: brew install k6
# Linux: https://k6.io/docs/getting-started/installation/

# Basic load test
k6 run k6/basic-load.js

# Con variables de entorno
k6 run k6/basic-load.js \
  --env BASE_URL=https://api.example.com \
  --env API_TOKEN=your-token

# Advanced scenarios
k6 run k6/advanced-scenarios.js

# Stress test
k6 run k6/stress-test.js

# Rust API load test
k6 run k6/rust-api-load.js --env BASE_URL=http://localhost:8080

# Performance comparison
k6 run k6/performance-comparison.js \
  --env RUST_API=http://rust-api:8080 \
  --env NODE_API=http://node-api:3000
```

### Node.js Profiling

```bash
cd nodejs
npm install

# CPU profiling
node performance-profiler.js --profile-name my-app --duration=60

# Memory monitoring
node memory-profiler.js --monitor

# Memory snapshot
node memory-profiler.js --snapshot --filename=heap.heapsnapshot
```

### Rust Benchmarks

```bash
cd rust

# Ejecutar benchmarks
cargo bench

# Con profiling integrado
cargo bench -- --profile-time=10

# Ver resultados HTML
open target/criterion/report/index.html
```

### Python Capacity Planning

```bash
cd python

# Generar reporte de capacidad
python capacity_calculator.py --report

# Calcular recursos para usuarios objetivo
python capacity_calculator.py \
  --target-users 5000 \
  --current-users 1000 \
  --max-throughput 1000.0 \
  --current-instances 3
```

## 📊 Métricas y Resultados

### k6

- **Resultados en consola:** Métricas en tiempo real
- **Exportar a JSON:** `k6 run script.js --out json=results.json`
- **Exportar a InfluxDB:** `k6 run script.js --out influxdb=http://influxdb:8086/k6`

### Node.js Profiling

- **CPU Profiles:** Archivos `.cpuprofile` - abrir en Chrome DevTools
- **Memory Snapshots:** Archivos `.heapsnapshot` - abrir en Chrome DevTools

### Rust Benchmarks

- **HTML Reports:** `target/criterion/report/index.html`
- **Métricas:** Tiempo promedio, percentiles, comparaciones

## 🔧 Configuración

### Variables de Entorno (k6)

- `BASE_URL`: URL base de la API
- `API_TOKEN`: Token de autenticación
- `RUST_API`: URL del API Rust
- `NODE_API`: URL del API Node.js
- `SCENARIO`: Escenario específico a ejecutar

### Parámetros Node.js Profiling

- `--profile-name`: Nombre del perfil
- `--duration`: Duración en segundos
- `--interval`: Intervalo de monitoreo en ms

## 📖 Documentación Completa

Ver [`../SKILL.md`](../SKILL.md) para documentación completa sobre:
- Load testing strategies
- Performance profiling techniques
- Capacity planning methodologies
- Best practices

