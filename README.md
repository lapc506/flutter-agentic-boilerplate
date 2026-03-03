# Flutter Agentic Boilerplate

Plantilla de inicio para aplicaciones Flutter listas para producción con backend REST.

El objetivo principal de esta plantilla es que puedas comenzar a trabajar rápidamente en tu próximo proyecto Flutter listo para producción sin toda la molestia de la configuración inicial del proyecto.

## ¿Qué es esto?

Esta es una plantilla de boilerplate simple para crear una aplicación Flutter.

**Además, este proyecto incluye un sistema de Agent Skills** que proporciona conocimiento contextual y capacidades especializadas a los asistentes de IA. Los skills agénticos cubren desde patrones arquitectónicos (MVVM, Clean Architecture) hasta integraciones avanzadas (Firebase, GraphQL, CI/CD) y pueden invocarse automáticamente o explícitamente durante el desarrollo.

Puedes usar este boilerplate como base y aprovechar los skills agénticos para guiar la implementación de features específicas, arquitecturas complejas o integraciones con servicios externos. Los skills se cargan progresivamente solo cuando se necesitan, manteniendo la eficiencia y reduciendo la carga cognitiva.

## Decisiones Arquitectonicas

Esta plantilla es **opinionated** en arquitectura y state management:

- **Clean Architecture** — Separacion en capas (Domain / Data / Presentation) con dependencias unidireccionales. Cada feature es un modulo independiente con sus propias capas.
- **Atomic Design** — Sistema de componentes UI organizado en niveles de complejidad creciente: atoms, molecules, organisms, templates y pages.

### State Management Recomendado

Se recomiendan dos frameworks de state management, segun la escala del proyecto:

| Framework | Caso de uso | Paquete |
|-----------|-------------|---------|
| **Riverpod** | Proyectos de cualquier escala. Providers reactivos, compile-safe, con code generation opcional. | [`riverpod`](https://pub.dev/packages/riverpod) |
| **Air Framework** | Proyectos enterprise/large-scale. Framework modular completo con state management reactivo, dependency injection, routing y DevTools integrados. | [`air_framework`](https://pub.dev/packages/air_framework) |

Los skills agenticos incluyen guias detalladas para ambos frameworks, ademas de otros patrones arquitectonicos disponibles en `skills/flutter/`.

## Comenzando

### Prerrequisitos

- Flutter SDK instalado (versión estable recomendada)
- Dart SDK (incluido con Flutter)
- Android Studio / Xcode para desarrollo móvil
- Git

### Inicialización Rápida

Puedes inicializar el proyecto de dos formas:

#### Opción 1: Usando el Skill Agéntico (Recomendado)

Invoca el skill `@skill:flutter-project-setup` con tu asistente de IA para obtener una configuración guiada y personalizada del proyecto.

**Ejemplo:** *Levanta un proyecto Flutter usando @skill:flutter-project-setup y con @skill:riverpod y con @skill:clean-architecture.*

#### Opción 2: Usando Scripts Automatizados

Este proyecto incluye scripts automatizados que forman parte del skill `project-setup`:

**Windows (PowerShell):**

```powershell
.\skills\flutter\project-setup\scripts\setup.ps1
```

**Linux/macOS (Bash):**

```bash
chmod +x skills/flutter/project-setup/scripts/setup.sh
./skills/flutter/project-setup/scripts/setup.sh
```

Los scripts de setup realizarán automáticamente:
1. Verificación de instalación de Flutter
2. Creación de la estructura del monorepo (`backend/` y `mobile/`)
3. Inicialización del proyecto Flutter en `mobile/`
4. Instalación de dependencias
5. Configuración básica del proyecto (`.env-sample`, `.gitignore`, README)

## Despliegue

Antes de lanzar tu app de Android, asegúrate de firmarla:

1. Genera un archivo Keystore si aún no tienes uno. Si tienes uno, ignora este paso y ve al siguiente.
2. Ve a `mobile/android/key.properties` e incluye la ruta de tu Keystore, alias y contraseña.

## Skills Agénticos Disponibles

Este proyecto incluye un sistema de **Agent Skills** que proporciona conocimiento contextual y capacidades especializadas a los asistentes de IA. Los skills se invocan automáticamente basándose en keywords en tus prompts o explícitamente usando la sintaxis `@skill:`.

Para más detalles sobre cada skill, consulta [AGENTS.md](AGENTS.md).

### 🎨 Flutter Skills (28)

- `@skill:flutter/accessibility` - Implementación de accesibilidad con semantic widgets y screen reader support
- `@skill:flutter/analytics-tracking` - Analytics y tracking de eventos con Firebase Analytics, Mixpanel y Amplitude
- `@skill:flutter/animation-motion` - Animaciones avanzadas con Rive, Lottie, Hero animations y AnimationController
- `@skill:flutter/app-distribution` - Distribución de apps: TestFlight, Google Play Internal Testing, Firebase App Distribution
- `@skill:flutter/bloc-advanced` - State management con BLoC avanzado: Hydrated BLoC, Replay BLoC, transformers
- `@skill:flutter/clean-architecture` - Arquitectura en capas (Domain/Data/Presentation) con máxima testabilidad
- `@skill:flutter/code-generation` - Automatización de código boilerplate con build_runner, freezed, json_serializable
- `@skill:flutter/deep-linking` - Deep linking con universal links (iOS) y app links (Android) usando go_router
- `@skill:flutter/error-tracking` - Monitoreo de errores con Sentry y Firebase Crashlytics
- `@skill:flutter/feature-first` - Organización del código por features en lugar de capas técnicas
- `@skill:flutter/feature-flags` - Feature flags y remote configuration con Firebase Remote Config y LaunchDarkly
- `@skill:flutter/firebase` - Integración completa con Firebase: Auth, Firestore, Cloud Messaging y Analytics
- `@skill:flutter/graphql` - Integración con GraphQL: queries, mutations, subscriptions en tiempo real
- `@skill:flutter/i18n` - Soporte para múltiples idiomas con flutter_localizations, ARB files y formateo regional
- `@skill:flutter/integration-testing` - Estrategia completa de testing: unit, widget e integration tests
- `@skill:flutter/mobile-testing` - Testing móvil automatizado con Mobile MCP: pruebas de integración en dispositivos reales, simuladores iOS y emuladores Android
- `@skill:flutter/modular-architecture` - Arquitectura modular con módulos independientes y reutilizables
- `@skill:flutter/mvvm` - Patrón MVVM con separación clara entre UI y lógica de negocio
- `@skill:flutter/native-integration` - Integración profunda con APIs nativas de iOS (Swift/UIKit) y Android (Kotlin)
- `@skill:flutter/offline-first` - Arquitectura offline-first con cache inteligente y sincronización bidireccional
- `@skill:flutter/performance` - Optimización de rendimiento: profiling, memory leaks, rendering optimization
- `@skill:flutter/platform-channels` - Comunicación bidireccional con código nativo: MethodChannel, EventChannel y FFI
- `@skill:flutter/project-setup` - Configuración inicial estándar con análisis estático, flavors, temas y i18n
- `@skill:flutter/push-notifications` - Push notifications con Firebase Cloud Messaging y local notifications
- `@skill:flutter/riverpod` - State management con Riverpod: providers, hooks, y gestión de estado reactiva
- `@skill:flutter/security` - Mejores prácticas de seguridad: obfuscation, certificate pinning, secure storage
- `@skill:flutter/theming` - Sistema de diseño con múltiples temas, Material 3, dark mode y cambio dinámico
- `@skill:flutter/webview-integration` - Integración de WebViews con flutter_inappwebview y JavaScript channels

### 🚀 CI/CD Skills (9)

- `@skill:cicd/github-actions` - CI/CD nativo de GitHub para automatizar testing, building y deployment
- `@skill:cicd/argocd` - GitOps deployment para Kubernetes, sincronizando automáticamente el estado del cluster
- `@skill:cicd/terraform` - Infrastructure as Code multi-cloud para definir y provision infraestructura
- `@skill:cicd/aws` - Amazon Web Services deployment: EKS, RDS, S3, Lambda
- `@skill:cicd/gcp` - Google Cloud Platform deployment: GKE, Cloud Run, Cloud SQL, Firebase
- `@skill:cicd/azure` - Microsoft Azure deployment: AKS, Azure Functions, Azure SQL, Cosmos DB
- `@skill:cicd/ovhcloud` - OVHCloud deployment (EU-based): Managed Kubernetes, Object Storage, Databases
- `@skill:cicd/ansible-awx` - Configuration management y automation con Ansible AWX
- `@skill:cicd/crossplane` - Kubernetes-native infrastructure management multi-cloud

### 🎨 Design Integration Skills (1)

- `@skill:figma` - Integración con Figma Dev Mode vía MCP para extraer assets y componentes

### 🔍 Static Analysis Skills (1)

- `@skill:static-analysis` - Herramientas de análisis estático: Dart Analyzer, Datadog SAST y CodeRabbit CLI

### 🛡️ System Reliability Engineering Skills (14)

- `@skill:sre/alerting-incident-management` - Gestión de alertas e incidentes
- `@skill:sre/api-gateway-rate-limiting` - Rate limiting en API Gateway
- `@skill:sre/chaos-engineering` - Ingeniería del caos para testing de resiliencia
- `@skill:sre/container-security` - Seguridad de contenedores
- `@skill:sre/cost-optimization-finops` - Optimización de costos y FinOps
- `@skill:sre/database-reliability` - Confiabilidad de bases de datos
- `@skill:sre/disaster-recovery-business-continuity` - Recuperación ante desastres y continuidad de negocio
- `@skill:sre/load-testing-performance` - Testing de carga y rendimiento
- `@skill:sre/logging-log-aggregation` - Logging y agregación de logs
- `@skill:sre/network-policies-security` - Políticas de red y seguridad
- `@skill:sre/observability-stack` - Stack de observabilidad completo
- `@skill:sre/post-mortem` - Procesos de post-mortem
- `@skill:sre/security-compliance-automation` - Automatización de seguridad y compliance
- `@skill:sre/service-mesh` - Service mesh para microservicios
- `@skill:sre/slo-sli-sla` - Service Level Objectives, Indicators y Agreements

## Ejemplo de Estructura del Monorepo

```
proyecto/
├── backend/              # Backend REST API
│   ├── src/
│   ├── tests/
│   └── package.json
├── mobile/               # Aplicacion Flutter (Clean Architecture + Atomic Design)
│   ├── lib/
│   │   ├── core/             # Constantes, errores, red, tema, utils
│   │   ├── features/         # Modulos por feature
│   │   │   └── [feature]/
│   │   │       ├── data/
│   │   │       ├── domain/
│   │   │       └── presentation/
│   │   ├── shared/ui/        # Atomic Design (atoms, molecules, organisms, templates)
│   │   └── main.dart
│   ├── test/
│   └── assets/
├── skills/               # Agent Skills para asistentes de IA
│   ├── flutter/          # Skills de Flutter (28 skills)
│   │   ├── accessibility/
│   │   ├── analytics-tracking/
│   │   ├── animation-motion/
│   │   ├── app-distribution/
│   │   ├── bloc-advanced/
│   │   ├── clean-architecture/
│   │   ├── code-generation/
│   │   ├── deep-linking/
│   │   ├── error-tracking/
│   │   ├── feature-first/
│   │   ├── feature-flags/
│   │   ├── firebase/
│   │   ├── graphql/
│   │   ├── i18n/
│   │   ├── in-app-purchases/
│   │   ├── integration-testing/
│   │   ├── mobile-testing/
│   │   │   └── scripts/
│   │   ├── modular-architecture/
│   │   ├── mvvm/
│   │   ├── native-integration/
│   │   ├── offline-first/
│   │   ├── performance/
│   │   ├── platform-channels/
│   │   ├── project-setup/
│   │   │   └── scripts/
│   │   ├── push-notifications/
│   │   ├── riverpod/
│   │   ├── security/
│   │   ├── theming/
│   │   ├── webview-integration/
│   │   ├── BEST_PRACTICES_MAPPING.md
│   │   └── flutter-best-practices.md
│   ├── cicd/             # Skills de CI/CD (9 skills)
│   │   ├── ansible-awx/
│   │   ├── argocd/
│   │   ├── aws/
│   │   ├── azure/
│   │   ├── crossplane/
│   │   ├── gcp/
│   │   ├── github-actions/
│   │   ├── ovhcloud/
│   │   ├── terraform/
│   │   └── README.md
│   ├── figma/            # Design Integration Skills
│   │   └── SKILL.md
│   ├── static-analysis/  # Static Analysis Skills
│   │   └── SKILL.md
│   ├── system-reliability-engineering/  # SRE Skills (14 skills)
│   │   ├── alerting-incident-management/
│   │   ├── api-gateway-rate-limiting/
│   │   │   └── scripts/
│   │   ├── chaos-engineering/
│   │   │   └── scripts/
│   │   ├── container-security/
│   │   │   └── scripts/
│   │   ├── cost-optimization-finops/
│   │   │   └── scripts/
│   │   ├── database-reliability/
│   │   │   └── scripts/
│   │   ├── disaster-recovery-business-continuity/
│   │   │   └── scripts/
│   │   ├── load-testing-performance/
│   │   │   └── scripts/
│   │   ├── logging-log-aggregation/
│   │   │   └── scripts/
│   │   ├── network-policies-security/
│   │   │   └── scripts/
│   │   ├── observability-stack/
│   │   │   └── scripts/
│   │   ├── post-mortem/
│   │   ├── security-compliance-automation/
│   │   │   └── scripts/
│   │   ├── service-mesh/
│   │   │   └── scripts/
│   │   └── slo-sli-sla/
│   │       ├── examples/
│   │       └── scripts/
│   ├── CHANGELOG.md
│   ├── CONTRIBUTING.md
│   ├── LICENSE
│   ├── MCP_SETUP.md
│   ├── README.md
│   └── gemini-extension.json
└── README.md
```

## Desarrollo

### Ejecutar la App

```bash
cd mobile
flutter run
```

### Ejecutar Tests

```bash
cd mobile
flutter test
```

### Generar Builds

```bash
# Android
cd mobile
flutter build apk --release

# iOS
cd mobile
flutter build ios --release
```

## Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Haz fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## Soporte

Si encuentras algún problema o tienes preguntas, por favor abre un issue en el repositorio.

---

**¡Feliz desarrollo!** 🚀

