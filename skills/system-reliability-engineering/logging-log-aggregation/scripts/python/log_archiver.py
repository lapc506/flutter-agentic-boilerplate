#!/usr/bin/env python3
"""
Log Archiver

Archive and manage log retention with S3 storage.

Usage:
    # Archive logs older than retention period
    python log_archiver.py archive --log-dir /var/log/app --retention-days 30
    
    # Restore archived logs
    python log_archiver.py restore --date 2024-01-15 --s3-prefix logs
"""

import argparse
import gzip
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

try:
    import boto3
    from botocore.exceptions import ClientError
except ImportError:
    print("❌ Error: boto3 not installed. Install with: pip install boto3")
    sys.exit(1)


class LogArchiver:
    """Archive and manage log files with S3 storage."""
    
    def __init__(self, s3_bucket: str, retention_days: int = 30):
        """
        Initialize log archiver.
        
        Args:
            s3_bucket: S3 bucket name for archived logs
            retention_days: Number of days to retain logs locally
        """
        self.s3_bucket = s3_bucket
        self.retention_days = retention_days
        self.s3_client = boto3.client('s3')

    def archive_logs(self, log_directory: str, dry_run: bool = False):
        """
        Archive logs older than retention period.
        
        Args:
            log_directory: Directory containing log files
            dry_run: If True, don't actually archive, just show what would be archived
        """
        log_path = Path(log_directory)
        if not log_path.exists():
            print(f"❌ Error: Directory {log_directory} does not exist")
            return
        
        cutoff_date = datetime.now() - timedelta(days=self.retention_days)
        cutoff_timestamp = cutoff_date.timestamp()
        
        archived_count = 0
        total_size = 0
        
        print(f"📦 Archiving logs older than {self.retention_days} days (before {cutoff_date.date()})...")
        
        for log_file in log_path.glob('*.log'):
            file_mtime = log_file.stat().st_mtime
            
            if file_mtime < cutoff_timestamp:
                file_size = log_file.stat().st_size
                total_size += file_size
                
                if dry_run:
                    print(f"  [DRY RUN] Would archive: {log_file.name} ({file_size / 1024:.2f} KB)")
                else:
                    try:
                        self._compress_and_upload(log_file)
                        archived_count += 1
                        print(f"  ✅ Archived: {log_file.name}")
                    except Exception as e:
                        print(f"  ❌ Error archiving {log_file.name}: {e}")
        
        if not dry_run:
            print(f"\n✅ Archived {archived_count} log file(s) ({total_size / 1024 / 1024:.2f} MB)")
        else:
            print(f"\n[DRY RUN] Would archive {archived_count} log file(s) ({total_size / 1024 / 1024:.2f} MB)")

    def _compress_and_upload(self, log_file: Path):
        """Compress log file and upload to S3."""
        # Compress
        compressed_file = log_file.with_suffix('.log.gz')
        
        try:
            with open(log_file, 'rb') as f_in:
                with gzip.open(compressed_file, 'wb') as f_out:
                    f_out.writelines(f_in)
            
            # Upload to S3
            date_str = datetime.fromtimestamp(log_file.stat().st_mtime).strftime('%Y-%m-%d')
            s3_key = f"logs/{date_str}/{log_file.name}.gz"
            
            self.s3_client.upload_file(
                str(compressed_file),
                self.s3_bucket,
                s3_key
            )
            
            # Delete local files
            log_file.unlink()
            compressed_file.unlink()
            
        except Exception as e:
            # Clean up compressed file if upload failed
            if compressed_file.exists():
                compressed_file.unlink()
            raise

    def restore_logs(self, date: datetime, s3_prefix: str = 'logs', output_dir: str = '/tmp/restored'):
        """
        Restore archived logs from S3.
        
        Args:
            date: Date to restore logs from
            s3_prefix: S3 prefix for logs
            output_dir: Local directory to restore logs to
        """
        date_prefix = date.strftime('%Y-%m-%d')
        s3_path = f"{s3_prefix}/{date_prefix}/"
        
        print(f"📥 Restoring logs from {date_prefix}...")
        
        try:
            objects = self.s3_client.list_objects_v2(
                Bucket=self.s3_bucket,
                Prefix=s3_path
            )
            
            if 'Contents' not in objects:
                print(f"❌ No logs found for date {date_prefix}")
                return
            
            restored_count = 0
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            
            for obj in objects['Contents']:
                s3_key = obj['Key']
                filename = Path(s3_key).name.replace('.gz', '')
                local_file = output_path / filename
                
                # Download
                print(f"  Downloading {filename}...")
                self.s3_client.download_file(
                    self.s3_bucket,
                    s3_key,
                    str(local_file.with_suffix('.log.gz'))
                )
                
                # Decompress
                with gzip.open(local_file.with_suffix('.log.gz'), 'rb') as f_in:
                    with open(local_file, 'wb') as f_out:
                        f_out.write(f_in.read())
                
                # Remove compressed file
                local_file.with_suffix('.log.gz').unlink()
                restored_count += 1
                print(f"  ✅ Restored: {filename}")
            
            print(f"\n✅ Restored {restored_count} log file(s) to {output_dir}")
            
        except ClientError as e:
            print(f"❌ S3 Error: {e}")
            raise


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Log Archiver - Archive and manage log retention",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "--s3-bucket",
        required=True,
        help="S3 bucket name for archived logs"
    )
    
    parser.add_argument(
        "--retention-days",
        type=int,
        default=30,
        help="Number of days to retain logs locally (default: 30)"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Archive command
    archive_parser = subparsers.add_parser("archive", help="Archive old logs")
    archive_parser.add_argument("--log-dir", required=True, help="Directory containing log files")
    archive_parser.add_argument("--dry-run", action="store_true", help="Show what would be archived without actually archiving")
    
    # Restore command
    restore_parser = subparsers.add_parser("restore", help="Restore archived logs")
    restore_parser.add_argument("--date", required=True, help="Date to restore (YYYY-MM-DD)")
    restore_parser.add_argument("--s3-prefix", default="logs", help="S3 prefix for logs (default: logs)")
    restore_parser.add_argument("--output-dir", default="/tmp/restored", help="Output directory (default: /tmp/restored)")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        archiver = LogArchiver(
            s3_bucket=args.s3_bucket,
            retention_days=args.retention_days
        )
        
        if args.command == "archive":
            archiver.archive_logs(args.log_dir, dry_run=args.dry_run)
        elif args.command == "restore":
            restore_date = datetime.strptime(args.date, '%Y-%m-%d')
            archiver.restore_logs(restore_date, args.s3_prefix, args.output_dir)
        
        return 0
        
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())

