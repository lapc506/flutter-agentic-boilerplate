#!/usr/bin/env python3
"""
PostgreSQL Backup Automation Script

Automates full backups, restoration, and cleanup for PostgreSQL databases.

Usage:
    # Create full backup
    python postgresql_backup.py backup --host localhost --user backup_user --dbname mydb

    # Restore from backup
    python postgresql_backup.py restore --backup-path /backup/full_20240115_120000 --target-dir /var/lib/postgresql/data

    # Cleanup old backups
    python postgresql_backup.py cleanup --backup-dir /backup --retention-days 30
"""

import argparse
import subprocess
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional


class PostgreSQLBackup:
    """
    PostgreSQL backup and restore automation.

    Handles:
    - Full database backups using pg_basebackup
    - Restore from backups
    - Cleanup of old backups based on retention policy
    """

    def __init__(
        self,
        host: str = "localhost",
        port: int = 5432,
        user: str = "postgres",
        dbname: Optional[str] = None,
        backup_dir: str = "/backup/postgresql"
    ):
        """
        Initialize PostgreSQL backup manager.

        Args:
            host: PostgreSQL host
            port: PostgreSQL port
            user: PostgreSQL user for backups
            dbname: Database name (optional, for logical backups)
            backup_dir: Directory to store backups
        """
        self.host = host
        self.port = port
        self.user = user
        self.dbname = dbname
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(parents=True, exist_ok=True)

    def full_backup(self, verify: bool = True) -> str:
        """
        Create full physical backup using pg_basebackup.

        Args:
            verify: Whether to verify backup after creation

        Returns:
            Path to backup directory

        Raises:
            Exception: If backup fails
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self.backup_dir / f"full_{timestamp}"
        backup_path.mkdir(parents=True, exist_ok=True)

        print(f"Creating full backup to {backup_path}...")

        cmd = [
            "pg_basebackup",
            "-h", self.host,
            "-p", str(self.port),
            "-U", self.user,
            "-D", str(backup_path),
            "-Ft",  # Tar format
            "-z",   # Compress
            "-P",    # Progress
            "-v"     # Verbose
        ]

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            print(f"✅ Backup created successfully: {backup_path}")

            if verify:
                self.verify_backup(backup_path)

            return str(backup_path)

        except subprocess.CalledProcessError as e:
            raise Exception(f"Backup failed: {e.stderr}") from e
        except FileNotFoundError:
            raise Exception("pg_basebackup not found. Is PostgreSQL installed?")

    def verify_backup(self, backup_path: str):
        """
        Verify backup integrity using pg_verifybackup.

        Args:
            backup_path: Path to backup directory

        Raises:
            Exception: If verification fails
        """
        print(f"Verifying backup: {backup_path}...")

        try:
            result = subprocess.run(
                ["pg_verifybackup", "-D", backup_path],
                capture_output=True,
                text=True,
                check=True
            )
            print("✅ Backup verification passed")

        except subprocess.CalledProcessError as e:
            raise Exception(f"Backup verification failed: {e.stderr}") from e
        except FileNotFoundError:
            print("⚠️  pg_verifybackup not found, skipping verification")

    def restore(
        self,
        backup_path: str,
        target_dir: str,
        stop_service: bool = True,
        start_service: bool = True
    ):
        """
        Restore database from backup.

        Args:
            backup_path: Path to backup directory
            target_dir: Target PostgreSQL data directory
            stop_service: Whether to stop PostgreSQL service before restore
            start_service: Whether to start PostgreSQL service after restore

        Raises:
            Exception: If restore fails
        """
        backup_path = Path(backup_path)
        target_dir = Path(target_dir)

        if not backup_path.exists():
            raise Exception(f"Backup path does not exist: {backup_path}")

        print(f"Restoring from {backup_path} to {target_dir}...")

        # Stop PostgreSQL
        if stop_service:
            print("Stopping PostgreSQL service...")
            try:
                subprocess.run(
                    ["systemctl", "stop", "postgresql"],
                    check=True,
                    capture_output=True
                )
            except subprocess.CalledProcessError as e:
                raise Exception(f"Failed to stop PostgreSQL: {e.stderr}") from e
            except FileNotFoundError:
                print("⚠️  systemctl not found, assuming manual service management")

        # Remove old data
        if target_dir.exists():
            print(f"Removing old data directory: {target_dir}")
            import shutil
            shutil.rmtree(target_dir)

        target_dir.mkdir(parents=True, exist_ok=True)

        # Extract backup
        base_tar = backup_path / "base.tar.gz"
        if not base_tar.exists():
            raise Exception(f"Backup file not found: {base_tar}")

        print(f"Extracting backup from {base_tar}...")
        try:
            subprocess.run(
                ["tar", "-xzf", str(base_tar), "-C", str(target_dir)],
                check=True,
                capture_output=True
            )
            print("✅ Backup extracted successfully")
        except subprocess.CalledProcessError as e:
            raise Exception(f"Failed to extract backup: {e.stderr}") from e

        # Start PostgreSQL
        if start_service:
            print("Starting PostgreSQL service...")
            try:
                subprocess.run(
                    ["systemctl", "start", "postgresql"],
                    check=True,
                    capture_output=True
                )
                print("✅ PostgreSQL service started")
            except subprocess.CalledProcessError as e:
                raise Exception(f"Failed to start PostgreSQL: {e.stderr}") from e
            except FileNotFoundError:
                print("⚠️  systemctl not found, please start PostgreSQL manually")

    def cleanup_old_backups(self, retention_days: int = 30, dry_run: bool = False):
        """
        Remove backups older than retention period.

        Args:
            retention_days: Number of days to retain backups
            dry_run: If True, only show what would be deleted

        Returns:
            Number of backups removed
        """
        cutoff = datetime.now() - timedelta(days=retention_days)
        removed_count = 0

        print(f"Cleaning up backups older than {retention_days} days (before {cutoff.date()})...")

        for backup in sorted(self.backup_dir.glob("full_*")):
            if backup.is_dir():
                try:
                    # Parse timestamp from directory name
                    timestamp_str = backup.name.replace("full_", "")
                    backup_time = datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")

                    if backup_time < cutoff:
                        if dry_run:
                            print(f"Would remove: {backup} (created {backup_time.date()})")
                        else:
                            import shutil
                            shutil.rmtree(backup)
                            print(f"✅ Removed old backup: {backup} (created {backup_time.date()})")
                            removed_count += 1
                except ValueError:
                    # Skip directories that don't match expected format
                    continue

        if dry_run:
            print(f"Dry run: Would remove {removed_count} backup(s)")
        else:
            print(f"✅ Cleanup complete: Removed {removed_count} backup(s)")

        return removed_count

    def list_backups(self):
        """List all available backups."""
        backups = []

        for backup in sorted(self.backup_dir.glob("full_*")):
            if backup.is_dir():
                try:
                    timestamp_str = backup.name.replace("full_", "")
                    backup_time = datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")
                    size = sum(f.stat().st_size for f in backup.rglob('*') if f.is_file())
                    backups.append({
                        "path": str(backup),
                        "timestamp": backup_time,
                        "size": size
                    })
                except ValueError:
                    continue

        if not backups:
            print("No backups found")
            return

        print(f"\nFound {len(backups)} backup(s):\n")
        for backup in backups:
            size_mb = backup["size"] / (1024 * 1024)
            print(f"  {backup['timestamp'].strftime('%Y-%m-%d %H:%M:%S')} - "
                  f"{size_mb:.1f} MB - {backup['path']}")


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="PostgreSQL backup and restore automation",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Backup command
    backup_parser = subparsers.add_parser("backup", help="Create full backup")
    backup_parser.add_argument("--host", default="localhost", help="PostgreSQL host")
    backup_parser.add_argument("--port", type=int, default=5432, help="PostgreSQL port")
    backup_parser.add_argument("--user", default="postgres", help="PostgreSQL user")
    backup_parser.add_argument("--dbname", help="Database name (optional)")
    backup_parser.add_argument("--backup-dir", default="/backup/postgresql", help="Backup directory")
    backup_parser.add_argument("--no-verify", action="store_true", help="Skip backup verification")

    # Restore command
    restore_parser = subparsers.add_parser("restore", help="Restore from backup")
    restore_parser.add_argument("--backup-path", required=True, help="Path to backup directory")
    restore_parser.add_argument("--target-dir", required=True, help="Target PostgreSQL data directory")
    restore_parser.add_argument("--no-stop", action="store_true", help="Don't stop PostgreSQL service")
    restore_parser.add_argument("--no-start", action="store_true", help="Don't start PostgreSQL service")

    # Cleanup command
    cleanup_parser = subparsers.add_parser("cleanup", help="Cleanup old backups")
    cleanup_parser.add_argument("--backup-dir", default="/backup/postgresql", help="Backup directory")
    cleanup_parser.add_argument("--retention-days", type=int, default=30, help="Days to retain backups")
    cleanup_parser.add_argument("--dry-run", action="store_true", help="Show what would be deleted")

    # List command
    list_parser = subparsers.add_parser("list", help="List available backups")
    list_parser.add_argument("--backup-dir", default="/backup/postgresql", help="Backup directory")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    try:
        if args.command == "backup":
            backup = PostgreSQLBackup(
                host=args.host,
                port=args.port,
                user=args.user,
                dbname=getattr(args, "dbname", None),
                backup_dir=args.backup_dir
            )
            backup.full_backup(verify=not args.no_verify)

        elif args.command == "restore":
            backup = PostgreSQLBackup(backup_dir=os.path.dirname(args.backup_path))
            backup.restore(
                backup_path=args.backup_path,
                target_dir=args.target_dir,
                stop_service=not args.no_stop,
                start_service=not args.no_start
            )

        elif args.command == "cleanup":
            backup = PostgreSQLBackup(backup_dir=args.backup_dir)
            backup.cleanup_old_backups(
                retention_days=args.retention_days,
                dry_run=args.dry_run
            )

        elif args.command == "list":
            backup = PostgreSQLBackup(backup_dir=args.backup_dir)
            backup.list_backups()

        return 0

    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    exit(main())
