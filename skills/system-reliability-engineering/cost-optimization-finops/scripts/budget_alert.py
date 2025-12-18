#!/usr/bin/env python3
"""
Budget Alert Manager

Create and manage AWS budgets with automated alerts.

Usage:
    # Create budget
    python budget_alert.py create \
      --name monthly-budget \
      --amount 10000 \
      --period monthly \
      --thresholds 50,80,100 \
      --email ops@example.com
    
    # List budgets
    python budget_alert.py list
    
    # Get budget status
    python budget_alert.py status --name monthly-budget
"""

import argparse
import json
import sys
from dataclasses import dataclass
from typing import List, Optional

try:
    import boto3
    from botocore.exceptions import ClientError, BotoCoreError
except ImportError:
    print("❌ Error: boto3 not installed. Install with: pip install boto3")
    sys.exit(1)


@dataclass
class Budget:
    """Budget configuration."""
    name: str
    amount: float
    period: str  # DAILY, MONTHLY, QUARTERLY, ANNUALLY
    thresholds: List[float]
    email: str
    filters: Optional[dict] = None


class BudgetAlert:
    """
    Manage AWS budgets with automated alerts.
    
    Handles:
    - Creating budgets
    - Setting up alert thresholds
    - Managing notifications
    """
    
    def __init__(self, profile: Optional[str] = None):
        """
        Initialize Budget Alert Manager.
        
        Args:
            profile: AWS profile name (optional)
        """
        session = boto3.Session(profile_name=profile) if profile else boto3.Session()
        self.budgets_client = session.client('budgets')
        self.account_id = self._get_account_id()

    def _get_account_id(self) -> str:
        """Get AWS account ID."""
        try:
            sts = boto3.client('sts')
            return sts.get_caller_identity()['Account']
        except Exception as e:
            print(f"⚠️  Warning: Could not get account ID: {e}")
            return "unknown"

    def create_budget(self, budget: Budget):
        """
        Create AWS budget with alerts.
        
        Args:
            budget: Budget configuration
        """
        try:
            # Build budget definition
            budget_def = {
                'BudgetName': budget.name,
                'BudgetLimit': {
                    'Amount': str(budget.amount),
                    'Unit': 'USD',
                },
                'TimeUnit': budget.period.upper(),
                'BudgetType': 'COST',
            }
            
            # Add filters if specified
            if budget.filters:
                budget_def['CostFilters'] = budget.filters
            
            # Build notifications
            notifications = []
            for threshold in budget.thresholds:
                notifications.append({
                    'Notification': {
                        'NotificationType': 'ACTUAL',
                        'ComparisonOperator': 'GREATER_THAN',
                        'Threshold': threshold,
                        'ThresholdType': 'PERCENTAGE',
                    },
                    'Subscribers': [
                        {
                            'SubscriptionType': 'EMAIL',
                            'Address': budget.email,
                        },
                    ],
                })
            
            # Create budget
            self.budgets_client.create_budget(
                AccountId=self.account_id,
                Budget=budget_def,
                NotificationsWithSubscribers=notifications,
            )
            
            print(f"✅ Budget '{budget.name}' created successfully")
            print(f"   Amount: ${budget.amount:,.2f} {budget.period}")
            print(f"   Alerts at: {', '.join(f'{t}%' for t in budget.thresholds)}")
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'DuplicateRecordException':
                print(f"❌ Budget '{budget.name}' already exists")
            else:
                print(f"❌ AWS API Error: {e}", file=sys.stderr)
            raise
        except Exception as e:
            print(f"❌ Error creating budget: {e}", file=sys.stderr)
            raise

    def list_budgets(self) -> List[dict]:
        """
        List all budgets.
        
        Returns:
            List of budget information
        """
        try:
            response = self.budgets_client.describe_budgets(AccountId=self.account_id)
            return response.get('Budgets', [])
        except ClientError as e:
            print(f"❌ AWS API Error: {e}", file=sys.stderr)
            raise

    def get_budget_status(self, budget_name: str) -> dict:
        """
        Get budget status and current spending.
        
        Args:
            budget_name: Name of budget
            
        Returns:
            Budget status information
        """
        try:
            # Get budget
            budgets = self.list_budgets()
            budget = next((b for b in budgets if b['BudgetName'] == budget_name), None)
            
            if not budget:
                raise ValueError(f"Budget '{budget_name}' not found")
            
            # Get calculated spending
            response = self.budgets_client.describe_budget_performance_history(
                AccountId=self.account_id,
                BudgetName=budget_name,
            )
            
            return {
                'budget': budget,
                'performance': response.get('BudgetPerformanceHistory', {})
            }
            
        except ClientError as e:
            print(f"❌ AWS API Error: {e}", file=sys.stderr)
            raise

    def delete_budget(self, budget_name: str):
        """
        Delete a budget.
        
        Args:
            budget_name: Name of budget to delete
        """
        try:
            self.budgets_client.delete_budget(
                AccountId=self.account_id,
                BudgetName=budget_name,
            )
            print(f"✅ Budget '{budget_name}' deleted successfully")
        except ClientError as e:
            print(f"❌ AWS API Error: {e}", file=sys.stderr)
            raise


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="AWS Budget Alert Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "--profile",
        help="AWS profile name"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Create command
    create_parser = subparsers.add_parser("create", help="Create a budget")
    create_parser.add_argument("--name", required=True, help="Budget name")
    create_parser.add_argument("--amount", type=float, required=True, help="Budget amount")
    create_parser.add_argument(
        "--period",
        choices=["daily", "monthly", "quarterly", "annually"],
        default="monthly",
        help="Budget period"
    )
    create_parser.add_argument(
        "--thresholds",
        required=True,
        help="Alert thresholds as comma-separated percentages (e.g., 50,80,100)"
    )
    create_parser.add_argument("--email", required=True, help="Email for alerts")
    create_parser.add_argument("--filters", help="Budget filters as JSON (optional)")
    
    # List command
    subparsers.add_parser("list", help="List all budgets")
    
    # Status command
    status_parser = subparsers.add_parser("status", help="Get budget status")
    status_parser.add_argument("--name", required=True, help="Budget name")
    
    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a budget")
    delete_parser.add_argument("--name", required=True, help="Budget name")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        manager = BudgetAlert(profile=args.profile)
        
        if args.command == "create":
            thresholds = [float(t.strip()) for t in args.thresholds.split(',')]
            filters = json.loads(args.filters) if args.filters else None
            
            budget = Budget(
                name=args.name,
                amount=args.amount,
                period=args.period,
                thresholds=thresholds,
                email=args.email,
                filters=filters
            )
            
            manager.create_budget(budget)
            
        elif args.command == "list":
            budgets = manager.list_budgets()
            
            if not budgets:
                print("No budgets found")
                return 0
            
            print(f"\n📊 Found {len(budgets)} budget(s):\n")
            for budget in budgets:
                limit = budget.get('BudgetLimit', {})
                print(f"  {budget['BudgetName']}")
                print(f"    Amount: ${float(limit.get('Amount', 0)):,.2f} {budget.get('TimeUnit', 'N/A')}")
                print(f"    Type: {budget.get('BudgetType', 'N/A')}")
                print()
                
        elif args.command == "status":
            status = manager.get_budget_status(args.name)
            budget = status['budget']
            
            print(f"\n📊 Budget Status: {budget['BudgetName']}\n")
            limit = budget.get('BudgetLimit', {})
            print(f"  Amount: ${float(limit.get('Amount', 0)):,.2f} {budget.get('TimeUnit', 'N/A')}")
            print(f"  Type: {budget.get('BudgetType', 'N/A')}")
            # Add more status information as needed
            
        elif args.command == "delete":
            confirm = input(f"Are you sure you want to delete budget '{args.name}'? (yes/no): ")
            if confirm.lower() == 'yes':
                manager.delete_budget(args.name)
            else:
                print("Cancelled")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    exit(main())

