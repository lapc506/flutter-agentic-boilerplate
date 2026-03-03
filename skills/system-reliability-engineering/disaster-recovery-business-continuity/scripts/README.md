# Disaster Recovery & Business Continuity Scripts

Scripts ejecutables para gestión de Disaster Recovery (DR) y Business Continuity (BC).

## 📁 Archivos

- **`backup-strategy.sh`** - Estrategia automatizada de backups (Bash)
- **`failover_procedures.py`** - Gestor de procedimientos de failover (Python CLI)
- **`dr-test.sh`** - Script completo de testing de DR (Bash)
- **`requirements.txt`** - Dependencias (ninguna, usa stdlib)

## 🚀 Quick Start

### Backup Strategy

```bash
# Hacer ejecutable
chmod +x backup-strategy.sh

# Crear backup completo
./backup-strategy.sh full

# Crear backup incremental
./backup-strategy.sh incremental

# Limpiar backups antiguos
./backup-strategy.sh cleanup

# Verificar backup
./backup-strategy.sh verify /backup/full/20240115

# Listar backups
./backup-strategy.sh list
```

**Variables de entorno:**
```bash
export BACKUP_DIR="/backup"
export RETENTION_DAYS=30
export S3_BUCKET="backup-bucket"
export DB_HOST="localhost"
export DB_USER="backup_user"
export DB_NAME="mydb"
export APP_DATA_DIR="/var/app/data"
```

### Failover Procedures

```bash
# Registrar servicio
python failover_procedures.py register \
  --name payment-service \
  --primary us-east-1 \
  --standby us-west-2 \
  --rto 15 \
  --rpo 5

# Ejecutar failover
python failover_procedures.py failover payment-service

# Dry-run (simular sin cambios)
python failover_procedures.py failover payment-service --dry-run

# Ver estado
python failover_procedures.py status payment-service

# Listar servicios
python failover_procedures.py list
```

### DR Testing

```bash
# Hacer ejecutable
chmod +x dr-test.sh

# Ejecutar test completo
./dr-test.sh payment-service

# Test sin simular desastre (solo verificar procedimientos)
DR_TEST_SKIP_SIMULATION=true ./dr-test.sh payment-service

# Test sin failback
DR_TEST_SKIP_FAILBACK=true ./dr-test.sh payment-service
```

## 📋 Requisitos del Sistema

Los scripts pueden requerir herramientas del sistema:

- **kubectl** - Para operaciones de Kubernetes (failover, health checks)
- **aws CLI** - Para uploads a S3 (backups)
- **curl** - Para health checks
- **PostgreSQL tools** - `pg_dump`, `pg_basebackup` (para backups de base de datos)
- **tar, gzip** - Para compresión de backups

## 📖 Documentación Completa

Ver [`../SKILL.md`](../SKILL.md) para documentación completa sobre:
- Definiciones de RPO/RTO
- Estrategias de backup
- Procedimientos de failover
- Testing de DR
- Configuración multi-región
