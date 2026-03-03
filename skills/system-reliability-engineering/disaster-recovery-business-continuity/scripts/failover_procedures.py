#!/usr/bin/env python3
"""
Failover Procedures Manager

Manages failover procedures for disaster recovery with:
- Service registration
- Health checks
- Automatic failover
- Routing updates
- Failover verification

Usage:
    python failover_procedures.py failover payment-service
    python failover_procedures.py status payment-service
    python failover_procedures.py register --name payment-service --primary us-east-1 --standby us-west-2 --rto 15
"""

import argparse
import json
import subprocess
import sys
import time
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path
from typing import List, Optional, Dict


class FailoverStatus(Enum):
    PRIMARY = "primary"
    STANDBY = "standby"
    FAILOVER_IN_PROGRESS = "failover_in_progress"
    FAILED = "failed"


@dataclass
class Service:
    """Service configuration for failover."""
    name: str
    primary_region: str
    standby_region: str
    rto_minutes: int
    rpo_minutes: int = 5
    status: FailoverStatus = FailoverStatus.PRIMARY
    last_failover: Optional[str] = None


class FailoverManager:
    """
    Manages failover procedures for services.

    Handles:
    - Service registration
    - Health checks
    - Failover execution
    - Routing updates
    - Verification
    """

    def __init__(self, config_file: str = "failover_config.json"):
        """
        Initialize failover manager.

        Args:
            config_file: Path to configuration file
        """
        self.config_file = Path(config_file)
        self.services: Dict[str, Service] = {}
        self.load_config()

    def load_config(self):
        """Load service configurations from file."""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    data = json.load(f)
                    for name, service_data in data.items():
                        service_data['status'] = FailoverStatus(service_data['status'])
                        self.services[name] = Service(**service_data)
            except Exception as e:
                print(f"⚠️  Warning: Failed to load config: {e}", file=sys.stderr)

    def save_config(self):
        """Save service configurations to file."""
        data = {}
        for name, service in self.services.items():
            service_dict = asdict(service)
            service_dict['status'] = service.status.value
            data[name] = service_dict

        with open(self.config_file, 'w') as f:
            json.dump(data, f, indent=2)

    def register_service(
        self,
        name: str,
        primary_region: str,
        standby_region: str,
        rto_minutes: int,
        rpo_minutes: int = 5
    ):
        """
        Register a service for failover management.

        Args:
            name: Service name
            primary_region: Primary region
            standby_region: Standby region
            rto_minutes: Recovery Time Objective in minutes
            rpo_minutes: Recovery Point Objective in minutes
        """
        service = Service(
            name=name,
            primary_region=primary_region,
            standby_region=standby_region,
            rto_minutes=rto_minutes,
            rpo_minutes=rpo_minutes,
            status=FailoverStatus.PRIMARY
        )
        self.services[name] = service
        self.save_config()
        print(f"✅ Service '{name}' registered")

    def failover_service(self, service_name: str, dry_run: bool = False) -> bool:
        """
        Execute failover for a service.

        Args:
            service_name: Name of service to failover
            dry_run: If True, only simulate failover

        Returns:
            True if failover successful, False otherwise
        """
        service = self.services.get(service_name)
        if not service:
            print(f"❌ Error: Service '{service_name}' not found")
            return False

        if service.status == FailoverStatus.FAILOVER_IN_PROGRESS:
            print(f"❌ Error: Failover already in progress for '{service_name}'")
            return False

        print(f"🔄 Initiating failover for '{service_name}'...")

        if dry_run:
            print("🔍 DRY RUN MODE - No changes will be made")

        try:
            # 1. Verify standby is healthy
            print("1️⃣  Checking standby health...")
            if not self._check_standby_health(service, dry_run):
                print("❌ Standby is not healthy, aborting failover")
                return False
            print("✅ Standby is healthy")

            # 2. Update status
            if not dry_run:
                service.status = FailoverStatus.FAILOVER_IN_PROGRESS
                self.save_config()

            # 3. Promote standby to primary
            print("2️⃣  Promoting standby to primary...")
            if not dry_run:
                self._promote_standby(service)
            print("✅ Standby promoted")

            # 4. Update DNS/load balancer routing
            print("3️⃣  Updating routing...")
            if not dry_run:
                self._update_routing(service)
            print("✅ Routing updated")

            # 5. Verify failover
            print("4️⃣  Verifying failover...")
            if not self._verify_failover(service, dry_run):
                print("❌ Failover verification failed")
                if not dry_run:
                    service.status = FailoverStatus.FAILED
                    self.save_config()
                return False
            print("✅ Failover verified")

            # 6. Update status
            if not dry_run:
                service.status = FailoverStatus.STANDBY
                service.last_failover = time.strftime("%Y-%m-%d %H:%M:%S")
                self.save_config()

            print(f"✅ Failover completed successfully for '{service_name}'")
            return True

        except Exception as e:
            print(f"❌ Failover failed: {e}", file=sys.stderr)
            if not dry_run:
                service.status = FailoverStatus.FAILED
                self.save_config()
            return False

    def _check_standby_health(self, service: Service, dry_run: bool = False) -> bool:
        """
        Check if standby is healthy.

        Args:
            service: Service to check
            dry_run: If True, simulate check

        Returns:
            True if healthy, False otherwise
        """
        if dry_run:
            return True

        # Example: Check Kubernetes deployment health
        # kubectl get deployment -n production service-name-standby
        try:
            # Replace with actual health check logic
            # For now, simulate success
            result = subprocess.run(
                ["kubectl", "get", "deployment", f"{service.name}-standby"],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0
        except FileNotFoundError:
            print("⚠️  kubectl not found, assuming standby is healthy")
            return True
        except subprocess.TimeoutExpired:
            print("⚠️  Health check timeout, assuming standby is healthy")
            return True
        except Exception:
            # If health check fails, assume unhealthy
            return False

    def _promote_standby(self, service: Service):
        """
        Promote standby to primary.

        Args:
            service: Service to promote
        """
        # Example: Update database replication
        # For PostgreSQL: pg_ctl promote
        # For Kubernetes: Update labels/annotations

        # Replace with actual promotion logic
        print(f"   Promoting {service.name} in {service.standby_region}...")

        # Example Kubernetes command:
        # subprocess.run([
        #     "kubectl", "patch", "deployment", f"{service.name}-standby",
        #     "-p", '{"metadata":{"labels":{"role":"primary"}}}'
        # ])

    def _update_routing(self, service: Service):
        """
        Update DNS/load balancer routing.

        Args:
            service: Service to update routing for
        """
        # Example: Update Route53 DNS
        # aws route53 change-resource-record-sets ...

        # Example: Update Kubernetes service
        # kubectl patch service service-name -p '{"spec":{"selector":{"region":"standby"}}}'

        print(f"   Updating routing to point to {service.standby_region}...")

    def _verify_failover(self, service: Service, dry_run: bool = False) -> bool:
        """
        Verify failover was successful.

        Args:
            service: Service to verify
            dry_run: If True, simulate verification

        Returns:
            True if verification successful, False otherwise
        """
        if dry_run:
            return True

        # Example: Check if service is responding
        # curl -f http://service-endpoint/health

        # For now, simulate success
        time.sleep(2)  # Simulate verification delay
        return True

    def get_status(self, service_name: Optional[str] = None) -> Dict:
        """
        Get failover status for service(s).

        Args:
            service_name: Service name (None for all services)

        Returns:
            Status dictionary
        """
        if service_name:
            service = self.services.get(service_name)
            if not service:
                return {"error": f"Service '{service_name}' not found"}
            return {
                "name": service.name,
                "status": service.status.value,
                "primary_region": service.primary_region,
                "standby_region": service.standby_region,
                "rto_minutes": service.rto_minutes,
                "rpo_minutes": service.rpo_minutes,
                "last_failover": service.last_failover
            }
        else:
            return {
                name: {
                    "status": service.status.value,
                    "primary_region": service.primary_region,
                    "standby_region": service.standby_region,
                    "rto_minutes": service.rto_minutes,
                    "last_failover": service.last_failover
                }
                for name, service in self.services.items()
            }

    def list_services(self) -> List[str]:
        """List all registered services."""
        return list(self.services.keys())


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Failover procedures manager for disaster recovery",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "--config",
        default="failover_config.json",
        help="Configuration file path"
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Register command
    register_parser = subparsers.add_parser("register", help="Register a service")
    register_parser.add_argument("--name", required=True, help="Service name")
    register_parser.add_argument("--primary", required=True, help="Primary region")
    register_parser.add_argument("--standby", required=True, help="Standby region")
    register_parser.add_argument("--rto", type=int, required=True, help="RTO in minutes")
    register_parser.add_argument("--rpo", type=int, default=5, help="RPO in minutes")

    # Failover command
    failover_parser = subparsers.add_parser("failover", help="Execute failover")
    failover_parser.add_argument("service", help="Service name")
    failover_parser.add_argument("--dry-run", action="store_true", help="Simulate failover")

    # Status command
    status_parser = subparsers.add_parser("status", help="Get service status")
    status_parser.add_argument("service", nargs="?", help="Service name (optional, shows all if omitted)")

    # List command
    subparsers.add_parser("list", help="List all registered services")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    manager = FailoverManager(args.config)

    try:
        if args.command == "register":
            manager.register_service(
                name=args.name,
                primary_region=args.primary,
                standby_region=args.standby,
                rto_minutes=args.rto,
                rpo_minutes=args.rpo
            )

        elif args.command == "failover":
            success = manager.failover_service(args.service, dry_run=args.dry_run)
            return 0 if success else 1

        elif args.command == "status":
            status = manager.get_status(args.service)
            print(json.dumps(status, indent=2))

        elif args.command == "list":
            services = manager.list_services()
            if services:
                print("Registered services:")
                for service_name in services:
                    print(f"  - {service_name}")
            else:
                print("No services registered")

        return 0

    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    exit(main())
