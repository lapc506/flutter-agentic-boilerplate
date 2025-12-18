# Cost Optimization & FinOps Scripts

Scripts ejecutables para gestión de costos cloud y FinOps practices.

## 📁 Archivos

- **`aws_cost_tracker.py`** - Tracking y análisis de costos AWS (Python CLI)
- **`budget_alert.py`** - Gestión de budgets y alertas AWS (Python CLI)
- **`resource_optimizer.py`** - Análisis de recursos y oportunidades de optimización (Python CLI)
- **`auto_optimizer.py`** - Optimizador automático completo (Python CLI)
- **`requirements.txt`** - Dependencias Python

## 🚀 Quick Start

### Instalación

```bash
pip install -r requirements.txt
```

### AWS Cost Tracker

```bash
# Costos diarios
python aws_cost_tracker.py daily --days 30

# Costos por servicio
python aws_cost_tracker.py service EC2 --days 30

# Costos por tag
python aws_cost_tracker.py tag --tag-key Environment --days 30

# Exportar a CSV
python aws_cost_tracker.py daily --days 30 --output costs.csv
```

### Budget Alerts

```bash
# Crear budget
python budget_alert.py create \
  --name monthly-budget \
  --amount 10000 \
  --period monthly \
  --thresholds 50,80,100 \
  --email ops@example.com

# Listar budgets
python budget_alert.py list

# Ver estado
python budget_alert.py status --name monthly-budget
```

### Resource Optimizer

```bash
# Encontrar instancias idle
python resource_optimizer.py idle --cpu-threshold 10

# Oportunidades de rightsizing
python resource_optimizer.py rightsize

# Volúmenes no usados
python resource_optimizer.py unused-volumes
```

### Auto Optimizer

```bash
# Análisis completo
python auto_optimizer.py analyze

# Generar reporte
python auto_optimizer.py report --output report.json
```

## 📋 Requisitos

- **AWS Credentials:** Configuradas vía AWS CLI, variables de entorno, o IAM role
- **Permisos IAM:** 
  - `ce:GetCostAndUsage` (Cost Explorer)
  - `budgets:*` (Budgets)
  - `ec2:Describe*` (EC2)
  - `cloudwatch:GetMetricStatistics` (CloudWatch)

## 📖 Documentación Completa

Ver [`../SKILL.md`](../SKILL.md) para documentación completa sobre:
- Cost monitoring strategies
- Budget management
- Resource optimization
- Cost allocation
- FinOps best practices

