#!/usr/bin/env python3
"""
Capacity Planning Calculator

Calculate capacity requirements and resource planning based on metrics.

Usage:
    python capacity_calculator.py --current-users 1000 --peak-users 1500
    python capacity_calculator.py --target-users 5000 --calculate-resources
"""

import argparse
import sys
from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class CapacityMetrics:
    """Capacity metrics for planning."""
    current_users: int
    peak_users: int
    avg_request_per_user_per_sec: float
    avg_response_time_ms: float
    error_rate: float
    current_throughput_rps: float
    max_throughput_rps: float


class CapacityPlanner:
    """Capacity planning calculator."""
    
    def __init__(self, metrics: CapacityMetrics, current_instances: int = 3):
        """
        Initialize capacity planner.
        
        Args:
            metrics: Capacity metrics
            current_instances: Current number of instances
        """
        self.metrics = metrics
        self.current_instances = current_instances

    def calculate_capacity_headroom(self) -> float:
        """Calculate current capacity headroom (0.0 to 1.0)."""
        if self.metrics.max_throughput_rps == 0:
            return 0.0
        utilization = self.metrics.current_throughput_rps / self.metrics.max_throughput_rps
        return max(0.0, 1.0 - utilization)

    def estimate_max_users(self, target_error_rate: float = 0.01) -> int:
        """
        Estimate maximum users with acceptable error rate.
        
        Args:
            target_error_rate: Maximum acceptable error rate
            
        Returns:
            Estimated maximum users
        """
        if self.metrics.current_throughput_rps == 0:
            return 0
        
        # Simple estimation: assume linear scaling until error rate threshold
        users_at_max = int(
            self.metrics.peak_users * 
            (self.metrics.max_throughput_rps / self.metrics.current_throughput_rps)
        )
        return users_at_max

    def calculate_resources_needed(
        self,
        target_users: int,
        target_error_rate: float = 0.01
    ) -> Dict:
        """
        Calculate resources needed for target user count.
        
        Args:
            target_users: Target number of users
            target_error_rate: Maximum acceptable error rate
            
        Returns:
            Dictionary with resource requirements
        """
        if self.metrics.max_throughput_rps == 0:
            return {
                "error": "max_throughput_rps cannot be zero"
            }
        
        current_users_per_instance = (
            self.metrics.peak_users / self.current_instances
            if self.current_instances > 0 else 0
        )
        
        required_rps = target_users * self.metrics.avg_request_per_user_per_sec
        required_instances = int(
            required_rps / self.metrics.max_throughput_rps
        ) + 1  # Add buffer
        
        scaling_factor = (
            required_instances / self.current_instances
            if self.current_instances > 0 else float('inf')
        )
        
        return {
            "target_users": target_users,
            "required_instances": required_instances,
            "required_rps": required_rps,
            "current_instances": self.current_instances,
            "scaling_factor": scaling_factor,
            "current_users_per_instance": current_users_per_instance,
            "target_users_per_instance": target_users / required_instances if required_instances > 0 else 0,
        }

    def generate_report(self) -> str:
        """Generate capacity planning report."""
        headroom = self.calculate_capacity_headroom()
        max_users = self.estimate_max_users()
        
        report = []
        report.append("=" * 60)
        report.append("CAPACITY PLANNING REPORT")
        report.append("=" * 60)
        report.append("")
        report.append(f"Current Users: {self.metrics.current_users}")
        report.append(f"Peak Users: {self.metrics.peak_users}")
        report.append(f"Current Throughput: {self.metrics.current_throughput_rps:.2f} req/s")
        report.append(f"Max Throughput: {self.metrics.max_throughput_rps:.2f} req/s")
        report.append(f"Capacity Headroom: {headroom * 100:.1f}%")
        report.append(f"Estimated Max Users: {max_users}")
        report.append(f"Current Instances: {self.current_instances}")
        report.append("")
        
        return "\n".join(report)


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Capacity Planning Calculator",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument("--current-users", type=int, default=1000, help="Current number of users")
    parser.add_argument("--peak-users", type=int, default=1500, help="Peak number of users")
    parser.add_argument("--avg-rps-per-user", type=float, default=0.5, help="Average requests per user per second")
    parser.add_argument("--avg-response-time", type=float, default=100.0, help="Average response time (ms)")
    parser.add_argument("--error-rate", type=float, default=0.01, help="Current error rate")
    parser.add_argument("--current-throughput", type=float, default=500.0, help="Current throughput (req/s)")
    parser.add_argument("--max-throughput", type=float, default=1000.0, help="Max throughput per instance (req/s)")
    parser.add_argument("--current-instances", type=int, default=3, help="Current number of instances")
    
    parser.add_argument("--target-users", type=int, help="Calculate resources for target users")
    parser.add_argument("--report", action="store_true", help="Generate capacity report")
    
    args = parser.parse_args()
    
    metrics = CapacityMetrics(
        current_users=args.current_users,
        peak_users=args.peak_users,
        avg_request_per_user_per_sec=args.avg_rps_per_user,
        avg_response_time_ms=args.avg_response_time,
        error_rate=args.error_rate,
        current_throughput_rps=args.current_throughput,
        max_throughput_rps=args.max_throughput,
    )
    
    planner = CapacityPlanner(metrics, current_instances=args.current_instances)
    
    if args.report:
        print(planner.generate_report())
    
    if args.target_users:
        resources = planner.calculate_resources_needed(args.target_users)
        print("\nResource Requirements:")
        print("=" * 60)
        for key, value in resources.items():
            if isinstance(value, float):
                print(f"  {key}: {value:.2f}")
            else:
                print(f"  {key}: {value}")
    
    if not args.report and not args.target_users:
        # Default: show report
        print(planner.generate_report())
    
    return 0


if __name__ == "__main__":
    exit(main())

