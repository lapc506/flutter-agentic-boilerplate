---
name: cicd-argocd
description: "Configures ArgoCD GitOps deployment for Kubernetes clusters with Kustomize overlays and multi-environment promotion. Use when deploying backends to Kubernetes with argocd, gitops, continuous-deployment, or k8s-deployment workflows requiring declarative sync and rollback."
---

# ArgoCD GitOps Deployment

## Cuándo Usar

- Deployments a Kubernetes con GitOps workflow
- Múltiples ambientes (dev/staging/prod) con Kustomize overlays
- Rollbacks automáticos y audit trail completo
- Self-healing applications

## Cuándo NO Usar

- No usas Kubernetes
- Deployments simples sin múltiples ambientes
- Preferencia por CI/CD imperativo tradicional

## Estructura del Proyecto

```
my-app-monorepo/
├── k8s/
│   ├── argocd/
│   │   ├── applications/
│   │   │   ├── backend-dev.yaml
│   │   │   ├── backend-staging.yaml
│   │   │   └── backend-prod.yaml
│   │   ├── app-of-apps.yaml
│   │   └── projects.yaml
│   ├── base/backend/
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   └── kustomization.yaml
│   └── overlays/
│       ├── dev/backend/
│       ├── staging/backend/
│       └── production/backend/
└── backend/Dockerfile
```

## Instalación

```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
kubectl patch svc argocd-server -n argocd -p '{"spec": {"type": "LoadBalancer"}}'
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
argocd login <ARGOCD_SERVER>
```

## Configuración de AppProject

```yaml
# k8s/argocd/projects.yaml
apiVersion: argoproj.io/v1alpha1
kind: AppProject
metadata:
  name: myapp
  namespace: argocd
spec:
  sourceRepos:
    - 'https://github.com/myorg/myapp-monorepo.git'
  destinations:
    - namespace: 'myapp-*'
      server: https://kubernetes.default.svc
    - namespace: production
      server: https://kubernetes.default.svc
  namespaceResourceWhitelist:
    - group: 'apps'
      kind: Deployment
    - group: ''
      kind: Service
    - group: 'networking.k8s.io'
      kind: Ingress
```

## Configuración de Application

```yaml
# k8s/argocd/applications/backend-prod.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: backend-prod
  namespace: argocd
  finalizers:
    - resources-finalizer.argocd.argoproj.io
spec:
  project: myapp
  source:
    repoURL: https://github.com/myorg/myapp-monorepo.git
    targetRevision: main
    path: k8s/overlays/production/backend
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
      - PruneLast=true
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m
```

## Kustomize Overlay (Producción)

```yaml
# k8s/overlays/production/backend/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
namespace: production
bases:
  - ../../../base/backend
replicas:
  - name: backend
    count: 5
images:
  - name: myorg/backend
    newTag: v1.2.3
patches:
  - path: patches/resources.yaml
  - path: patches/hpa.yaml
```

## Sync Waves y Hooks

```yaml
# Orden de deployment con sync waves
apiVersion: v1
kind: ConfigMap
metadata:
  name: database-config
  annotations:
    argocd.argoproj.io/sync-wave: "0"  # Deploy primero
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
  annotations:
    argocd.argoproj.io/sync-wave: "1"  # Deploy después del ConfigMap
---
apiVersion: batch/v1
kind: Job
metadata:
  name: db-migration
  annotations:
    argocd.argoproj.io/hook: PreSync
    argocd.argoproj.io/hook-delete-policy: BeforeHookCreation
```

## CLI Commands Esenciales

```bash
argocd app list
argocd app get backend-prod
argocd app sync backend-prod
argocd app rollback backend-prod
argocd app set backend-prod --kustomize-image myorg/backend:v1.2.4
argocd app wait backend-prod --sync
```

## Environment Promotion

```bash
# Promover de dev a staging
argocd app set backend-staging --kustomize-image myorg/backend:v1.2.3

# Promover de staging a producción (aprobación manual)
argocd app set backend-prod --kustomize-image myorg/backend:v1.2.3
```

## Referencias

- [ArgoCD Documentation](https://argo-cd.readthedocs.io/)
- [Kustomize Documentation](https://kustomize.io/)
- Skills relacionados: [Kubernetes](../kubernetes/SKILL.md), [GitHub Actions](../github-actions/SKILL.md)
