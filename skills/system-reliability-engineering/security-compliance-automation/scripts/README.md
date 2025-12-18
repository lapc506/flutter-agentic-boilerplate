# Security & Compliance Automation Scripts

Scripts ejecutables para vulnerability scanning, compliance checking y automated remediation.

## 📁 Archivos

- **`vulnerability_scanner.py`** - Escaneo de vulnerabilidades en imágenes de contenedores (Python CLI)
- **`compliance_checker.py`** - Verificación de compliance AWS CIS benchmark (Python CLI)
- **`auto_remediation.py`** - Remediation automática de recursos Kubernetes (Python CLI)
- **`requirements.txt`** - Dependencias Python
- **`policies/kubernetes-security.rego`** - Políticas OPA (referencia, no ejecutable)

## 🚀 Quick Start

### Instalación

```bash
pip install -r requirements.txt

# Instalar Trivy (para vulnerability scanner)
# macOS:
brew install trivy

# Linux:
# Download from https://github.com/aquasecurity/trivy/releases
```

### Vulnerability Scanner

```bash
# Escanear imagen
python vulnerability_scanner.py scan --image gcr.io/my-project/my-app:latest

# Solo vulnerabilidades críticas
python vulnerability_scanner.py scan --image my-image --severity CRITICAL

# Exportar resultados
python vulnerability_scanner.py scan --image my-image --output results.json

# Verificar compliance
python vulnerability_scanner.py compliance --image my-image
```

### Compliance Checker

```bash
# Verificar CIS benchmark
python compliance_checker.py check-cis

# Verificar regla específica
python compliance_checker.py check-rule --rule-name access-keys-rotated

# Generar reporte
python compliance_checker.py report --output compliance-report.txt
```

### Auto Remediation

```bash
# Remediar namespace completo
python auto_remediation.py remediate --namespace production

# Dry run (ver qué se remediaría)
python auto_remediation.py remediate --namespace production --dry-run

# Remediar recurso específico
python auto_remediation.py remediate-resource \
  --kind Pod \
  --name my-pod \
  --namespace default
```

## 📋 Requisitos

- **Trivy:** Instalado y disponible en PATH (para vulnerability scanner)
- **AWS Credentials:** Configuradas para compliance checker
- **Kubernetes Access:** kubeconfig configurado para auto remediation
- **Permisos:**
  - AWS Config habilitado (para compliance checker)
  - Permisos de escritura en Kubernetes (para auto remediation)

## 📖 Documentación Completa

Ver [`../SKILL.md`](../SKILL.md) para documentación completa sobre:
- OPA policies
- Vulnerability scanning strategies
- Compliance automation
- Security policies as code
- Automated remediation best practices

