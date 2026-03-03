# SLO/SLI/SLA Scripts

Scripts ejecutables para gestión de Service Level Objectives (SLOs), Service Level Indicators (SLIs) y error budgets.

## 📁 Archivos

- **`error_budget.py`** - Calculadora de error budget (CLI standalone)
- **`slo_api.py`** - API REST FastAPI para consultar SLOs desde Prometheus
- **`requirements.txt`** - Dependencias Python

## 🚀 Quick Start

### Error Budget Calculator

No requiere instalación (usa solo stdlib):

```bash
# Ejemplo básico
python error_budget.py \
  --slo-target 0.9995 \
  --total-requests 1000000 \
  --error-requests 400

# Modo interactivo
python error_budget.py --slo-target 0.9995 --interactive
```

### SLO API Service

Instalación:

```bash
pip install -r requirements.txt
```

Ejecución:

```bash
# Desarrollo
uvicorn slo_api:app --reload

# Producción
uvicorn slo_api:app --host 0.0.0.0 --port 8000 --workers 4
```

## 📖 Documentación Completa

Ver [`../SKILL.md`](../SKILL.md) para documentación completa y ejemplos de uso.

## 🔗 Ejemplos

Ver [`../examples/usage_example.py`](../examples/usage_example.py) para ejemplos programáticos.
