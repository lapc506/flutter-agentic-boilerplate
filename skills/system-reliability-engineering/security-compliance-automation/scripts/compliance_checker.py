#!/usr/bin/env python3
"""
Compliance Checker

Check AWS resources against CIS benchmarks and compliance rules.

Usage:
    # Check CIS benchmark
    python compliance_checker.py check-cis
    
    # Check specific rule
    python compliance_checker.py check-rule --rule-name access-keys-rotated
    
    # Generate report
    python compliance_checker.py report --output compliance-report.txt
"""

import argparse
import sys
from typing import Dict, List, Optional

try:
    import boto3
    from botocore.exceptions import ClientError, BotoCoreError
except ImportError:
    print("❌ Error: boto3 not installed. Install with: pip install boto3")
    sys.exit(1)


class ComplianceChecker:
    """Check AWS resources against compliance rules."""
    
    def __init__(self, profile: Optional[str] = None, region: str = 'us-east-1'):
        """
        Initialize compliance checker.
        
        Args:
            profile: AWS profile name (optional)
            region: AWS region (default: us-east-1)
        """
        session = boto3.Session(profile_name=profile) if profile else boto3.Session()
        self.config_client = session.client('config', region_name=region)
        self.region = region

    def check_cis_benchmark(self) -> Dict:
        """
        Check AWS resources against CIS benchmark.
        
        Returns:
            Dictionary with compliance results for each rule
        """
        rules = [
            'access-keys-rotated',
            'iam-password-policy',
            'root-access-key-check',
            's3-bucket-public-read-prohibited',
            's3-bucket-public-write-prohibited',
            'ec2-instance-managed-by-systems-manager',
            'encrypted-volumes',
        ]
        
        results = {}
        print(f"🔍 Checking {len(rules)} CIS benchmark rules...\n")
        
        for rule in rules:
            compliance = self._check_rule_compliance(rule)
            results[rule] = compliance
            
            status_emoji = "✅" if compliance['compliance_type'] == 'COMPLIANT' else "❌"
            print(f"  {status_emoji} {rule}: {compliance['compliance_type']}")
        
        return results

    def _check_rule_compliance(self, rule_name: str) -> Dict:
        """
        Check compliance for a specific rule.
        
        Args:
            rule_name: Name of the compliance rule
            
        Returns:
            Dictionary with compliance information
        """
        try:
            response = self.config_client.describe_compliance_by_config_rule(
                ConfigRuleNames=[rule_name]
            )
            
            if response.get('ComplianceByConfigRules'):
                compliance = response['ComplianceByConfigRules'][0]
                return {
                    'rule_name': rule_name,
                    'compliance_type': compliance.get('ComplianceType', 'UNKNOWN'),
                    'compliance_summary': compliance.get('ComplianceSummary', {}),
                }
            
            return {
                'rule_name': rule_name,
                'compliance_type': 'NOT_APPLICABLE',
                'error': 'Rule not found or not configured'
            }
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'NoSuchConfigRuleException':
                return {
                    'rule_name': rule_name,
                    'compliance_type': 'NOT_CONFIGURED',
                    'error': 'Config rule not found. Enable AWS Config first.'
                }
            else:
                return {
                    'rule_name': rule_name,
                    'compliance_type': 'ERROR',
                    'error': str(e)
                }

    def generate_compliance_report(self, results: Optional[Dict] = None) -> str:
        """
        Generate compliance report.
        
        Args:
            results: Compliance results (if None, will check CIS benchmark)
            
        Returns:
            Formatted compliance report string
        """
        if results is None:
            results = self.check_cis_benchmark()
        
        report = []
        report.append("=" * 60)
        report.append("AWS COMPLIANCE REPORT")
        report.append("=" * 60)
        report.append(f"Region: {self.region}")
        report.append(f"Generated: {__import__('datetime').datetime.now().isoformat()}")
        report.append("")
        
        compliant_count = 0
        non_compliant_count = 0
        not_applicable_count = 0
        
        for rule, compliance in results.items():
            status = compliance.get('compliance_type', 'UNKNOWN')
            
            if status == 'COMPLIANT':
                compliant_count += 1
                report.append(f"✅ {rule}: COMPLIANT")
            elif status in ['NON_COMPLIANT', 'ERROR']:
                non_compliant_count += 1
                report.append(f"❌ {rule}: {status}")
                if 'error' in compliance:
                    report.append(f"   Error: {compliance['error']}")
            else:
                not_applicable_count += 1
                report.append(f"⚠️  {rule}: {status}")
        
        report.append("")
        report.append("=" * 60)
        report.append("SUMMARY")
        report.append("=" * 60)
        report.append(f"Compliant: {compliant_count}")
        report.append(f"Non-Compliant: {non_compliant_count}")
        report.append(f"Not Applicable: {not_applicable_count}")
        report.append(f"Total: {len(results)}")
        
        compliance_percentage = (
            (compliant_count / len(results) * 100) if results else 0
        )
        report.append(f"Compliance: {compliance_percentage:.1f}%")
        
        return "\n".join(report)


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Compliance Checker - Check AWS resources against compliance rules",
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
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Check CIS command
    subparsers.add_parser("check-cis", help="Check CIS benchmark compliance")
    
    # Check rule command
    rule_parser = subparsers.add_parser("check-rule", help="Check specific rule compliance")
    rule_parser.add_argument("--rule-name", required=True, help="Rule name to check")
    
    # Report command
    report_parser = subparsers.add_parser("report", help="Generate compliance report")
    report_parser.add_argument("--output", help="Output file path")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        checker = ComplianceChecker(profile=args.profile, region=args.region)
        
        if args.command == "check-cis":
            results = checker.check_cis_benchmark()
            print("\n" + checker.generate_compliance_report(results))
            
        elif args.command == "check-rule":
            compliance = checker._check_rule_compliance(args.rule_name)
            print(f"\nRule: {args.rule_name}")
            print(f"Status: {compliance['compliance_type']}")
            if 'error' in compliance:
                print(f"Error: {compliance['error']}")
                
        elif args.command == "report":
            results = checker.check_cis_benchmark()
            report = checker.generate_compliance_report(results)
            
            if args.output:
                with open(args.output, 'w') as f:
                    f.write(report)
                print(f"✅ Report saved to {args.output}")
            else:
                print("\n" + report)
        
        return 0
        
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())

