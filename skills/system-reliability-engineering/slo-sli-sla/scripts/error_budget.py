#!/usr/bin/env python3
"""
Error Budget Calculator for SLO Management

This script calculates error budgets based on SLO targets and tracks
error budget consumption for services.

Usage:
    python error_budget.py --slo-target 0.9995 --total-requests 1000000 --error-requests 400
    python error_budget.py --slo-target 0.9995 --window-days 30 --interactive
"""

import argparse
from datetime import datetime, timedelta
from typing import Dict, Optional


class ErrorBudget:
    """
    Calculate and manage error budgets for Service Level Objectives (SLOs).

    Error budget represents the allowed percentage of errors within a time window.
    For example, a 99.95% availability SLO means 0.05% error budget.
    """

    def __init__(
        self,
        slo_target: float,
        window_days: int = 30,
        total_requests: Optional[int] = None
    ):
        """
        Initialize ErrorBudget calculator.

        Args:
            slo_target: SLO target as decimal (e.g., 0.9995 for 99.95%)
            window_days: Evaluation window in days (default: 30)
            total_requests: Total number of requests (optional)
        """
        self.slo_target = slo_target  # e.g., 0.9995 for 99.95%
        self.window_days = window_days
        self.total_requests = total_requests
        self.window_seconds = window_days * 24 * 60 * 60

    def calculate_error_budget(self) -> float:
        """
        Calculate error budget as percentage of allowed errors.

        Example: 99.95% SLO means 0.05% error budget

        Returns:
            Error budget as decimal (e.g., 0.0005 for 0.05%)
        """
        return 1.0 - self.slo_target

    def calculate_error_budget_requests(self, total_requests: int) -> int:
        """
        Calculate number of requests allowed to fail.

        Args:
            total_requests: Total number of requests in the window

        Returns:
            Number of requests allowed to fail
        """
        error_budget_pct = self.calculate_error_budget()
        return int(total_requests * error_budget_pct)

    def calculate_remaining_budget(
        self,
        total_requests: int,
        error_requests: int
    ) -> Dict:
        """
        Calculate remaining error budget.

        Args:
            total_requests: Total number of requests
            error_requests: Number of failed requests

        Returns:
            Dictionary with budget status including:
            - total_budget: Total error budget in requests
            - consumed: Consumed budget in requests
            - remaining: Remaining budget in requests
            - remaining_percentage: Remaining budget as percentage
            - consumed_percentage: Consumed budget as percentage
            - status: Budget status (healthy/caution/at_risk/exhausted)
        """
        total_budget = self.calculate_error_budget_requests(total_requests)
        consumed = error_requests
        remaining = total_budget - consumed
        remaining_pct = (remaining / total_budget * 100) if total_budget > 0 else 0
        consumed_pct = (consumed / total_budget * 100) if total_budget > 0 else 0

        return {
            "total_budget": total_budget,
            "consumed": consumed,
            "remaining": remaining,
            "remaining_percentage": remaining_pct,
            "consumed_percentage": consumed_pct,
            "status": self._get_budget_status(consumed_pct)
        }

    def _get_budget_status(self, consumed_pct: float) -> str:
        """
        Get budget status based on consumption percentage.

        Args:
            consumed_pct: Percentage of budget consumed

        Returns:
            Status string: exhausted, at_risk, caution, or healthy
        """
        if consumed_pct >= 100:
            return "exhausted"
        elif consumed_pct >= 75:
            return "at_risk"
        elif consumed_pct >= 50:
            return "caution"
        else:
            return "healthy"

    def format_status(self, status_dict: Dict) -> str:
        """
        Format status dictionary as human-readable string.

        Args:
            status_dict: Status dictionary from calculate_remaining_budget

        Returns:
            Formatted status string
        """
        status_emoji = {
            "healthy": "✅",
            "caution": "⚠️",
            "at_risk": "🔶",
            "exhausted": "🔴"
        }

        emoji = status_emoji.get(status_dict["status"], "❓")

        return f"""
{emoji} Error Budget Status: {status_dict['status'].upper()}

SLO Target: {self.slo_target * 100:.3f}%
Window: {self.window_days} days

Budget:
  Total: {status_dict['total_budget']:,} requests
  Consumed: {status_dict['consumed']:,} requests ({status_dict['consumed_percentage']:.2f}%)
  Remaining: {status_dict['remaining']:,} requests ({status_dict['remaining_percentage']:.2f}%)
"""


def main():
    """CLI entry point for error budget calculator."""
    parser = argparse.ArgumentParser(
        description="Calculate error budgets for SLO management",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Calculate budget for 1M requests with 400 errors
  python error_budget.py --slo-target 0.9995 --total-requests 1000000 --error-requests 400

  # Interactive mode
  python error_budget.py --slo-target 0.9995 --interactive

  # Custom window
  python error_budget.py --slo-target 0.9999 --window-days 7 --total-requests 500000 --error-requests 10
        """
    )

    parser.add_argument(
        "--slo-target",
        type=float,
        required=True,
        help="SLO target as decimal (e.g., 0.9995 for 99.95%%)"
    )

    parser.add_argument(
        "--window-days",
        type=int,
        default=30,
        help="Evaluation window in days (default: 30)"
    )

    parser.add_argument(
        "--total-requests",
        type=int,
        help="Total number of requests"
    )

    parser.add_argument(
        "--error-requests",
        type=int,
        help="Number of failed requests"
    )

    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Interactive mode to input values"
    )

    args = parser.parse_args()

    # Validate SLO target
    if not 0 < args.slo_target <= 1:
        print("❌ Error: SLO target must be between 0 and 1 (e.g., 0.9995 for 99.95%%)")
        return 1

    # Interactive mode
    if args.interactive:
        try:
            if not args.total_requests:
                args.total_requests = int(input("Enter total requests: "))
            if not args.error_requests:
                args.error_requests = int(input("Enter error requests: "))
        except (ValueError, KeyboardInterrupt):
            print("\n❌ Invalid input or cancelled")
            return 1

    # Validate required arguments
    if not args.total_requests or not args.error_requests:
        print("❌ Error: --total-requests and --error-requests are required (or use --interactive)")
        return 1

    # Calculate error budget
    error_budget = ErrorBudget(
        slo_target=args.slo_target,
        window_days=args.window_days,
        total_requests=args.total_requests
    )

    status = error_budget.calculate_remaining_budget(
        args.total_requests,
        args.error_requests
    )

    # Print formatted output
    print(error_budget.format_status(status))

    return 0


if __name__ == "__main__":
    exit(main())
