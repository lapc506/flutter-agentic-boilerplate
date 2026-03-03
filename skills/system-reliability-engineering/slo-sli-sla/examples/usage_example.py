#!/usr/bin/env python3
"""
Example usage of ErrorBudget class

This demonstrates how to use the ErrorBudget calculator
programmatically in your own code.
"""

import sys
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from error_budget import ErrorBudget


def example_basic_calculation():
    """Basic error budget calculation example."""
    print("=" * 60)
    print("Example 1: Basic Error Budget Calculation")
    print("=" * 60)

    # 99.95% availability SLO
    error_budget = ErrorBudget(slo_target=0.9995, window_days=30)

    # 1M requests in 30 days
    total_requests = 1_000_000
    error_requests = 400  # Actual errors

    status = error_budget.calculate_remaining_budget(total_requests, error_requests)

    print(error_budget.format_status(status))
    print(f"Error budget percentage: {error_budget.calculate_error_budget() * 100:.3f}%")
    print(f"Allowed errors: {error_budget.calculate_error_budget_requests(total_requests):,}")


def example_different_slos():
    """Compare different SLO targets."""
    print("\n" + "=" * 60)
    print("Example 2: Comparing Different SLO Targets")
    print("=" * 60)

    slo_targets = [
        (0.99, "99%"),
        (0.999, "99.9%"),
        (0.9995, "99.95%"),
        (0.9999, "99.99%")
    ]

    total_requests = 1_000_000
    error_requests = 500

    print(f"\nTotal requests: {total_requests:,}")
    print(f"Error requests: {error_requests:,}\n")

    for slo_target, label in slo_targets:
        error_budget = ErrorBudget(slo_target=slo_target, window_days=30)
        status = error_budget.calculate_remaining_budget(total_requests, error_requests)

        print(f"{label:8} SLO: {status['status']:10} | "
              f"Budget: {status['total_budget']:6,} | "
              f"Remaining: {status['remaining']:6,} ({status['remaining_percentage']:5.1f}%)")


def example_budget_statuses():
    """Demonstrate different budget statuses."""
    print("\n" + "=" * 60)
    print("Example 3: Budget Status Thresholds")
    print("=" * 60)

    error_budget = ErrorBudget(slo_target=0.9995, window_days=30)
    total_requests = 1_000_000
    total_budget = error_budget.calculate_error_budget_requests(total_requests)

    # Test different consumption levels
    consumption_levels = [
        (total_budget * 0.25, "25% consumed"),
        (total_budget * 0.50, "50% consumed"),
        (total_budget * 0.75, "75% consumed"),
        (total_budget * 0.99, "99% consumed"),
        (total_budget * 1.00, "100% consumed"),
    ]

    print(f"\nTotal budget: {total_budget:,} requests\n")

    for error_requests, label in consumption_levels:
        status = error_budget.calculate_remaining_budget(total_requests, int(error_requests))
        print(f"{label:15} → Status: {status['status']:10} | "
              f"Remaining: {status['remaining_percentage']:5.1f}%")


def example_window_comparison():
    """Compare different time windows."""
    print("\n" + "=" * 60)
    print("Example 4: Different Time Windows")
    print("=" * 60)

    slo_target = 0.9995
    total_requests_per_day = 100_000
    error_requests_per_day = 50

    windows = [7, 14, 30, 90]

    print(f"\nDaily requests: {total_requests_per_day:,}")
    print(f"Daily errors: {error_requests_per_day:,}\n")

    for window_days in windows:
        total_requests = total_requests_per_day * window_days
        error_requests = error_requests_per_day * window_days

        error_budget = ErrorBudget(slo_target=slo_target, window_days=window_days)
        status = error_budget.calculate_remaining_budget(total_requests, error_requests)

        print(f"{window_days:3} days: {status['status']:10} | "
              f"Remaining: {status['remaining']:8,} ({status['remaining_percentage']:5.1f}%)")


if __name__ == "__main__":
    example_basic_calculation()
    example_different_slos()
    example_budget_statuses()
    example_window_comparison()

    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)
