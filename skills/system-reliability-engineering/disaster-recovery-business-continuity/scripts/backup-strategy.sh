#!/bin/bash
#
# Backup Strategy Script
#
# Automated backup strategy for disaster recovery with:
# - Full backups (daily)
# - Incremental backups (hourly)
# - S3 upload
# - Backup verification
# - Cleanup of old backups
#
# Usage:
#   ./backup-strategy.sh full          # Create full backup
#   ./backup-strategy.sh incremental   # Create incremental backup
#   ./backup-strategy.sh cleanup       # Cleanup old backups
#   ./backup-strategy.sh verify <path> # Verify backup
#

set -euo pipefail

# Configuration
BACKUP_DIR="${BACKUP_DIR:-/backup}"
RETENTION_DAYS="${RETENTION_DAYS:-30}"
S3_BUCKET="${S3_BUCKET:-backup-bucket}"
DB_HOST="${DB_HOST:-localhost}"
DB_USER="${DB_USER:-backup_user}"
DB_NAME="${DB_NAME:-mydb}"
APP_DATA_DIR="${APP_DATA_DIR:-/var/app/data}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

# Full backup (daily)
backup_full() {
    log_info "Starting full backup..."

    DATE=$(date +%Y%m%d)
    BACKUP_PATH="$BACKUP_DIR/full/$DATE"
    mkdir -p "$BACKUP_PATH"

    log_info "Backing up database..."
    # Database backup
    if command -v pg_dump &> /dev/null; then
        pg_dump -h "$DB_HOST" -U "$DB_USER" "$DB_NAME" | gzip > "$BACKUP_PATH/db.sql.gz"
        log_info "Database backup completed: $BACKUP_PATH/db.sql.gz"
    else
        log_warn "pg_dump not found, skipping database backup"
    fi

    log_info "Backing up application data..."
    # Application data backup
    if [ -d "$APP_DATA_DIR" ]; then
        tar -czf "$BACKUP_PATH/app-data.tar.gz" -C "$(dirname "$APP_DATA_DIR")" "$(basename "$APP_DATA_DIR")"
        log_info "Application data backup completed: $BACKUP_PATH/app-data.tar.gz"
    else
        log_warn "Application data directory not found: $APP_DATA_DIR"
    fi

    # Upload to S3 if configured
    if [ -n "$S3_BUCKET" ] && command -v aws &> /dev/null; then
        log_info "Uploading to S3: s3://$S3_BUCKET/backups/full/$DATE/"
        aws s3 cp "$BACKUP_PATH" "s3://$S3_BUCKET/backups/full/$DATE/" --recursive || {
            log_error "Failed to upload to S3"
            return 1
        }
        log_info "S3 upload completed"
    else
        log_warn "S3 upload skipped (S3_BUCKET not set or aws CLI not available)"
    fi

    # Verify backup
    verify_backup "$BACKUP_PATH"

    log_info "Full backup completed: $BACKUP_PATH"
}

# Incremental backup (hourly)
backup_incremental() {
    log_info "Starting incremental backup..."

    DATE=$(date +%Y%m%d)
    TIME=$(date +%H%M)
    BACKUP_PATH="$BACKUP_DIR/incremental/$DATE/$TIME"
    mkdir -p "$BACKUP_PATH"

    log_info "Creating incremental database backup..."
    # WAL archive for PostgreSQL
    if command -v pg_basebackup &> /dev/null; then
        pg_basebackup -h "$DB_HOST" -U "$DB_USER" -D "$BACKUP_PATH" -Ft -z -P || {
            log_error "Incremental backup failed"
            return 1
        }
        log_info "Incremental backup completed: $BACKUP_PATH"
    else
        log_warn "pg_basebackup not found, skipping incremental backup"
        return 1
    fi

    # Upload to S3 if configured
    if [ -n "$S3_BUCKET" ] && command -v aws &> /dev/null; then
        log_info "Uploading to S3: s3://$S3_BUCKET/backups/incremental/$DATE/$TIME/"
        aws s3 cp "$BACKUP_PATH" "s3://$S3_BUCKET/backups/incremental/$DATE/$TIME/" --recursive || {
            log_error "Failed to upload to S3"
            return 1
        }
        log_info "S3 upload completed"
    else
        log_warn "S3 upload skipped"
    fi

    log_info "Incremental backup completed: $BACKUP_PATH"
}

# Cleanup old backups
cleanup_backups() {
    log_info "Cleaning up old backups (retention: $RETENTION_DAYS days)..."

    # Cleanup full backups
    if [ -d "$BACKUP_DIR/full" ]; then
        DELETED_FULL=$(find "$BACKUP_DIR/full" -type d -mtime +$RETENTION_DAYS -print -exec rm -rf {} \; | wc -l)
        log_info "Deleted $DELETED_FULL old full backup(s)"
    fi

    # Cleanup incremental backups (keep last 7 days)
    if [ -d "$BACKUP_DIR/incremental" ]; then
        DELETED_INC=$(find "$BACKUP_DIR/incremental" -type d -mtime +7 -print -exec rm -rf {} \; | wc -l)
        log_info "Deleted $DELETED_INC old incremental backup(s)"
    fi

    log_info "Cleanup completed"
}

# Verify backup
verify_backup() {
    local BACKUP_PATH=$1

    log_info "Verifying backup: $BACKUP_PATH"

    if [ ! -d "$BACKUP_PATH" ]; then
        log_error "Backup path does not exist: $BACKUP_PATH"
        return 1
    fi

    # Check database backup
    if [ -f "$BACKUP_PATH/db.sql.gz" ]; then
        if gzip -t "$BACKUP_PATH/db.sql.gz" 2>/dev/null; then
            log_info "Database backup verification: OK"
        else
            log_error "Database backup is corrupted"
            return 1
        fi
    else
        log_warn "Database backup file not found"
    fi

    # Check application data backup
    if [ -f "$BACKUP_PATH/app-data.tar.gz" ]; then
        if tar -tzf "$BACKUP_PATH/app-data.tar.gz" > /dev/null 2>&1; then
            log_info "Application data backup verification: OK"
        else
            log_error "Application data backup is corrupted"
            return 1
        fi
    else
        log_warn "Application data backup file not found"
    fi

    log_info "Backup verification completed: OK"
    return 0
}

# List backups
list_backups() {
    log_info "Listing available backups..."

    echo ""
    echo "Full backups:"
    if [ -d "$BACKUP_DIR/full" ]; then
        ls -lh "$BACKUP_DIR/full" 2>/dev/null || echo "  No full backups found"
    else
        echo "  No full backups directory"
    fi

    echo ""
    echo "Incremental backups:"
    if [ -d "$BACKUP_DIR/incremental" ]; then
        find "$BACKUP_DIR/incremental" -type d -maxdepth 2 -mindepth 2 | sort || echo "  No incremental backups found"
    else
        echo "  No incremental backups directory"
    fi
}

# Main
main() {
    case "${1:-}" in
        full)
            backup_full
            ;;
        incremental)
            backup_incremental
            ;;
        cleanup)
            cleanup_backups
            ;;
        verify)
            if [ -z "${2:-}" ]; then
                log_error "Backup path required for verify"
                echo "Usage: $0 verify <backup-path>"
                exit 1
            fi
            verify_backup "$2"
            ;;
        list)
            list_backups
            ;;
        *)
            echo "Usage: $0 {full|incremental|cleanup|verify|list}"
            echo ""
            echo "Commands:"
            echo "  full         - Create full backup"
            echo "  incremental  - Create incremental backup"
            echo "  cleanup      - Cleanup old backups"
            echo "  verify <path> - Verify backup integrity"
            echo "  list         - List available backups"
            echo ""
            echo "Environment variables:"
            echo "  BACKUP_DIR      - Backup directory (default: /backup)"
            echo "  RETENTION_DAYS  - Days to retain backups (default: 30)"
            echo "  S3_BUCKET       - S3 bucket for uploads (optional)"
            echo "  DB_HOST         - Database host (default: localhost)"
            echo "  DB_USER         - Database user (default: backup_user)"
            echo "  DB_NAME         - Database name (default: mydb)"
            echo "  APP_DATA_DIR    - Application data directory (default: /var/app/data)"
            exit 1
            ;;
    esac
}

main "$@"
