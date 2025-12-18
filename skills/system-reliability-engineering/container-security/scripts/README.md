# Container Security Scripts

Scripts ejecutables para container security: image signing y admission controller.

## 📁 Archivos

- **`sign-image.sh`** - Firmar imágenes de contenedores con Notary (Bash)
- **`admission_controller.py`** - Validación de seguridad de pods (Python CLI)
- **`requirements.txt`** - Dependencias Python

## 🚀 Quick Start

### Instalación

```bash
pip install -r requirements.txt

# Instalar Notary (para image signing)
# macOS:
brew install notary

# Linux:
# Download from https://github.com/notaryproject/notary/releases
```

### Image Signing

```bash
chmod +x sign-image.sh

# Firmar imagen
./sign-image.sh --image gcr.io/my-project/my-app:latest

# Con servidor Notary personalizado
./sign-image.sh \
  --image my-image:latest \
  --notary-server https://notary-server:4443
```

### Admission Controller

```bash
# Validar pod spec
python admission_controller.py validate --pod-spec pod.json

# Validar deployment spec
python admission_controller.py validate --deployment-spec deployment.json
```

## 📋 Requisitos

- **Docker:** Para pull/push de imágenes
- **Notary:** Instalado y configurado (para image signing)
- **Kubernetes Access:** kubeconfig configurado (para admission controller)

## 📖 Documentación Completa

Ver [`../SKILL.md`](../SKILL.md) para documentación completa sobre:
- Image scanning con Trivy
- Falco runtime security
- Image signing
- Security policies
- Admission controllers

