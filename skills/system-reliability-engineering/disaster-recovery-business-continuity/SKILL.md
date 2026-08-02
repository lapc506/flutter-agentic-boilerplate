# 🆘 Skill: Disaster Recovery & Business Continuity

## 📋 Metadata

| Atributo | Valor |
|----------|-------|
| **ID** | `sre-disaster-recovery-business-continuity` |
| **Nivel** | 🔴 Avanzado |
| **Versión** | 1.0.0 |
| **Keywords** | `disaster-recovery`, `business-continuity`, `backup`, `failover`, `rpo`, `rto`, `dr-plan`, `gcp`, `opentofu`, `irreversible-choices`, `state-protection` |
| **Referencia** | [AWS Disaster Recovery](https://aws.amazon.com/disaster-recovery/) |

## 🔑 Keywords para Invocación

- `disaster-recovery`
- `business-continuity`
- `backup-strategy`
- `failover`
- `rpo`
- `rto`
- `dr-plan`
- `opentofu`
- `prevent-destroy`
- `cloud-run`
- `@skill:disaster-recovery`

### Ejemplos de Prompts

```
Implementa disaster recovery plan con RPO y RTO
```

```
Configura backup strategy y failover procedures
```

```
Setup business continuity plan para servicios críticos
```

```
@skill:disaster-recovery - Plan completo de DR y BC
```

```
Proteger estado en OpenTofu contra un destroy o un replace accidental
```

```
El tofu plan sale verde pero el cambio no llegó a las máquinas
```

## 📖 Descripción

Disaster Recovery (DR) y Business Continuity (BC) aseguran que servicios críticos puedan recuperarse rápidamente de desastres. Este skill cubre DR planning, backup strategies, failover procedures, RPO/RTO definitions, y testing procedures.

### ✅ Cuándo Usar Este Skill

- Servicios críticos en producción
- SLAs estrictos
- Compliance requirements
- Data protection requirements
- High availability requirements

### ❌ Cuándo NO Usar Este Skill

- Servicios no críticos
- Desarrollo local
- Prototipos sin datos reales

## 🏗️ DR Strategy Framework

```
RPO (Recovery Point Objective)
    ↓
Backup Frequency
    ↓
RTO (Recovery Time Objective)
    ↓
Failover Procedures
```

## 💻 Implementación

> **📁 Scripts Ejecutables:** Este skill incluye scripts ejecutables en la carpeta [`scripts/`](scripts/):
> - [`backup-strategy.sh`](scripts/backup-strategy.sh) - Estrategia automatizada de backups (Bash)
> - [`failover_procedures.py`](scripts/failover_procedures.py) - Gestor de procedimientos de failover (Python CLI)
> - [`dr-test.sh`](scripts/dr-test.sh) - Script completo de testing de DR (Bash)
> - [`requirements.txt`](scripts/requirements.txt) - Dependencias (ninguna, usa stdlib)
>
> Ver [`scripts/README.md`](scripts/README.md) para documentación de uso.

### 1. RPO/RTO Definitions

```yaml
# dr/rpo-rto-definitions.yml
services:
  - name: payment-service
    rpo: 5m      # Maximum 5 minutes of data loss
    rto: 15m     # Recovery within 15 minutes
    priority: critical
    backup_strategy: continuous

  - name: user-service
    rpo: 1h      # Maximum 1 hour of data loss
    rto: 30m     # Recovery within 30 minutes
    priority: high
    backup_strategy: hourly

  - name: analytics-service
    rpo: 24h     # Maximum 24 hours of data loss
    rto: 2h      # Recovery within 2 hours
    priority: medium
    backup_strategy: daily
```

### 2. Backup Strategy

**Script ejecutable:** [`scripts/backup-strategy.sh`](scripts/backup-strategy.sh)

Script Bash completo para automatizar estrategia de backups con soporte para backups completos, incrementales, verificación y limpieza.

#### Cuándo ejecutar

- **Backups programados:** Como parte de cron jobs (diarios/horarios)
- **Backups manuales:** Para crear backups bajo demanda
- **Verificación:** Para validar integridad de backups antes de restaurar
- **Limpieza:** Para mantener espacio de almacenamiento bajo control

#### Uso

```bash
# Hacer ejecutable
chmod +x scripts/backup-strategy.sh

# Backup completo (diario)
./scripts/backup-strategy.sh full

# Backup incremental (horario)
./scripts/backup-strategy.sh incremental

# Limpiar backups antiguos
./scripts/backup-strategy.sh cleanup

# Verificar backup
./scripts/backup-strategy.sh verify /backup/full/20240115

# Listar backups disponibles
./scripts/backup-strategy.sh list
```

#### Configuración

Variables de entorno:

```bash
export BACKUP_DIR="/backup"              # Directorio de backups
export RETENTION_DAYS=30                 # Días de retención
export S3_BUCKET="backup-bucket"         # Bucket S3 (opcional)
export DB_HOST="localhost"              # Host de base de datos
export DB_USER="backup_user"             # Usuario de backup
export DB_NAME="mydb"                    # Nombre de base de datos
export APP_DATA_DIR="/var/app/data"      # Directorio de datos de aplicación
```

#### Características

- ✅ Backups completos e incrementales
- ✅ Verificación automática de integridad
- ✅ Upload a S3 (opcional)
- ✅ Limpieza automática con política de retención
- ✅ Logging con colores
- ✅ Manejo de errores robusto

### 3. Failover Procedures

**Script ejecutable:** [`scripts/failover_procedures.py`](scripts/failover_procedures.py)

Gestor completo de procedimientos de failover con registro de servicios, health checks, y ejecución automatizada de failover.

#### Cuándo ejecutar

- **Registro de servicios:** Al configurar nuevos servicios para DR
- **Failover manual:** Cuando se detecta un desastre y se necesita failover
- **Failover automatizado:** Integrado con sistemas de monitoreo
- **Testing:** Para probar procedimientos de failover (dry-run)

#### Uso

```bash
# Registrar servicio
python scripts/failover_procedures.py register \
  --name payment-service \
  --primary us-east-1 \
  --standby us-west-2 \
  --rto 15 \
  --rpo 5

# Ejecutar failover
python scripts/failover_procedures.py failover payment-service

# Dry-run (simular sin cambios)
python scripts/failover_procedures.py failover payment-service --dry-run

# Ver estado de servicio
python scripts/failover_procedures.py status payment-service

# Ver estado de todos los servicios
python scripts/failover_procedures.py status

# Listar servicios registrados
python scripts/failover_procedures.py list
```

#### Características

- ✅ Registro y gestión de servicios
- ✅ Health checks de standby
- ✅ Promoción automática de standby a primary
- ✅ Actualización de routing (DNS/load balancer)
- ✅ Verificación de failover
- ✅ Modo dry-run para testing
- ✅ Persistencia de configuración en JSON
- ✅ Tracking de último failover

### 4. DR Testing

**Script ejecutable:** [`scripts/dr-test.sh`](scripts/dr-test.sh)

Script completo de testing de Disaster Recovery que simula un desastre y verifica todos los procedimientos de recuperación.

#### Cuándo ejecutar

- **Testing regular:** Ejecutar periódicamente (mensual/trimestral) para validar procedimientos
- **Después de cambios:** Después de modificar configuración de DR
- **Entrenamiento:** Para entrenar al equipo en procedimientos de DR
- **Validación:** Antes de aprobar cambios en producción

#### Uso

```bash
# Hacer ejecutable
chmod +x scripts/dr-test.sh

# Test completo
./scripts/dr-test.sh payment-service

# Test sin simular desastre (solo verificar procedimientos)
DR_TEST_SKIP_SIMULATION=true ./scripts/dr-test.sh payment-service

# Test sin failback (más rápido)
DR_TEST_SKIP_FAILBACK=true ./scripts/dr-test.sh payment-service
```

#### Fases del Test

1. **Pre-test checklist** - Verifica backups, standby health, documentación
2. **Simular desastre** - Detiene servicio primary (simulado)
3. **Ejecutar failover** - Ejecuta procedimiento de failover
4. **Verificar disponibilidad** - Confirma que servicio está disponible
5. **Restaurar primary** - Restaura servicio primary
6. **Failback** - Ejecuta procedimiento de failback
7. **Post-test verification** - Verifica salud del servicio y consistencia de datos

#### Características

- ✅ Checklist pre-test completo
- ✅ Simulación de desastre
- ✅ Verificación de cada fase
- ✅ Logging detallado con colores
- ✅ Opciones para saltar fases (testing parcial)
- ✅ Verificación de consistencia de datos

### 5. Multi-Region Setup

```yaml
# k8s/multi-region-deployment.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: dr-config
data:
  primary_region: "us-east-1"
  standby_region: "us-west-2"
  failover_threshold: "5m"
  rpo_minutes: "5"
  rto_minutes: "15"
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: payment-service-primary
  labels:
    app: payment-service
    region: primary
spec:
  replicas: 3
  selector:
    matchLabels:
      app: payment-service
      region: primary
  template:
    metadata:
      labels:
        app: payment-service
        region: primary
    spec:
      containers:
      - name: app
        image: payment-service:latest
        env:
        - name: REGION
          value: "primary"
        - name: REPLICATION_MODE
          value: "master"
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: payment-service-standby
  labels:
    app: payment-service
    region: standby
spec:
  replicas: 2
  selector:
    matchLabels:
      app: payment-service
      region: standby
  template:
    metadata:
      labels:
        app: payment-service
        region: standby
    spec:
      containers:
      - name: app
        image: payment-service:latest
        env:
        - name: REGION
          value: "standby"
        - name: REPLICATION_MODE
          value: "replica"
```

### 6. DR sobre GCP + OpenTofu: decisiones irreversibles y planes que no llegan

> **Todo lo de arriba sigue vigente.** RPO/RTO, la estrategia de backups, los
> procedimientos de failover y el multi-región siguen siendo el camino. Esta sección agrega
> dos cosas que un stack declarado en OpenTofu introduce y que ningún runbook de arriba
> cubre: **elecciones que no se pueden deshacer**, y **planes verdes que no llegan a la
> máquina**.

#### 6.1 Elegí el almacén por su MODO DE FALLA, no por costo ni comodidad

Es el mismo criterio que gobierna un plan de DR, aplicado un nivel más abajo: **no importa
tanto qué tan seguido falla, importa qué se ve cuando falla.**

*Comparación tomada de
`dojo-os @ origin/develop:openspec/changes/2026-08-02-observability-liveness-axis/design.md`;
las filas describen el razonamiento de esa decisión, **no un benchmark corrido acá**.*

| candidato | qué pasa cuando el almacén no responde |
|---|---|
| **Firestore en modo Datastore** | **lanza un error atrapable** — se distingue de "no hay datos" |
| Objeto en GCS | lanza, pero un objeto corrupto pierde las N unidades de una |
| Valkey / Redis | un reinicio de instancia deja **todas** las claves ausentes → se lee "todo muerto" |
| SaaS de cron monitoring | **falla hacia el silencio**: si el proveedor está caído, nadie se entera |

La cuarta fila es la peor para DR: un componente que **falla hacia el silencio** es
indistinguible de uno sano, y es exactamente el que no querés en el camino de recuperación.

#### 6.2 Una elección irreversible se declara en código, nunca se clickea

**El modo de una base Firestore —Native o Datastore— no se puede cambiar después**, y un
proyecto sostiene una sola. Es la definición de decisión irreversible, y por eso es lo
último que debería vivir en una consola: en un archivo versionado tiene diff, revisor y
fecha; en una consola no tiene ninguno de los tres.

```hcl
# tofu/heartbeat-liveness.tf — DojoCodingLabs/dojo-infra-gitops PR #48
resource "google_firestore_database" "heartbeat" {
  project     = var.alerts_project_id
  name        = "(default)"
  location_id = var.region
  type        = "DATASTORE_MODE"   # IRREVERSIBLE

  # Un `tofu destroy` no puede llevarse el historial con él.
  deletion_policy = "ABANDON"

  lifecycle {
    # El modo es irreversible y la ubicación no se puede mover. Un plan que propone
    # REEMPLAZAR esta base es un plan que propone perder los datos, y tiene que fallar
    # ruidosamente en vez de aplicar callado.
    prevent_destroy = true
  }
}
```

**Los dos atributos hacen cosas distintas y hacen falta los dos:**

| atributo | contra qué protege |
|---|---|
| `prevent_destroy = true` | contra un `plan` que propone **recrear** el recurso (cambio de atributo ForceNew) |
| `deletion_policy = "ABANDON"` | contra que un `tofu destroy` deliberado se lleve los datos con la declaración |

**Checklist para cualquier recurso con estado en un árbol de OpenTofu:**

- [ ] ¿Alguno de sus atributos es ForceNew? Listalos en un comentario **arriba del recurso**.
- [ ] ¿La elección es reversible? Si no, decilo en el comentario y agregá `prevent_destroy`.
- [ ] ¿El `destroy` se lleva datos? `deletion_policy` / `skip_final_snapshot = false`.
- [ ] ¿El recurso ya existe en la nube? Entonces necesita un **`import` block**, no un
      `apply` — sin eso, `apply` crea un **segundo** conjunto al lado del vivo y nada da
      error. (Ver el skill `alerting-incident-management`, §7.5.)

#### 6.3 Un `tofu plan` verde NO es un cambio entregado

Este es el que más caro sale, porque el gate está verde y la conclusión razonable es la
equivocada.

*Reportado por quien lo midió en `DojoCodingLabs/dojo-infra-gitops` PR #23 (merge
`7231482`, 2026-07-31) y **no re-corrido en este pase**:* un cambio a
`tofu/modules/runner-pool/startup.sh.tftpl` produce
`No changes. Your infrastructure matches the configuration.`, y el `apply` post-merge
reporta `0 added, 0 changed, 0 destroyed`. Las cinco VMs **sí** están en el state y **sí**
se refrescan. Igual: cero diff.

**Los dos mecanismos que lo causan sí se verificaron de primera mano**, leyendo el ref
(`git show origin/main:<archivo>` sobre `dojo-infra-gitops @ origin/main d6e59f0`). Son
independientes y los dos deliberados y preexistentes:

```hcl
# tofu/modules/runner-pool/main.tf:74-78
# El registration token cambia en cada apply (vive una hora), y un token cambiado NO debe
# recrear una VM viva a mitad de job.
lifecycle {
  ignore_changes = [metadata["startup-script"]]
}
```

```bash
# tofu/modules/runner-pool/startup.sh.tftpl:125
# Aunque el script nuevo llegara a una VM viva, es no-op en un host ya aprovisionado.
if [ -f /var/lib/dojo-runner-provisioned ]; then
  log "already provisioned; nothing to do"
  exit 0
fi
```

El primero **suprime exactamente el campo que cualquier cambio al script toca**. El segundo
lo neutraliza aunque llegue.

> **Un `plan` verde sobre un cambio de startup script es el gate mirando la propiedad
> ADYACENTE.** El cambio aplica solo a VMs **creadas después** del merge. Llevarlo a la
> flota viva es un *replace* de VMs: una operación de flota aparte, con su propia ventana y
> su propio riesgo.

**Qué hacer con eso, en un contexto de DR:**

1. **Decilo explícitamente en el PR.** Quien ve `plan` verde concluye razonablemente que el
   merge arregla el problema que motivó el cambio, y no lo hace.
2. **Verificá contra la máquina, no contra el plan.** El comando que contesta es el que
   interroga al host o al proveedor, nunca el que interroga al state.
3. **Y el comentario de `plan` en el PR viene TRUNCADO** (`…output truncated, see the job
   log for the full plan…`), así que **la ausencia de un recurso ahí no es evidencia de
   nada**. Hay que ir al log del job.

#### 6.4 Las cuatro trampas de despliegue que rompen un failover a GCP

Nombradas acá porque las cuatro se descubren tarde, en el peor momento posible.

| trampa | qué pasa | cómo se evita |
|---|---|---|
| **Secreto sin versión** | **Cloud Run rechaza la revisión entera** y nunca la crea. No es que arranque y falle al leer. Un contenedor creado y vacío cuenta como sin versión | crear la versión **antes** de referenciarla; y dejar de montar lo que nadie lee |
| **Sin `--service-account`** | el servicio corre con la identidad por defecto de Compute Engine, que nadie eligió. Otorgarle un rol se lo otorga a **todas** las VMs del proyecto | pasar `--service-account` explícito; verificado con `grep -c 'service-account' scripts/deploy.sh` → **0** en `dojo-infra-alerts @ origin/main 2304b6e` |
| **API no habilitada** | el recurso se declara, el tick nunca dispara, y todo reporta `success` | declarar `google_project_service` y confirmar con `gcloud services list --enabled` |
| **Proyecto heredado del provider** | el recurso se crea en el proyecto equivocado y llama a nada mientras reporta éxito | nombrar `project` **explícitamente en cada recurso**, no heredarlo |

**Y la regla que las cubre a las cuatro:** en un `tofu`, una variable sin setear tiene que
producir **cero recursos**, no un recurso apuntando a nada.

```hcl
locals { heartbeat_enabled = var.alerts_service_url != "" }

resource "google_cloud_scheduler_job" "heartbeat_liveness" {
  count = local.heartbeat_enabled ? 1 : 0
  # ...
}

output "heartbeat_liveness_job" {
  # Vacío es una respuesta real acá, y se reporta como tal en vez de como un blanco.
  value = local.heartbeat_enabled ? (
    google_cloud_scheduler_job.heartbeat_liveness[0].name
  ) : "NOT CREATED: alerts_service_url is unset"
}
```

#### 6.5 Un DR test que reporta "no pasó nada" no probó nada

El `dr-test.sh` de este skill simula un desastre y verifica los procedimientos. **Antes de
confiar en su resultado**, verificá que los controles de los que depende puedan ponerse en
rojo: un test de DR sobre infraestructura no instrumentada reporta éxito y se lee como
resiliencia. Ver el skill `chaos-engineering`, §6, que documenta la secuencia de cinco pasos
para validar un control antes de usarlo como instrumento de medición.

## 🎯 Mejores Prácticas

### 1. RPO/RTO

✅ **DO:**
- Define realistic RPO/RTO
- Align with business requirements
- Test regularly
- Document assumptions

❌ **DON'T:**
- Set unrealistic targets
- Ignore business impact
- Skip testing

### 2. Backups

✅ **DO:**
- Test restore procedures
- Store backups off-site
- Encrypt backups
- Verify backup integrity

❌ **DON'T:**
- Assume backups work
- Skip verification
- Store in same location

### 3. Failover

✅ **DO:**
- Test failover regularly
- Document procedures
- Monitor failover events
- Practice with team

❌ **DON'T:**
- Skip failover testing
- Ignore documentation
- Test only in emergencies

## 🚨 Troubleshooting

### Backup Failures

1. Check disk space
2. Verify permissions
3. Review backup logs
4. Test restore procedures

### Failover Issues

1. Verify standby health
2. Check network connectivity
3. Review failover procedures
4. Test in non-production first

## 📚 Recursos Adicionales

- [AWS Disaster Recovery](https://aws.amazon.com/disaster-recovery/)
- [Google SRE - Disaster Recovery](https://sre.google/workbook/disaster-recovery/)
- [DR Planning Guide](https://www.ready.gov/business/emergency-plans/continuity-planning)

---

**Versión:** 1.0.0
**Última actualización:** Diciembre 2025
**Total líneas:** 1,100+
