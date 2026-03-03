# Estructura del Proyecto

> Esta plantilla es **opinionated**: usa **Clean Architecture** + **Atomic Design** como estructura base para la app movil, y recomienda **Riverpod** o **Air Framework** para state management.

## Arbol de Directorios

```
proyecto/
├── AGENTS.md                          # Documentacion de Agent Skills + taxonomia Linear
├── README.md                          # Guia de inicio
├── mcp.json                           # Configuracion MCP servers
├── .gitignore
│
├── apps/
│   ├── backend/                       # API backend (NestJS / Express / etc.)
│   │   ├── src/
│   │   ├── test/
│   │   ├── scripts/
│   │   └── public/
│   ├── mobile/                        # App movil (Flutter)
│   │   ├── lib/
│   │   │   ├── core/                  # Constantes, errores, red, tema, utils
│   │   │   ├── features/             # Modulos por feature (Clean Architecture)
│   │   │   │   └── [feature]/
│   │   │   │       ├── data/         # Datasources, models, repository impl
│   │   │   │       ├── domain/       # Entities, use cases, repository interfaces
│   │   │   │       └── presentation/ # Pages, providers/controllers, widgets
│   │   │   ├── shared/
│   │   │   │   └── ui/               # Atomic Design
│   │   │   │       ├── atoms/        # Componentes basicos (botones, inputs, iconos)
│   │   │   │       ├── molecules/    # Combinaciones simples (labeled input, icon button)
│   │   │   │       ├── organisms/    # Componentes complejos (forms, cards, app bars)
│   │   │   │       └── templates/    # Layouts de pagina sin datos
│   │   │   └── main.dart
│   │   ├── test/
│   │   └── assets/
│   └── widgetbook/                    # Catalogo de widgets (Widgetbook)
│       ├── lib/
│       └── test/
│
├── infrastructure/
│   ├── terraform/
│   │   ├── environments/              # dev / qa / staging / prod
│   │   └── modules/                   # Modulos reutilizables
│   ├── helm-charts/
│   ├── k8s/                           # Manifiestos K8s de infra (gateway, cert-manager)
│   ├── docker/
│   ├── kms/                           # Gestion de secretos (Infisical, Vault, SOPS, etc.)
│   └── scripts/
│
├── k8s/                               # Manifiestos K8s de aplicacion
│   ├── base/backend/
│   ├── overlays/                      # dev / qa / staging / prod
│   └── argocd/                        # GitOps (projects + applications)
│
├── skills/                            # Agent Skills (54 skills)
│   ├── flutter/                       # 28 skills Flutter
│   ├── cicd/                          # 9 skills CI/CD
│   ├── backend/                       # Backend skills
│   ├── system-reliability-engineering/ # 14 skills SRE
│   ├── figma/
│   ├── static-analysis/
│   └── ...
│
├── docs/
│   ├── content/                       # Documentacion principal (MkDocs, Docusaurus, etc.)
│   ├── templates/                     # Plantillas (IEEE 830, ADR, etc.)
│   ├── versioning/                    # Tracking de versiones
│   ├── monitoring/                    # Docs de monitoreo
│   └── security/                      # Docs de seguridad
│
├── specs/                             # Especificaciones de requisitos (IEEE 830)
├── libs/                              # Librerias compartidas
├── scripts/                           # Scripts de utilidad (admin, setup, validacion)
├── logs/                              # Logs de aplicacion (backend, mobile)
├── linear-todo-templates/             # Templates para issues de Linear
│
└── .github/
    └── workflows/                     # CI/CD pipelines
```

## Descripcion de Directorios

| Directorio | Descripcion |
|------------|-------------|
| `apps/` | Aplicaciones del monorepo: backend API, app movil Flutter, y catalogo Widgetbook |
| `infrastructure/` | Infraestructura como codigo: Terraform, Helm, Docker, KMS, scripts de infra |
| `k8s/` | Manifiestos Kubernetes de aplicacion con Kustomize overlays y ArgoCD GitOps |
| `skills/` | Agent Skills para asistentes IA (Flutter, CI/CD, SRE, backend, etc.) |
| `docs/` | Documentacion del proyecto, plantillas, versionado, monitoreo y seguridad |
| `specs/` | Especificaciones de requisitos siguiendo estandar IEEE 830 |
| `libs/` | Librerias y paquetes compartidos entre aplicaciones |
| `scripts/` | Scripts de utilidad para administracion, setup y validacion |
| `logs/` | Logs de aplicacion separados por servicio (backend, mobile) |
| `linear-todo-templates/` | Templates reutilizables para issues en Linear |
| `.github/workflows/` | Pipelines de CI/CD con GitHub Actions |

## Arquitectura de la App Movil

La estructura de `apps/mobile/lib/` sigue **Clean Architecture** organizada por features, con **Atomic Design** para componentes UI compartidos.

### Clean Architecture (por feature)

Cada feature es un modulo independiente con tres capas:

| Capa | Contenido | Depende de |
|------|-----------|------------|
| `domain/` | Entities, use cases, repository interfaces | Nada (capa mas interna) |
| `data/` | Datasources, models, repository implementations | `domain/` |
| `presentation/` | Pages, widgets, providers/controllers | `domain/` |

Las dependencias son **unidireccionales**: `presentation/` y `data/` dependen de `domain/`, nunca al reves.

### Atomic Design (UI compartida)

Los componentes UI reutilizables viven en `shared/ui/` y siguen niveles de complejidad creciente:

| Nivel | Descripcion | Ejemplo |
|-------|-------------|---------|
| `atoms/` | Componentes indivisibles | Boton, TextField, Icono |
| `molecules/` | Combinacion de 2-3 atoms | Input con label, IconButton con tooltip |
| `organisms/` | Secciones funcionales completas | AppBar, Form, Card con acciones |
| `templates/` | Layouts de pagina (sin datos) | Scaffold con slots, grid layout |

### State Management Recomendado

| Framework | Cuando usarlo | Paquete |
|-----------|---------------|---------|
| **Riverpod** | Proyectos de cualquier escala. Providers reactivos, compile-safe, code generation opcional. | [`riverpod`](https://pub.dev/packages/riverpod) |
| **Air Framework** | Proyectos enterprise/large-scale. Framework modular con state reactivo (`@GenerateState`), DI, routing y DevTools. | [`air_framework`](https://pub.dev/packages/air_framework) |
