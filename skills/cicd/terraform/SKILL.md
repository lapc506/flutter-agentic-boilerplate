---
name: cicd-terraform
description: "Provisions cloud infrastructure using Terraform with reusable HCL modules for Kubernetes, databases, and networking. Use when managing infrastructure-as-code with terraform, iac, hcl, or provisioning for multi-environment cloud deployments on AWS, GCP, or Azure."
---

# Terraform Infrastructure as Code

## Cuándo Usar

- Infraestructura multi-cloud, multi-entorno con versionado
- Reutilización de módulos (Kubernetes, databases, networking)
- State management centralizado con remote backend
- Infraestructura reproducible y disaster recovery

## Cuándo NO Usar

- Infraestructura muy simple o temporal
- Ya usas otra herramienta IaC (Pulumi, CDK)
- Preferencia por consola/CLI manual

## Estructura del Proyecto

```
infrastructure/
├── terraform/
│   ├── environments/
│   │   ├── dev/
│   │   ├── staging/
│   │   └── production/
│   │       ├── main.tf
│   │       ├── variables.tf
│   │       ├── outputs.tf
│   │       └── terraform.tfvars
│   ├── modules/
│   │   ├── kubernetes/
│   │   ├── database/
│   │   │   ├── postgres/
│   │   │   └── redis/
│   │   ├── storage/
│   │   └── networking/
│   ├── backend.tf
│   └── versions.tf
└── scripts/
    ├── init.sh
    └── deploy.sh
```

## Backend Configuration (S3 + DynamoDB)

```hcl
# infrastructure/terraform/backend.tf
terraform {
  required_version = ">= 1.6.0"

  backend "s3" {
    bucket               = "myapp-terraform-state"
    key                  = "infrastructure/terraform.tfstate"
    region               = "us-east-1"
    encrypt              = true
    dynamodb_table       = "terraform-lock"
    workspace_key_prefix = "env"
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.23"
    }
  }
}
```

## Módulo: Kubernetes Cluster (EKS)

```hcl
# infrastructure/terraform/modules/kubernetes/main.tf
resource "aws_eks_cluster" "main" {
  name     = var.cluster_name
  role_arn = aws_iam_role.cluster.arn
  version  = var.kubernetes_version

  vpc_config {
    subnet_ids              = var.subnet_ids
    endpoint_private_access = true
    endpoint_public_access  = var.enable_public_access
    security_group_ids      = [aws_security_group.cluster.id]
  }

  encryption_config {
    provider { key_arn = aws_kms_key.eks.arn }
    resources = ["secrets"]
  }

  tags = merge(var.tags, {
    Name        = var.cluster_name
    Environment = var.environment
    ManagedBy   = "Terraform"
  })
}

resource "aws_eks_node_group" "main" {
  cluster_name    = aws_eks_cluster.main.name
  node_group_name = "${var.cluster_name}-node-group"
  node_role_arn   = aws_iam_role.node.arn
  subnet_ids      = var.private_subnet_ids
  instance_types  = var.instance_types
  capacity_type   = var.capacity_type  # ON_DEMAND or SPOT

  scaling_config {
    desired_size = var.desired_nodes
    max_size     = var.max_nodes
    min_size     = var.min_nodes
  }

  tags = var.tags
}
```

Key variables: `cluster_name`, `kubernetes_version` (default `"1.28"`), `subnet_ids`, `private_subnet_ids`, `desired_nodes` (default `3`), `min_nodes` (default `2`), `max_nodes` (default `10`), `instance_types` (default `["t3.medium"]`), `capacity_type` (default `"ON_DEMAND"`).

Key outputs: `cluster_id`, `cluster_endpoint`, `cluster_certificate_authority_data` (sensitive), `cluster_security_group_id`.

## Environment Configuration Pattern

```hcl
# infrastructure/terraform/environments/production/main.tf
provider "aws" {
  region = var.aws_region
  default_tags {
    tags = {
      Project     = "MyApp"
      Environment = "production"
      ManagedBy   = "Terraform"
    }
  }
}

module "eks" {
  source             = "../../modules/kubernetes"
  cluster_name       = "myapp-prod"
  kubernetes_version = "1.28"
  environment        = "production"
  subnet_ids         = module.vpc.public_subnet_ids
  private_subnet_ids = module.vpc.private_subnet_ids
  desired_nodes      = 5
  min_nodes          = 3
  max_nodes          = 20
  instance_types     = ["t3.large", "t3.xlarge"]
  tags               = local.common_tags
}

module "database" {
  source          = "../../modules/database/postgres"
  identifier      = "myapp-prod-db"
  environment     = "production"
  instance_class  = "db.r6g.large"
  multi_az        = true
  master_password = data.aws_secretsmanager_secret_version.db_password.secret_string
  tags            = local.common_tags
}

locals {
  common_tags = {
    Project     = "MyApp"
    Environment = "production"
    ManagedBy   = "Terraform"
    Team        = "Platform"
  }
}
```

## Mejores Prácticas

- **Secrets**: usar AWS Secrets Manager — nunca hardcodear contraseñas en HCL.
- **Naming**: `{project}-{environment}-{resource}` (e.g. `myapp-prod-cluster`).
- **Tagging**: `merge(local.common_tags, var.additional_tags)` en todos los recursos.
- **Module versioning**: pinear versiones con `version = "~> 5.0"`.
- **State locking**: siempre usar DynamoDB con el backend S3.

## Comandos Esenciales

```bash
terraform init                          # Inicializar
terraform validate                      # Validar configuración
terraform fmt -recursive                # Formatear código
terraform plan -out=tfplan              # Plan de cambios
terraform apply tfplan                  # Aplicar cambios
terraform workspace select production   # Cambiar workspace
terraform output                        # Ver outputs
terraform import aws_instance.ex i-123  # Importar recurso existente
```

## Recursos

- [Terraform Registry](https://registry.terraform.io/)
- [Terraform Best Practices](https://www.terraform-best-practices.com/)
- [AWS Provider Docs](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- Skills relacionados: `cicd/github-actions`, `cicd/argocd`, `cicd/kubernetes`
