# Network Policies & Security Scripts

Scripts ejecutables para gestión de network policies en Kubernetes.

## 📁 Archivos

- **`network_policy_manager.py`** - Gestión de network policies (Python CLI)
- **`requirements.txt`** - Dependencias Python

## 🚀 Quick Start

### Instalación

```bash
pip install -r requirements.txt
```

### Network Policy Manager

```bash
# Listar policies
python network_policy_manager.py list --namespace production

# Crear policy
python network_policy_manager.py create \
  --namespace production \
  --policy policy.json

# Aplicar default deny-all
python network_policy_manager.py apply-default --namespace production

# Validar policy
python network_policy_manager.py validate --policy policy.json
```

## 📋 Requisitos

- **Kubernetes Access:** kubeconfig configurado
- **Permisos:** Permisos para crear/listar network policies

## 📖 Documentación Completa

Ver [`../SKILL.md`](../SKILL.md) para documentación completa sobre:
- Network policies básicas
- Egress e ingress rules
- Calico y Cilium
- Security best practices

