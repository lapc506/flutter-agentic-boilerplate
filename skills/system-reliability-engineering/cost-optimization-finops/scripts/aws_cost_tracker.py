#!/usr/bin/env python3
"""
AWS Cost Tracker

Track and analyze AWS costs using Cost Explorer API.

Usage:
    # Get daily costs
    python aws_cost_tracker.py daily --days 30
    
    # Get service costs
    python aws_cost_tracker.py service --service EC2 --days 30
    
    # Get costs by tag
    python aws_cost_tracker.py tag --tag-key Environment --days 30
    
    # Export to CSV
    python aws_cost_tracker.py daily --days 30 --output costs.csv
"""

import argparse
import csv
import json
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional

try:
    import boto3
    from botocore.exceptions import ClientError, BotoCoreError
except ImportError:
    print("❌ Error: boto3 not installed. Install with: pip install boto3")
    sys.exit(1)


class AWSCostTracker:
    """
    Track and analyze AWS costs using Cost Explorer API.
    
    Provides methods to:
    - Get daily costs
    - Get costs by service
    - Get costs by tags
    - Export cost data
    """
    
    def __init__(self, profile: Optional[str] = None, region: str = "us-east-1"):
        """
        Initialize AWS Cost Tracker.
        
        Args:
            profile: AWS profile name (optional)
            region: AWS region (default: us-east-1)
        """
        session = boto3.Session(profile_name=profile) if profile else boto3.Session()
        self.ce_client = session.client('ce', region_name=region)
        self.account_id = self._get_account_id()

    def _get_account_id(self) -> str:
        """Get AWS account ID."""
        try:
            sts = boto3.client('sts')
            return sts.get_caller_identity()['Account']
        except Exception as e:
            print(f"⚠️  Warning: Could not get account ID: {e}")
            return "unknown"

    def get_daily_costs(
        self,
        days: int = 30,
        group_by_service: bool = True
    ) -> List[Dict]:
        """
        Get daily costs for last N days.
        
        Args:
            days: Number of days to retrieve
            group_by_service: Group costs by service
            
        Returns:
            List of daily cost data
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        try:
            group_by = []
            if group_by_service:
                group_by.append({'Type': 'DIMENSION', 'Key': 'SERVICE'})

            response = self.ce_client.get_cost_and_usage(
                TimePeriod={
                    'Start': start_date.strftime('%Y-%m-%d'),
                    'End': end_date.strftime('%Y-%m-%d'),
                },
                Granularity='DAILY',
                Metrics=['UnblendedCost'],
                GroupBy=group_by if group_by else None,
            )

            return response.get('ResultsByTime', [])
            
        except ClientError as e:
            print(f"❌ AWS API Error: {e}", file=sys.stderr)
            raise
        except Exception as e:
            print(f"❌ Error getting costs: {e}", file=sys.stderr)
            raise

    def get_service_costs(self, service_name: str, days: int = 30) -> float:
        """
        Get total cost for a specific service.
        
        Args:
            service_name: AWS service name (e.g., 'EC2', 'S3')
            days: Number of days to analyze
            
        Returns:
            Total cost in USD
        """
        costs = self.get_daily_costs(days, group_by_service=True)
        total = 0.0

        for day in costs:
            for group in day.get('Groups', []):
                if service_name in group['Keys']:
                    amount = float(group['Metrics']['UnblendedCost']['Amount'])
                    total += amount

        return total

    def get_cost_by_tag(
        self,
        tag_key: str,
        days: int = 30
    ) -> Dict[str, float]:
        """
        Get costs grouped by tag.
        
        Args:
            tag_key: Tag key to group by (e.g., 'Environment', 'Team')
            days: Number of days to analyze
            
        Returns:
            Dictionary mapping tag values to costs
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        try:
            response = self.ce_client.get_cost_and_usage(
                TimePeriod={
                    'Start': start_date.strftime('%Y-%m-%d'),
                    'End': end_date.strftime('%Y-%m-%d'),
                },
                Granularity='DAILY',
                Metrics=['UnblendedCost'],
                GroupBy=[
                    {'Type': 'TAG', 'Key': tag_key},
                ],
            )

            costs_by_tag = {}
            for day in response.get('ResultsByTime', []):
                for group in day.get('Groups', []):
                    tag_value = group['Keys'][0] if group['Keys'] else 'untagged'
                    amount = float(group['Metrics']['UnblendedCost']['Amount'])
                    costs_by_tag[tag_value] = costs_by_tag.get(tag_value, 0) + amount

            return costs_by_tag
            
        except ClientError as e:
            print(f"❌ AWS API Error: {e}", file=sys.stderr)
            raise

    def export_to_csv(self, data: List[Dict], output_file: str):
        """
        Export cost data to CSV.
        
        Args:
            data: Cost data from get_daily_costs
            output_file: Output CSV file path
        """
        with open(output_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Date', 'Service', 'Cost (USD)'])
            
            for day in data:
                date = day['TimePeriod']['Start']
                for group in day.get('Groups', []):
                    service = group['Keys'][0] if group['Keys'] else 'Total'
                    cost = group['Metrics']['UnblendedCost']['Amount']
                    writer.writerow([date, service, cost])
        
        print(f"✅ Cost data exported to {output_file}")


def format_cost_data(data: List[Dict]) -> str:
    """Format cost data for display."""
    output = []
    total_cost = 0.0
    
    for day in data:
        date = day['TimePeriod']['Start']
        day_total = 0.0
        
        output.append(f"\n📅 {date}")
        for group in day.get('Groups', []):
            service = group['Keys'][0] if group['Keys'] else 'Total'
            cost = float(group['Metrics']['UnblendedCost']['Amount'])
            day_total += cost
            output.append(f"  {service:20} ${cost:>10.2f}")
        
        output.append(f"  {'Total':20} ${day_total:>10.2f}")
        total_cost += day_total
    
    output.append(f"\n{'='*35}")
    output.append(f"{'Total Period':20} ${total_cost:>10.2f}")
    
    return "\n".join(output)


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="AWS Cost Tracker - Track and analyze AWS costs",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "--profile",
        help="AWS profile name"
    )
    
    parser.add_argument(
        "--region",
        default="us-east-1",
        help="AWS region (default: us-east-1)"
    )
    
    parser.add_argument(
        "--days",
        type=int,
        default=30,
        help="Number of days to analyze (default: 30)"
    )
    
    parser.add_argument(
        "--output",
        help="Output CSV file path"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Daily costs
    daily_parser = subparsers.add_parser("daily", help="Get daily costs")
    
    # Service costs
    service_parser = subparsers.add_parser("service", help="Get costs for a service")
    service_parser.add_argument("service", help="Service name (e.g., EC2, S3)")
    
    # Tag costs
    tag_parser = subparsers.add_parser("tag", help="Get costs by tag")
    tag_parser.add_argument("--tag-key", required=True, help="Tag key (e.g., Environment)")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        tracker = AWSCostTracker(profile=args.profile, region=args.region)
        
        if args.command == "daily":
            data = tracker.get_daily_costs(days=args.days, group_by_service=True)
            
            if args.output:
                tracker.export_to_csv(data, args.output)
            else:
                print(format_cost_data(data))
                
        elif args.command == "service":
            cost = tracker.get_service_costs(args.service, days=args.days)
            print(f"\n💰 Total cost for {args.service} (last {args.days} days): ${cost:.2f}")
            
        elif args.command == "tag":
            costs = tracker.get_cost_by_tag(args.tag_key, days=args.days)
            
            print(f"\n💰 Costs by {args.tag_key} (last {args.days} days):\n")
            total = 0.0
            for tag_value, cost in sorted(costs.items(), key=lambda x: x[1], reverse=True):
                print(f"  {tag_value:20} ${cost:>10.2f}")
                total += cost
            print(f"\n  {'Total':20} ${total:>10.2f}")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    exit(main())

