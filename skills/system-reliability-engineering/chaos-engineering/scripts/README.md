# Chaos Engineering Scripts

Scripts ejecutables para chaos engineering y resilience testing.

## 📁 Archivos

- **`chaos_monkey.py`** - Chaos Monkey para Kubernetes (Python CLI)
- **`experiments.py`** - Framework para ejecutar y gestionar chaos experiments (Python CLI)
- **`requirements.txt`** - Dependencias Python
- **`examples/`** - YAML de Litmus como referencia (no ejecutables)

## 🚀 Quick Start

### Instalación

```bash
pip install -r requirements.txt
```

### Chaos Monkey

```bash
# Ejecutar experimento (pod-delete)
python chaos_monkey.py run --experiment-type pod-delete

# Habilitar/deshabilitar
python chaos_monkey.py enable
python chaos_monkey.py disable

# Configurar probabilidad
python chaos_monkey.py set-probability --probability 0.1
```

### Experiments

```bash
# Ejecutar experimento
python experiments.py run --name pod-delete

# Listar experimentos
python experiments.py list
```

## 📋 Requisitos

- **Kubernetes Access:** kubeconfig configurado
- **Permisos:** Permisos para eliminar pods en namespaces con `chaos.enabled=true` annotation
- **Annotations:** Deployments deben tener `chaos.enabled=true` annotation para ser elegibles

## 🎯 Uso

### Anotar Deployment para Chaos

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
  annotations:
    chaos.enabled: "true"
spec:
  # ...
```

### Ejecutar Chaos Monkey

```bash
# Ejecutar con probabilidad del 10%
python chaos_monkey.py run --experiment-type pod-delete --probability 0.1
```

## 📖 Documentación Completa

Ver [`../SKILL.md`](../SKILL.md) para documentación completa sobre:
- Chaos engineering principles
- Litmus experiments
- Experiment design
- Resilience testing strategies
- Best practices

