# 📚 Agent Skills - Índice

Este directorio contiene todos los skills disponibles organizados por categorías. Los skills siguen el patrón de [Deep Agents](https://blog.langchain.com/using-skills-with-deep-agents/) con archivos `SKILL.md` que se cargan progresivamente.

## 📂 Estructura

```
skills/
├── flutter/                    # Skills para desarrollo Flutter
│   ├── mvvm/
│   ├── clean-architecture/
│   ├── project-setup/
│   ├── testing/
│   ├── mobile-testing/
│   ├── riverpod/
│   ├── bloc-advanced/
│   ├── modular-architecture/
│   ├── feature-first/
│   ├── i18n/
│   ├── theming/
│   ├── offline-first/
│   ├── graphql/
│   ├── firebase/
│   └── performance/
├── cicd/                       # Skills para CI/CD e Infraestructura
│   ├── github-actions/
│   ├── terraform/
│   ├── argocd/
│   ├── aws/
│   ├── gcp/
│   ├── azure/
│   ├── ovhcloud/
│   ├── ansible-awx/
│   └── crossplane/
├── backend/                    # Skills para desarrollo Backend
│   └── hexagonal-architecture/
└── figma/                      # Skills para integración con Figma
```

## 🎯 Skills Disponibles

### 🎨 Flutter Skills

| # | Skill | Nivel | Path | Keywords |
|---|-------|-------|------|----------|
| 1 | **MVVM Pattern** | 🟡 Intermedio | [`flutter/mvvm/`](./flutter/mvvm/) | `mvvm`, `model-view-viewmodel`, `provider` |
| 2 | **Clean Architecture** | 🔴 Avanzado | [`flutter/clean-architecture/`](./flutter/clean-architecture/) | `clean`, `clean-arch`, `bloc`, `usecase` |
| 3 | **Project Setup** | 🟢 Básico | [`flutter/project-setup/`](./flutter/project-setup/) | `setup`, `init`, `scaffold` |
| 4 | **Testing Strategy** | 🔴 Avanzado | [`flutter/testing/`](./flutter/testing/) | `testing`, `test`, `unit-test`, `widget-test` |
| 5 | **Mobile Testing** | 🔴 Avanzado | [`flutter/mobile-testing/`](./flutter/mobile-testing/) | `mobile-testing`, `integration-test-mobile`, `mobile-mcp`, `mobile-automation`, `ui-testing-mobile` |
| 6 | **Code Generation** | 🟢 Básico | [`flutter/code-generation/`](./flutter/code-generation/) | `code-gen`, `build-runner`, `freezed`, `json-serializable`, `injectable` |
| 7 | **Security** | 🔴 Avanzado | [`flutter/security/`](./flutter/security/) | `security`, `obfuscation`, `certificate-pinning`, `encryption`, `biometric` |
| 8 | **Platform Channels** | 🔴 Avanzado | [`flutter/platform-channels/`](./flutter/platform-channels/) | `platform-channels`, `methodchannel`, `eventchannel`, `ffi`, `native` |
| 9 | **Native Integration** | 🔴 Avanzado | [`flutter/native-integration/`](./flutter/native-integration/) | `native-integration`, `swift`, `kotlin`, `uikit`, `native-ui` |
| 10 | **App Distribution** | 🟡 Intermedio | [`flutter/app-distribution/`](./flutter/app-distribution/) | `app-distribution`, `testflight`, `play-console`, `fastlane` |
| 11 | **Error Tracking** | 🟡 Intermedio | [`flutter/error-tracking/`](./flutter/error-tracking/) | `error-tracking`, `sentry`, `crashlytics`, `monitoring` |
| 12 | **Analytics & Tracking** | 🟡 Intermedio | [`flutter/analytics-tracking/`](./flutter/analytics-tracking/) | `analytics`, `mixpanel`, `amplitude`, `firebase-analytics` |
| 13 | **Deep Linking** | 🟡 Intermedio | [`flutter/deep-linking/`](./flutter/deep-linking/) | `deep-linking`, `universal-links`, `app-links`, `go-router` |
| 14 | **Push Notifications** | 🟡 Intermedio | [`flutter/push-notifications/`](./flutter/push-notifications/) | `push-notifications`, `fcm`, `firebase-messaging`, `local-notifications` |
| 15 | **Animation & Motion** | 🔴 Avanzado | [`flutter/animation-motion/`](./flutter/animation-motion/) | `animation`, `motion`, `rive`, `lottie`, `hero`, `tween` |
| 16 | **Accessibility** | 🟡 Intermedio | [`flutter/accessibility/`](./flutter/accessibility/) | `accessibility`, `a11y`, `semantic`, `screen-reader`, `wcag` |
| 17 | **Feature Flags** | 🟡 Intermedio | [`flutter/feature-flags/`](./flutter/feature-flags/) | `feature-flags`, `remote-config`, `firebase-remote-config`, `ab-testing` |
| 18 | **In-App Purchases** | 🔴 Avanzado | [`flutter/in-app-purchases/`](./flutter/in-app-purchases/) | `in-app-purchases`, `iap`, `subscriptions`, `revenue-cat` |
| 19 | **WebView Integration** | 🟡 Intermedio | [`flutter/webview-integration/`](./flutter/webview-integration/) | `webview`, `flutter-inappwebview`, `javascript`, `hybrid` |

### 🚀 CI/CD & Infrastructure Skills

| # | Skill | Nivel | Path | Keywords |
|---|-------|-------|------|----------|
| 1 | **GitHub Actions** | 🟡 Intermedio | [`cicd/github-actions/`](./cicd/github-actions/) | `github-actions`, `ci`, `workflow` |
| 2 | **Terraform** | 🔴 Avanzado | [`cicd/terraform/`](./cicd/terraform/) | `terraform`, `iac`, `hcl` |
| 3 | **ArgoCD** | 🔴 Avanzado | [`cicd/argocd/`](./cicd/argocd/) | `argocd`, `gitops`, `kubernetes` |
| 4 | **AWS** | 🔴 Avanzado | [`cicd/aws/`](./cicd/aws/) | `aws`, `eks`, `rds`, `lambda` |
| 5 | **GCP** | 🔴 Avanzado | [`cicd/gcp/`](./cicd/gcp/) | `gcp`, `gke`, `cloud-run` |
| 6 | **Azure** | 🔴 Avanzado | [`cicd/azure/`](./cicd/azure/) | `azure`, `aks`, `azure-functions` |
| 7 | **OVHCloud** | 🟡 Intermedio | [`cicd/ovhcloud/`](./cicd/ovhcloud/) | `ovh`, `ovhcloud`, `kubernetes` |
| 8 | **Ansible AWX** | 🔴 Avanzado | [`cicd/ansible-awx/`](./cicd/ansible-awx/) | `ansible`, `awx`, `automation` |
| 9 | **Crossplane** | 🔴 Avanzado | [`cicd/crossplane/`](./cicd/crossplane/) | `crossplane`, `multi-cloud` |

### 🖇️ Backend Skills

| # | Skill | Nivel | Path | Keywords |
|---|-------|-------|------|----------|
| 1 | **Hexagonal Architecture** | 🔴 Avanzado | [`backend/hexagonal-architecture/`](./backend/hexagonal-architecture/) | `hexagonal`, `hexagonal-architecture`, `ports-and-adapters`, `ddd` |

### 🔧 System Reliability Engineering (SRE) Skills

| # | Skill | Nivel | Path | Keywords |
|---|-------|-------|------|----------|
| 1 | **Observability Stack** | 🔴 Avanzado | [`system-reliability-engineering/observability-stack/`](./system-reliability-engineering/observability-stack/) | `observability`, `monitoring`, `prometheus`, `grafana`, `jaeger`, `opentelemetry`, `liveness`, `heartbeat`, `absence-detection`, `cloud-run`, `opentofu` |
| 2 | **Alerting & Incident Management** | 🔴 Avanzado | [`system-reliability-engineering/alerting-incident-management/`](./system-reliability-engineering/alerting-incident-management/) | `alerting`, `incident-management`, `pagerduty`, `runbooks`, `postmortem`, `monitoring-as-code`, `alert-policy`, `opentofu` |
| 3 | **Service Level Objectives (SLO/SLI/SLA)** | 🔴 Avanzado | [`system-reliability-engineering/slo-sli-sla/`](./system-reliability-engineering/slo-sli-sla/) | `slo`, `sli`, `sla`, `error-budget`, `service-level`, `reliability`, `mttd`, `time-to-detect` |
| 4 | **Database Reliability** | 🔴 Avanzado | [`system-reliability-engineering/database-reliability/`](./system-reliability-engineering/database-reliability/) | `database`, `replication`, `backup`, `failover`, `postgresql`, `connection-pooling` |
| 5 | **Load Testing & Performance** | 🔴 Avanzado | [`system-reliability-engineering/load-testing-performance/`](./system-reliability-engineering/load-testing-performance/) | `load-testing`, `performance`, `k6`, `jmeter`, `stress-testing`, `capacity-planning` |
| 6 | **Logging & Log Aggregation** | 🔴 Avanzado | [`system-reliability-engineering/logging-log-aggregation/`](./system-reliability-engineering/logging-log-aggregation/) | `logging`, `log-aggregation`, `loki`, `elasticsearch`, `fluentd`, `structured-logs` |
| 7 | **Service Mesh** | 🔴 Avanzado | [`system-reliability-engineering/service-mesh/`](./system-reliability-engineering/service-mesh/) | `service-mesh`, `istio`, `linkerd`, `envoy`, `traffic-management`, `mtls` |
| 8 | **API Gateway & Rate Limiting** | 🟡 Intermedio | [`system-reliability-engineering/api-gateway-rate-limiting/`](./system-reliability-engineering/api-gateway-rate-limiting/) | `api-gateway`, `rate-limiting`, `kong`, `nginx`, `traefik`, `throttling` |
| 9 | **Disaster Recovery & Business Continuity** | 🔴 Avanzado | [`system-reliability-engineering/disaster-recovery-business-continuity/`](./system-reliability-engineering/disaster-recovery-business-continuity/) | `disaster-recovery`, `business-continuity`, `backup`, `failover`, `rpo`, `rto`, `opentofu`, `prevent-destroy` |
| 10 | **Cost Optimization & FinOps** | 🟡 Intermedio | [`system-reliability-engineering/cost-optimization-finops/`](./system-reliability-engineering/cost-optimization-finops/) | `cost-optimization`, `finops`, `cloud-costs`, `resource-optimization`, `budget-alerts` |
| 11 | **Security & Compliance Automation** | 🔴 Avanzado | [`system-reliability-engineering/security-compliance-automation/`](./system-reliability-engineering/security-compliance-automation/) | `security`, `compliance`, `automation`, `vulnerability-scanning`, `opa`, `policy-as-code` |
| 12 | **Chaos Engineering** | 🔴 Avanzado | [`system-reliability-engineering/chaos-engineering/`](./system-reliability-engineering/chaos-engineering/) | `chaos-engineering`, `chaos-monkey`, `litmus`, `failure-injection`, `resilience-testing`, `detection-validation`, `game-day` |
| 13 | **Network Policies & Security** | 🔴 Avanzado | [`system-reliability-engineering/network-policies-security/`](./system-reliability-engineering/network-policies-security/) | `network-policies`, `network-security`, `kubernetes-networking`, `egress`, `ingress`, `calico` |
| 14 | **Container Security** | 🔴 Avanzado | [`system-reliability-engineering/container-security/`](./system-reliability-engineering/container-security/) | `container-security`, `image-scanning`, `runtime-security`, `falco`, `notary`, `cve-scanning` |

### 🎨 Design Integration Skills

| # | Skill | Nivel | Path | Keywords |
|---|-------|-------|------|----------|
| 1 | **Figma Dev Mode** | 🟡 Intermedio | [`figma/`](./figma/) | `figma`, `design`, `assets`, `components`, `dev-mode` |

## 🔑 Cómo Usar Keywords

Los keywords son triggers que puedes usar en tus prompts para invocar un skill específico:

### Ejemplo 1: Usando keywords directos
```
Crea un proyecto usando mvvm para una app de notas
```

### Ejemplo 2: Usando múltiples keywords
```
Necesito setup inicial con clean-arch y testing para un e-commerce
```

### Ejemplo 3: Backend + Infrastructure
```
Usa terraform + aws + argocd para setup de backend Flutter en Kubernetes
```

### Ejemplo 4: Comando explícito
```
@skill:mvvm - Genera una app de gestión de usuarios
@skill:terraform - Provision infrastructure en AWS
```

## 📖 Estructura de Cada Skill

Cada skill contiene:
- `README.md` - Documentación completa del skill
- Keywords para invocación
- Estructura del proyecto
- Ejemplos de código
- Dependencias recomendadas
- Guías de testing
- Mejores prácticas

## 🚀 Inicio Rápido

1. **Explora los skills** navegando a cada carpeta
2. **Lee la documentación** de cada skill
3. **Usa los keywords** en tus prompts con IA
4. **Combina skills** para proyectos complejos

## 🎨 Combinación de Skills

Puedes combinar múltiples skills en un solo proyecto:

```
Crea un proyecto con clean-arch + testing + cicd para una app de finanzas
```

## 📊 Niveles de Complejidad

- 🟢 **Básico:** Ideal para comenzar, conceptos fundamentales
- 🟡 **Intermedio:** Requiere conocimiento de Flutter y patrones
- 🔴 **Avanzado:** Requiere experiencia con arquitecturas complejas

## 🔧 Herramientas Requeridas

- Flutter SDK 3.35.0+
- Dart SDK 3.9+
- MCP Servers configurados (ver [`../docs/MCP_SETUP.md`](../docs/MCP_SETUP.md))

## 📚 Aprender Más

- Consulta [`/docs`](../docs/) para guías adicionales
- Lee el [README principal](../README.md) del proyecto
- Revisa [CONTRIBUTING](../docs/CONTRIBUTING.md) para contribuir

---

**💡 Tip:** Comienza con [`project-setup`](./project-setup/) seguido de [`mvvm`](./mvvm/) si eres nuevo en arquitecturas Flutter.
