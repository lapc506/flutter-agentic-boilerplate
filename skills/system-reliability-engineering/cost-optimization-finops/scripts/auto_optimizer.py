#!/usr/bin/env python3
"""
Automated Cost Optimizer

Automatically analyze and recommend cost optimizations:
- Idle instances
- Unused resources
- Rightsizing opportunities
- Reserved instance opportunities

Usage:
    # Run full optimization analysis
    python auto_optimizer.py analyze
    
    # Generate optimization report
    python auto_optimizer.py report --output report.json
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List

# Import resource optimizer
sys.path.insert(0, str(Path(__file__).parent))
from resource_optimizer import ResourceOptimizer


class AutoCostOptimizer:
    """
    Automated cost optimization analyzer.
    
    Combines multiple optimization strategies:
    - Idle instance detection
    - Rightsizing analysis
    - Unused resource detection
    - Cost savings estimation
    """
    
    def __init__(self, profile: str = None, region: str = None):
        """
        Initialize Auto Cost Optimizer.
        
        Args:
            profile: AWS profile name (optional)
            region: AWS region (optional)
        """
        self.optimizer = ResourceOptimizer(profile=profile, region=region)
        self.recommendations = []

    def analyze(self) -> Dict:
        """
        Run full optimization analysis.
        
        Returns:
            Dictionary with all optimization opportunities
        """
        print("🔍 Starting automated cost optimization analysis...\n")
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'idle_instances': [],
            'rightsizing_opportunities': [],
            'unused_volumes': [],
            'total_potential_savings': 0.0,
        }
        
        # 1. Find idle instances
        print("1️⃣  Analyzing idle instances...")
        idle_instances = self.optimizer.find_idle_instances(cpu_threshold=10.0)
        results['idle_instances'] = idle_instances
        print(f"   Found {len(idle_instances)} idle instance(s)")
        
        # 2. Find rightsizing opportunities
        print("\n2️⃣  Analyzing rightsizing opportunities...")
        rightsizing = self.optimizer.find_rightsizing_opportunities()
        results['rightsizing_opportunities'] = rightsizing
        print(f"   Found {len(rightsizing)} rightsizing opportunity(ies)")
        
        # 3. Find unused volumes
        print("\n3️⃣  Analyzing unused volumes...")
        unused_volumes = self.optimizer.find_unused_volumes()
        results['unused_volumes'] = unused_volumes
        print(f"   Found {len(unused_volumes)} unused volume(s)")
        
        # Calculate total potential savings
        idle_savings = sum(inst['potential_savings'] for inst in idle_instances)
        rightsizing_savings = sum(opp['potential_savings'] for opp in rightsizing if opp['potential_savings'] > 0)
        volume_savings = sum(vol['estimated_monthly_cost'] for vol in unused_volumes)
        
        results['total_potential_savings'] = idle_savings + rightsizing_savings + volume_savings
        
        print(f"\n💰 Total Potential Monthly Savings: ${results['total_potential_savings']:.2f}")
        
        return results

    def generate_recommendations(self, results: Dict) -> List[Dict]:
        """
        Generate actionable recommendations from analysis results.
        
        Args:
            results: Analysis results from analyze()
            
        Returns:
            List of recommendations
        """
        recommendations = []
        
        # Idle instance recommendations
        for instance in results['idle_instances']:
            if instance['avg_cpu'] < 5:
                recommendations.append({
                    'type': 'stop_instance',
                    'priority': 'high',
                    'resource_id': instance['instance_id'],
                    'action': f"Stop instance {instance['instance_id']} (CPU: {instance['avg_cpu']:.1f}%)",
                    'potential_savings': instance['potential_savings'],
                    'reason': 'Very low CPU utilization (< 5%)'
                })
            else:
                recommendations.append({
                    'type': 'downsize_instance',
                    'priority': 'medium',
                    'resource_id': instance['instance_id'],
                    'action': f"Downsize instance {instance['instance_id']} (CPU: {instance['avg_cpu']:.1f}%)",
                    'potential_savings': instance['potential_savings'],
                    'reason': 'Low CPU utilization (< 10%)'
                })
        
        # Rightsizing recommendations
        for opp in results['rightsizing_opportunities']:
            if opp['recommendation'] == 'downsize' and opp['potential_savings'] > 0:
                recommendations.append({
                    'type': 'rightsize_instance',
                    'priority': 'medium',
                    'resource_id': opp['instance_id'],
                    'action': f"Downsize {opp['instance_id']} from {opp['instance_type']}",
                    'potential_savings': opp['potential_savings'],
                    'reason': f"Low CPU utilization ({opp['avg_cpu']:.1f}%)"
                })
        
        # Unused volume recommendations
        for volume in results['unused_volumes']:
            recommendations.append({
                'type': 'delete_volume',
                'priority': 'high',
                'resource_id': volume['volume_id'],
                'action': f"Delete unused volume {volume['volume_id']} ({volume['size_gb']} GB)",
                'potential_savings': volume['estimated_monthly_cost'],
                'reason': 'Volume not attached to any instance'
            })
        
        # Sort by potential savings (descending)
        recommendations.sort(key=lambda x: x['potential_savings'], reverse=True)
        
        return recommendations

    def print_report(self, results: Dict, recommendations: List[Dict]):
        """Print formatted optimization report."""
        print("\n" + "="*70)
        print("📊 COST OPTIMIZATION REPORT")
        print("="*70)
        
        print(f"\n📅 Analysis Date: {results['timestamp']}")
        
        # Summary
        print(f"\n📈 Summary:")
        print(f"  Idle Instances: {len(results['idle_instances'])}")
        print(f"  Rightsizing Opportunities: {len(results['rightsizing_opportunities'])}")
        print(f"  Unused Volumes: {len(results['unused_volumes'])}")
        print(f"  Total Potential Savings: ${results['total_potential_savings']:.2f}/month")
        
        # Recommendations
        if recommendations:
            print(f"\n💡 Top Recommendations:")
            for i, rec in enumerate(recommendations[:10], 1):
                priority_emoji = "🔴" if rec['priority'] == 'high' else "🟡"
                print(f"\n  {i}. {priority_emoji} {rec['action']}")
                print(f"     Savings: ${rec['potential_savings']:.2f}/month")
                print(f"     Reason: {rec['reason']}")
        
        print("\n" + "="*70)


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Automated Cost Optimizer - Analyze and recommend cost optimizations",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "--profile",
        help="AWS profile name"
    )
    
    parser.add_argument(
        "--region",
        help="AWS region"
    )
    
    parser.add_argument(
        "--output",
        help="Output JSON file path"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Analyze command
    subparsers.add_parser("analyze", help="Run full optimization analysis")
    
    # Report command
    report_parser = subparsers.add_parser("report", help="Generate optimization report")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        optimizer = AutoCostOptimizer(profile=args.profile, region=args.region)
        
        if args.command in ["analyze", "report"]:
            results = optimizer.analyze()
            recommendations = optimizer.generate_recommendations(results)
            
            if args.command == "report":
                optimizer.print_report(results, recommendations)
            
            # Save to file if specified
            if args.output:
                output_data = {
                    'analysis': results,
                    'recommendations': recommendations
                }
                with open(args.output, 'w') as f:
                    json.dump(output_data, f, indent=2)
                print(f"\n✅ Report saved to {args.output}")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())

