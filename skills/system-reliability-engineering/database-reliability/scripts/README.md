# Database Reliability Scripts

Scripts ejecutables para gestión de confiabilidad de bases de datos: backups, restauración y limpieza.

## 📁 Archivos

- **`postgresql_backup.py`** - Automatización de backups y restauración de PostgreSQL
- **`requirements.txt`** - Dependencias (ninguna, usa solo stdlib)

## 🚀 Quick Start

### PostgreSQL Backup

No requiere instalación de dependencias Python (usa solo stdlib):

```bash
# Crear backup completo
python postgresql_backup.py backup \
  --host localhost \
  --user backup_user \
  --backup-dir /backup/postgresql

# Listar backups disponibles
python postgresql_backup.py list --backup-dir /backup/postgresql

# Limpiar backups antiguos (dry-run)
python postgresql_backup.py cleanup \
  --backup-dir /backup/postgresql \
  --retention-days 30 \
  --dry-run

# Restaurar desde backup
python postgresql_backup.py restore \
  --backup-path /backup/postgresql/full_20240115_120000 \
  --target-dir /var/lib/postgresql/data
```

## 📋 Requisitos del Sistema

El script requiere herramientas del sistema PostgreSQL:

- `pg_basebackup` - Para crear backups físicos
- `pg_verifybackup` - Para verificar backups (opcional)
- `tar` - Para extraer backups
- `systemctl` - Para gestionar servicios (opcional, puede hacerse manualmente)

## 📖 Documentación Completa

Ver [`../SKILL.md`](../SKILL.md) para documentación completa sobre:
- Configuración de replicación
- Failover automático
- Connection pooling
- Estrategias de backup
- Monitoreo de bases de datos
