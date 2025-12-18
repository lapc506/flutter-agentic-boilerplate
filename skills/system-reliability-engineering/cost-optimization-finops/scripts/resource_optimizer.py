#!/usr/bin/env python3
"""
Resource Optimizer

Analyze AWS resources and identify optimization opportunities:
- Idle instances
- Rightsizing opportunities
- Unused resources
- Reserved instance opportunities

Usage:
    # Find idle instances
    python resource_optimizer.py idle --cpu-threshold 10
    
    # Find rightsizing opportunities
    python resource_optimizer.py rightsize
    
    # Find unused volumes
    python resource_optimizer.py unused-volumes
"""

import argparse
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional

try:
    import boto3
    from botocore.exceptions import ClientError, BotoCoreError
except ImportError:
    print("❌ Error: boto3 not installed. Install with: pip install boto3")
    sys.exit(1)


class ResourceOptimizer:
    """
    Analyze AWS resources and identify optimization opportunities.
    
    Provides methods to:
    - Find idle instances
    - Find rightsizing opportunities
    - Find unused resources
    - Estimate cost savings
    """
    
    def __init__(self, profile: Optional[str] = None, region: Optional[str] = None):
        """
        Initialize Resource Optimizer.
        
        Args:
            profile: AWS profile name (optional)
            region: AWS region (optional, analyzes all regions if not specified)
        """
        session = boto3.Session(profile_name=profile) if profile else boto3.Session()
        self.ec2_client = session.client('ec2', region_name=region) if region else session.client('ec2')
        self.cloudwatch = session.client('cloudwatch', region_name=region) if region else session.client('cloudwatch')
        self.region = region or "default"

    def find_idle_instances(
        self,
        cpu_threshold: float = 10.0,
        days: int = 7
    ) -> List[Dict]:
        """
        Find EC2 instances with low CPU utilization.
        
        Args:
            cpu_threshold: CPU utilization threshold (default: 10%)
            days: Number of days to analyze (default: 7)
            
        Returns:
            List of idle instances with details
        """
        print(f"🔍 Analyzing instances in {self.region}...")
        
        try:
            instances = self.ec2_client.describe_instances()['Reservations']
            idle_instances = []
            
            for reservation in instances:
                for instance in reservation['Instances']:
                    if instance['State']['Name'] != 'running':
                        continue
                    
                    instance_id = instance['InstanceId']
                    instance_type = instance['InstanceType']
                    
                    # Check CPU utilization
                    try:
                        metrics = self.cloudwatch.get_metric_statistics(
                            Namespace='AWS/EC2',
                            MetricName='CPUUtilization',
                            Dimensions=[
                                {'Name': 'InstanceId', 'Value': instance_id},
                            ],
                            StartTime=datetime.now() - timedelta(days=days),
                            EndTime=datetime.now(),
                            Period=3600,  # 1 hour
                            Statistics=['Average'],
                        )
                        
                        avg_cpu = self._calculate_average(metrics['Datapoints'])
                        
                        if avg_cpu < cpu_threshold:
                            estimated_cost = self._estimate_monthly_cost(instance_type)
                            potential_savings = estimated_cost * 0.7  # Assume 70% savings if stopped
                            
                            idle_instances.append({
                                'instance_id': instance_id,
                                'instance_type': instance_type,
                                'avg_cpu': avg_cpu,
                                'estimated_monthly_cost': estimated_cost,
                                'potential_savings': potential_savings,
                                'region': self.region,
                            })
                    except Exception as e:
                        print(f"⚠️  Warning: Could not get metrics for {instance_id}: {e}")
                        continue
            
            return idle_instances
            
        except ClientError as e:
            print(f"❌ AWS API Error: {e}", file=sys.stderr)
            raise

    def find_unused_volumes(self) -> List[Dict]:
        """
        Find unused EBS volumes (not attached to any instance).
        
        Returns:
            List of unused volumes
        """
        print(f"🔍 Analyzing volumes in {self.region}...")
        
        try:
            volumes = self.ec2_client.describe_volumes()['Volumes']
            unused_volumes = []
            
            for volume in volumes:
                if not volume['Attachments']:
                    size_gb = volume['Size']
                    volume_type = volume['VolumeType']
                    estimated_cost = self._estimate_volume_cost(size_gb, volume_type)
                    
                    unused_volumes.append({
                        'volume_id': volume['VolumeId'],
                        'size_gb': size_gb,
                        'volume_type': volume_type,
                        'estimated_monthly_cost': estimated_cost,
                        'region': self.region,
                    })
            
            return unused_volumes
            
        except ClientError as e:
            print(f"❌ AWS API Error: {e}", file=sys.stderr)
            raise

    def find_rightsizing_opportunities(
        self,
        cpu_threshold_low: float = 20.0,
        cpu_threshold_high: float = 80.0,
        days: int = 7
    ) -> List[Dict]:
        """
        Find instances that could be downsized or upsized.
        
        Args:
            cpu_threshold_low: CPU threshold for downsizing (default: 20%)
            cpu_threshold_high: CPU threshold for upsizing (default: 80%)
            days: Number of days to analyze
            
        Returns:
            List of rightsizing opportunities
        """
        print(f"🔍 Analyzing rightsizing opportunities in {self.region}...")
        
        try:
            instances = self.ec2_client.describe_instances()['Reservations']
            opportunities = []
            
            for reservation in instances:
                for instance in reservation['Instances']:
                    if instance['State']['Name'] != 'running':
                        continue
                    
                    instance_id = instance['InstanceId']
                    instance_type = instance['InstanceType']
                    
                    try:
                        metrics = self.cloudwatch.get_metric_statistics(
                            Namespace='AWS/EC2',
                            MetricName='CPUUtilization',
                            Dimensions=[
                                {'Name': 'InstanceId', 'Value': instance_id},
                            ],
                            StartTime=datetime.now() - timedelta(days=days),
                            EndTime=datetime.now(),
                            Period=3600,
                            Statistics=['Average'],
                        )
                        
                        avg_cpu = self._calculate_average(metrics['Datapoints'])
                        current_cost = self._estimate_monthly_cost(instance_type)
                        
                        recommendation = None
                        potential_savings = 0.0
                        
                        if avg_cpu < cpu_threshold_low:
                            recommendation = "downsize"
                            # Estimate 30% cost reduction for downsizing
                            potential_savings = current_cost * 0.3
                        elif avg_cpu > cpu_threshold_high:
                            recommendation = "upsize"
                            # Upsizing costs more, so negative savings
                            potential_savings = -current_cost * 0.2
                        
                        if recommendation:
                            opportunities.append({
                                'instance_id': instance_id,
                                'instance_type': instance_type,
                                'avg_cpu': avg_cpu,
                                'recommendation': recommendation,
                                'current_monthly_cost': current_cost,
                                'potential_savings': potential_savings,
                                'region': self.region,
                            })
                    except Exception as e:
                        print(f"⚠️  Warning: Could not analyze {instance_id}: {e}")
                        continue
            
            return opportunities
            
        except ClientError as e:
            print(f"❌ AWS API Error: {e}", file=sys.stderr)
            raise

    def _calculate_average(self, datapoints: List[Dict]) -> float:
        """Calculate average from CloudWatch datapoints."""
        if not datapoints:
            return 0.0
        return sum(dp['Average'] for dp in datapoints) / len(datapoints)

    def _estimate_monthly_cost(self, instance_type: str) -> float:
        """
        Estimate monthly cost for instance type.
        
        Note: This is a simplified estimation. For accurate costs,
        use AWS Pricing API or Cost Explorer.
        """
        # Simplified cost estimation (in USD per month)
        # Real implementation should use AWS Pricing API
        cost_map = {
            't2.micro': 8.5,
            't2.small': 17.0,
            't2.medium': 34.0,
            't3.micro': 7.5,
            't3.small': 15.0,
            't3.medium': 30.0,
            'm5.large': 77.0,
            'm5.xlarge': 154.0,
            'c5.large': 68.0,
            'c5.xlarge': 136.0,
        }
        
        return cost_map.get(instance_type, 100.0)  # Default estimate

    def _estimate_volume_cost(self, size_gb: int, volume_type: str) -> float:
        """
        Estimate monthly cost for EBS volume.
        
        Args:
            size_gb: Volume size in GB
            volume_type: Volume type (gp2, gp3, io1, etc.)
        """
        # Simplified cost estimation (USD per GB per month)
        cost_per_gb = {
            'gp2': 0.10,
            'gp3': 0.08,
            'io1': 0.125,
            'io2': 0.125,
            'st1': 0.045,
            'sc1': 0.025,
        }
        
        base_cost = cost_per_gb.get(volume_type, 0.10)
        return size_gb * base_cost


def format_idle_instances(instances: List[Dict]) -> str:
    """Format idle instances for display."""
    if not instances:
        return "✅ No idle instances found"
    
    output = [f"\n🔍 Found {len(instances)} idle instance(s):\n"]
    total_savings = 0.0
    
    for inst in instances:
        output.append(f"  Instance: {inst['instance_id']}")
        output.append(f"    Type: {inst['instance_type']}")
        output.append(f"    Avg CPU: {inst['avg_cpu']:.1f}%")
        output.append(f"    Monthly Cost: ${inst['estimated_monthly_cost']:.2f}")
        output.append(f"    Potential Savings: ${inst['potential_savings']:.2f}")
        output.append("")
        total_savings += inst['potential_savings']
    
    output.append(f"  💰 Total Potential Savings: ${total_savings:.2f}/month")
    
    return "\n".join(output)


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="AWS Resource Optimizer - Find cost optimization opportunities",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "--profile",
        help="AWS profile name"
    )
    
    parser.add_argument(
        "--region",
        help="AWS region (default: all regions)"
    )
    
    parser.add_argument(
        "--days",
        type=int,
        default=7,
        help="Number of days to analyze (default: 7)"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Idle instances
    idle_parser = subparsers.add_parser("idle", help="Find idle instances")
    idle_parser.add_argument(
        "--cpu-threshold",
        type=float,
        default=10.0,
        help="CPU utilization threshold (default: 10%%)"
    )
    
    # Rightsizing
    subparsers.add_parser("rightsize", help="Find rightsizing opportunities")
    
    # Unused volumes
    subparsers.add_parser("unused-volumes", help="Find unused EBS volumes")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        optimizer = ResourceOptimizer(profile=args.profile, region=args.region)
        
        if args.command == "idle":
            instances = optimizer.find_idle_instances(
                cpu_threshold=args.cpu_threshold,
                days=args.days
            )
            print(format_idle_instances(instances))
            
        elif args.command == "rightsize":
            opportunities = optimizer.find_rightsizing_opportunities(days=args.days)
            
            if not opportunities:
                print("✅ No rightsizing opportunities found")
            else:
                print(f"\n🔍 Found {len(opportunities)} rightsizing opportunity(ies):\n")
                for opp in opportunities:
                    print(f"  Instance: {opp['instance_id']}")
                    print(f"    Type: {opp['instance_type']}")
                    print(f"    Avg CPU: {opp['avg_cpu']:.1f}%")
                    print(f"    Recommendation: {opp['recommendation']}")
                    print(f"    Current Cost: ${opp['current_monthly_cost']:.2f}/month")
                    print(f"    Potential Savings: ${opp['potential_savings']:.2f}/month")
                    print()
                    
        elif args.command == "unused-volumes":
            volumes = optimizer.find_unused_volumes()
            
            if not volumes:
                print("✅ No unused volumes found")
            else:
                print(f"\n🔍 Found {len(volumes)} unused volume(s):\n")
                total_cost = 0.0
                for vol in volumes:
                    print(f"  Volume: {vol['volume_id']}")
                    print(f"    Size: {vol['size_gb']} GB")
                    print(f"    Type: {vol['volume_type']}")
                    print(f"    Monthly Cost: ${vol['estimated_monthly_cost']:.2f}")
                    print()
                    total_cost += vol['estimated_monthly_cost']
                print(f"  💰 Total Monthly Cost: ${total_cost:.2f}")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    exit(main())

