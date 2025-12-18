# Service Mesh Scripts

Scripts bash para instalación y verificación de Istio service mesh.

## 📁 Archivos

- **`install-istio.sh`** - Instalación de Istio (Bash)
- **`verify-istio.sh`** - Verificación de instalación de Istio (Bash)

## 🚀 Quick Start

### Instalación de Istio

```bash
# Instalar con perfil demo (default)
chmod +x install-istio.sh
./install-istio.sh

# Instalar con perfil específico
./install-istio.sh --profile production

# Instalar versión específica
ISTIO_VERSION=1.19.0 ./install-istio.sh
```

### Verificación

```bash
# Verificar instalación
chmod +x verify-istio.sh
./verify-istio.sh
```

## 📋 Requisitos

- **kubectl:** Configurado y con acceso al cluster
- **curl:** Para descargar Istio
- **Permisos:** Permisos de cluster-admin para instalar Istio

## 📖 Documentación Completa

Ver [`../SKILL.md`](../SKILL.md) para documentación completa sobre:
- Istio installation
- Traffic management
- mTLS configuration
- Circuit breakers
- Service mesh best practices

