# 🚀 CI/CD Skills

Esta carpeta contiene skills especializados para Continuous Integration y Continuous Deployment, enfocados en infraestructura y deployment de backends para aplicaciones Flutter en un contexto de monorepo.

## 📦 Skills Disponibles

### 🔄 CI/CD & Deployment

| Skill | Nivel | Keywords | Descripción |
|-------|-------|----------|-------------|
| **GitHub Actions** | 🟡 Intermedio | `github-actions`, `ci`, `workflow` | CI/CD nativo de GitHub para Flutter + Backend |
| **ArgoCD** | 🔴 Avanzado | `argocd`, `gitops`, `kubernetes` | GitOps deployment para Kubernetes |

### 🏗️ Infrastructure as Code

| Skill | Nivel | Keywords | Descripción |
|-------|-------|----------|-------------|
| **Terraform** | 🔴 Avanzado | `terraform`, `iac`, `hcl` | Infrastructure as Code multi-cloud |

### ☁️ Cloud Providers

| Skill | Nivel | Keywords | Descripción |
|-------|-------|----------|-------------|
| **AWS** | 🔴 Avanzado | `aws`, `eks`, `rds`, `lambda` | Amazon Web Services deployment |
| **GCP** | 🔴 Avanzado | `gcp`, `gke`, `cloud-run` | Google Cloud Platform deployment |
| **Azure** | 🔴 Avanzado | `azure`, `aks`, `azure-functions` | Microsoft Azure deployment |
| **OVHCloud** | 🟡 Intermedio | `ovh`, `ovhcloud`, `kubernetes` | OVHCloud deployment (EU-based) |

### 🔧 Automation & Orchestration

| Skill | Nivel | Keywords | Descripción |
|-------|-------|----------|-------------|
| **Ansible AWX** | 🔴 Avanzado | `ansible`, `awx`, `automation` | Configuration management y automation |
| **Crossplane** | 🔴 Avanzado | `crossplane`, `multi-cloud` | Kubernetes-native infrastructure management |

## 🎯 Casos de Uso

### Monorepo Flutter + Backend

```
my-app-monorepo/
├── mobile/           # Flutter app
├── backend/          # Backend (Node.js/Python/Go)
├── infrastructure/   # Terraform/IaC
└── .github/workflows/  # GitHub Actions
```

### Stack Recomendado por Escenario

#### 🚀 Startup/MVP
- **CI/CD**: GitHub Actions
- **Cloud**: AWS (Free tier) o OVHCloud (precio)
- **Deployment**: Simple containers o Lambda

#### 🏢 Enterprise
- **IaC**: Terraform
- **CI/CD**: GitHub Actions + ArgoCD
- **Cloud**: AWS/GCP/Azure (multi-cloud con Crossplane)
- **Orchestration**: Kubernetes (EKS/GKE/AKS)
- **Automation**: Ansible AWX para## 🔄 Flujo de Ciclo de Vida (DEV a PROD)

Para garantizar la estabilidad desde el desarrollo local hasta la producción, se define el siguiente flujo:

1.  **DEV (Local - Kind en Ubuntu)**:
    - **Uso**: Desarrollo rápido, pruebas de integración locales.
    - **Aislamiento**: Cada desarrollador tiene su propio cluster Kind.
    - **PostgreSQL**: Instancia local dentro de Kind con persistencia en el host.
2.  **QA (Entorno de Pruebas Automatizadas)**:
    - **Uso**: Validación de Pull Requests (PRs).
    - **Trigger**: GitHub Actions despliega automáticamente en un cluster de QA efímero.
3.  **STAGE (Pre-producción)**:
    - **Uso**: Manual QA y User Acceptance Testing (UAT).
    - **Config**: Espejo de PROD con configuraciones reales (SSL, Ingress real).
4.  **PROD (Producción)**:
    - **Uso**: Usuarios finales. Alta disponibilidad y monitoreo activado.

---

## 🛠️ Configuración de Kind para Acceso Externo (DB)

Para acceder a PostgreSQL (puerto `5432`) desde herramientas como **DBeaver** o **DataGrip** en Ubuntu, se debe usar `extraPortMappings` en el archivo de configuración de Kind:

```yaml
# kind-config.yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
  extraPortMappings:
  # Mapeo para PostgreSQL
  - containerPort: 30432 # El NodePort definido en el Service de K8s
    hostPort: 5432       # El puerto que usarás en DBeaver (localhost:5432)
    protocol: TCP
  # Opcional: Mapeo para el API Gateway (HTTP)
  - containerPort: 30080
    hostPort: 80
    protocol: TCP
```

> [!IMPORTANT]
> En tus manifiestos de Kubernetes (Service de Postgres), debes asegurarte de que el tipo de servicio sea `NodePort` y que el `nodePort` coincida con el `containerPort` configurado arriba (`30432`).

---

## 🔎 ¿Qué falta en las especificaciones del proyecto?

Al revisar los actuales documentos de diseño y requisitos, se identifican las siguientes ausencias críticas para la estandarización de entornos:

1.  **Environment Segregation Strategy**: No hay un detalle de cómo se gestionan los secretos y las variables de entorno de forma diferenciada entre DEV, QA y PROD.
2.  **Local Dev Guide**: Falta un documento técnico (ej. `local-dev.md`) que explique el paso a paso para levantar el entorno con Kind, incluyendo la configuración de red y base de datos local.
3.  **Database Migration Workflow**: No se especifica cómo se ejecutan las migraciones de base de datos en los diferentes entornos de forma coordinada con los despliegues de ArgoCD.
4.  **External Tooling Guidelines**: Instrucciones sobre cómo conectar herramientas externas (DBeaver, Lens, Prometheus) al cluster Kind local.

---

## 💡 Recomendación de Implementación
Para tu caso específico en Ubuntu, el flujo ideal sería:
1. Usar **Ansible** para preparar Ubuntu e instanciar el cluster **Kind**.
2. Instalar **ArgoCD** dentro de Kind para gestionar los despliegues.
3. Desplegar **PostgreSQL** usando un manifest de `StatefulSet` (siguiendo patrones de Database Reliability) con persistencia en el host de Ubuntu vía `hostPath` o `local-path-provisioner`.

> [!TIP]
> Dado que Kind corre dentro de Docker, asegúrate de configurar correctamente los `extraPortMappings` en Kind si necesitas acceder a PostgreSQL directamente desde fuera del cluster (ej. desde una herramienta de escritorio).
 config management

#### 🌍 Multi-región/Multi-cloud
- **IaC**: Terraform + Crossplane
- **Deployment**: ArgoCD para GitOps
- **Cloud**: Multi-cloud (AWS + GCP o Azure)
- **Automation**: Ansible AWX

## 🔑 Keywords Combinados

Puedes combinar skills en tus prompts:

```bash
"Usa terraform + aws + argocd para setup de backend Flutter en Kubernetes"

"Configura github-actions + gcp + cloud-run para deployment serverless"

"Implementa multi-cloud con crossplane + terraform en AWS y Azure"

"Setup ansible-awx + kubernetes para automatizar deployments"
```

## 📚 Workflow Típico

### 1. Setup Infraestructura
```bash
@skill:terraform - Provision infrastructure en AWS
@skill:aws - Configure EKS cluster y RDS
```

### 2. Configure CI/CD
```bash
@skill:github-actions - Setup pipelines para Flutter y Backend
```

### 3. Setup GitOps
```bash
@skill:argocd - Configure continuous deployment
```

### 4. Automatización
```bash
@skill:ansible-awx - Automatiza configuración de servidores
```

## 🎓 Learning Path

### Nivel Básico
1. Start: **GitHub Actions** - CI/CD básico
2. Cloud: **AWS** o **GCP** - Servicios básicos

### Nivel Intermedio
3. IaC: **Terraform** - Infrastructure as Code
4. GitOps: **ArgoCD** - Continuous Deployment

### Nivel Avanzado
5. Multi-cloud: **Crossplane** - Cloud-agnostic
6. Automation: **Ansible AWX** - Advanced automation

## 🔗 Skills Relacionados

- [Flutter Skills](../flutter/) - Mobile app development
- [Figma Skills](../figma/) - Design integration

---

**Última actualización:** Diciembre 2025
**Total Skills:** 9
