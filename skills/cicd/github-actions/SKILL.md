---
name: cicd-github-actions
description: "Configures GitHub Actions CI/CD pipelines for Flutter monorepos with automated testing, building, and deployment. Use when setting up github-actions, ci, cd, pipeline, automation, or workflow for Flutter mobile apps and backends hosted on GitHub."
---

# GitHub Actions CI/CD

## Cuándo Usar

- Proyecto alojado en GitHub con necesidad de CI/CD integrado nativamente
- Monorepo con frontend Flutter + backend (Node.js, Python, Go, etc.)
- Pipelines simples a medianos con free tier generoso (2000 min/mes)

## Cuándo NO Usar

- Proyecto en GitLab/Bitbucket
- Runners on-premise complejos requeridos
- Preferencia por otras herramientas CI/CD (CircleCI, Jenkins, etc.)

## Estructura de Monorepo

```
my-app-monorepo/
├── .github/
│   └── workflows/
│       ├── flutter-ci.yml
│       ├── flutter-cd.yml
│       ├── backend-ci.yml
│       ├── backend-cd.yml
│       └── monorepo-pr.yml
├── mobile/                    # Flutter app
├── backend/                   # Backend (Node.js/Python/Go)
├── infrastructure/            # IaC (Terraform/etc)
└── shared/                    # Shared code/protos
```

## Flutter CI Workflow

```yaml
# .github/workflows/flutter-ci.yml
name: Flutter CI

on:
  push:
    branches: [main, develop]
    paths:
      - 'mobile/**'
      - '.github/workflows/flutter-ci.yml'
  pull_request:
    branches: [main, develop]
    paths:
      - 'mobile/**'

jobs:
  analyze:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: mobile
    steps:
      - uses: actions/checkout@v4
      - uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.35.0'
          channel: 'stable'
          cache: true
      - run: flutter pub get
      - run: dart format --output=none --set-exit-if-changed .
      - run: flutter analyze --fatal-infos

  test:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: mobile
    steps:
      - uses: actions/checkout@v4
      - uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.35.0'
          channel: 'stable'
          cache: true
      - run: flutter pub get
      - run: flutter test --coverage --reporter expanded
      - uses: codecov/codecov-action@v3
        with:
          files: ./mobile/coverage/lcov.info
          flags: flutter

  build-android:
    needs: [analyze, test]
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: mobile
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          distribution: 'zulu'
          java-version: '17'
          cache: 'gradle'
      - uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.35.0'
          channel: 'stable'
          cache: true
      - run: flutter pub get
      - run: flutter build appbundle --release
      - uses: actions/upload-artifact@v4
        with:
          name: android-aab
          path: mobile/build/app/outputs/bundle/release/app-release.aab
          retention-days: 7

  build-ios:
    needs: [analyze, test]
    runs-on: macos-latest
    defaults:
      run:
        working-directory: mobile
    steps:
      - uses: actions/checkout@v4
      - uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.35.0'
          channel: 'stable'
          cache: true
      - run: flutter pub get
      - run: flutter build ios --release --no-codesign
      - uses: actions/upload-artifact@v4
        with:
          name: ios-build
          path: mobile/build/ios/iphoneos/
          retention-days: 7
```

## CD Pattern (Tag-based)

CD workflows se disparan con tags versionados:

- `mobile-v*.*.*` — deploy Android (Play Store) e iOS (TestFlight)
- `backend-v*.*.*` — build/push Docker image y deploy a Kubernetes

```bash
# Release mobile
git tag -a mobile-v1.0.0 -m "Mobile release 1.0.0" && git push origin mobile-v1.0.0

# Release backend
git tag -a backend-v1.0.0 -m "Backend release 1.0.0" && git push origin backend-v1.0.0
```

## Reusable Workflows

```yaml
# .github/workflows/reusable-flutter-test.yml
on:
  workflow_call:
    inputs:
      working-directory:
        required: true
        type: string
      flutter-version:
        required: false
        type: string
        default: '3.35.0'

jobs:
  test:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: ${{ inputs.working-directory }}
    steps:
      - uses: actions/checkout@v4
      - uses: subosito/flutter-action@v2
        with:
          flutter-version: ${{ inputs.flutter-version }}
          cache: true
      - run: flutter pub get
      - run: flutter test --coverage
```

## Secrets Configuration

Configurar en: **Settings > Secrets and variables > Actions**

**Mobile:**
- `KEYSTORE_BASE64`, `KEYSTORE_PASSWORD`, `KEY_ALIAS`, `KEY_PASSWORD`
- `PLAY_STORE_CREDENTIALS`, `APP_STORE_ISSUER_ID`, `APP_STORE_API_KEY_ID`, `APP_STORE_API_PRIVATE_KEY`

**Backend/Infra:**
- `DOCKER_USERNAME`, `DOCKER_PASSWORD`, `KUBECONFIG`
- `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`

**General:**
- `CODECOV_TOKEN`, `SLACK_WEBHOOK_URL`

## Mejores Prácticas

- **Path filtering**: usar `paths:` para ejecutar workflows solo cuando cambien archivos relevantes
- **Caching**: habilitar `cache: true` en `subosito/flutter-action@v2` y `cache: 'gradle'` en setup-java
- **Matrix strategy**: `matrix: { node-version: [18.x, 20.x] }` para testear múltiples versiones
- **Environments**: usar `environment: production` en jobs de deploy para requerir approval manual
- **Concurrency control**: cancelar runs anteriores del mismo PR con `concurrency.cancel-in-progress: true`

## Skills Relacionados

- [Terraform](../terraform/SKILL.md) - Infrastructure as Code
- [ArgoCD](../argocd/SKILL.md) - GitOps deployment
- [Docker](../docker/SKILL.md) - Containerization
