#!/usr/bin/env python3
"""
Network Policy Manager

Manage Kubernetes network policies programmatically.

Usage:
    # List policies
    python network_policy_manager.py list --namespace production
    
    # Create policy
    python network_policy_manager.py create --namespace production --policy policy.json
    
    # Apply default deny-all
    python network_policy_manager.py apply-default --namespace production
    
    # Validate policy
    python network_policy_manager.py validate --policy policy.json
"""

import argparse
import json
import sys
from typing import Dict, List, Optional

try:
    import kubernetes
    from kubernetes.client.rest import ApiException
except ImportError:
    print("❌ Error: kubernetes not installed. Install with: pip install kubernetes")
    sys.exit(1)


class NetworkPolicyManager:
    """Manage Kubernetes network policies."""
    
    def __init__(self, kubeconfig: Optional[str] = None):
        """
        Initialize network policy manager.
        
        Args:
            kubeconfig: Path to kubeconfig file (optional)
        """
        if kubeconfig:
            kubernetes.config.load_kube_config(config_file=kubeconfig)
        else:
            try:
                kubernetes.config.load_incluster_config()
            except:
                kubernetes.config.load_kube_config()
        
        self.networking_v1 = kubernetes.client.NetworkingV1Api()

    def create_policy(self, namespace: str, policy: Dict) -> Dict:
        """
        Create network policy.
        
        Args:
            namespace: Namespace name
            policy: Network policy specification
            
        Returns:
            Created policy information
        """
        try:
            body = kubernetes.client.V1NetworkPolicy(**policy)
            created = self.networking_v1.create_namespaced_network_policy(
                namespace, body
            )
            return {
                'status': 'success',
                'policy': created.metadata.name,
                'namespace': namespace,
            }
        except ApiException as e:
            return {
                'status': 'error',
                'error': f'Kubernetes API error: {e}',
            }

    def list_policies(self, namespace: str) -> List[Dict]:
        """
        List all network policies in namespace.
        
        Args:
            namespace: Namespace name
            
        Returns:
            List of network policies
        """
        try:
            policies = self.networking_v1.list_namespaced_network_policy(namespace)
            return [
                {
                    'name': p.metadata.name,
                    'namespace': p.metadata.namespace,
                    'created': p.metadata.creation_timestamp.isoformat() if p.metadata.creation_timestamp else None,
                }
                for p in policies.items
            ]
        except ApiException as e:
            print(f"❌ Error listing policies: {e}", file=sys.stderr)
            return []

    def validate_policy(self, policy: Dict) -> Dict:
        """
        Validate network policy configuration.
        
        Args:
            policy: Network policy specification
            
        Returns:
            Validation results
        """
        errors = []
        warnings = []
        
        spec = policy.get('spec', {})
        
        # Check for required fields
        if 'metadata' not in policy:
            errors.append('Missing metadata')
        elif 'name' not in policy['metadata']:
            errors.append('Missing metadata.name')
        
        if 'spec' not in policy:
            errors.append('Missing spec')
        else:
            if 'podSelector' not in spec:
                errors.append('Missing spec.podSelector')
            
            # Check policy types
            policy_types = spec.get('policyTypes', [])
            if not policy_types:
                warnings.append('No policyTypes specified (defaults to Ingress)')
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings,
        }

    def apply_default_policies(self, namespace: str) -> Dict:
        """
        Apply default deny-all policy to namespace.
        
        Args:
            namespace: Namespace name
            
        Returns:
            Result of applying default policy
        """
        default_policy = {
            'apiVersion': 'networking.k8s.io/v1',
            'kind': 'NetworkPolicy',
            'metadata': {
                'name': 'default-deny-all',
                'namespace': namespace,
            },
            'spec': {
                'podSelector': {},
                'policyTypes': ['Ingress', 'Egress'],
            },
        }
        
        return self.create_policy(namespace, default_policy)


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Network Policy Manager - Manage Kubernetes network policies",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "--kubeconfig",
        help="Path to kubeconfig file"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List network policies")
    list_parser.add_argument("--namespace", required=True, help="Namespace")
    
    # Create command
    create_parser = subparsers.add_parser("create", help="Create network policy")
    create_parser.add_argument("--namespace", required=True, help="Namespace")
    create_parser.add_argument("--policy", required=True, help="Path to policy JSON file")
    
    # Apply default command
    default_parser = subparsers.add_parser("apply-default", help="Apply default deny-all policy")
    default_parser.add_argument("--namespace", required=True, help="Namespace")
    
    # Validate command
    validate_parser = subparsers.add_parser("validate", help="Validate network policy")
    validate_parser.add_argument("--policy", required=True, help="Path to policy JSON file")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        manager = NetworkPolicyManager(kubeconfig=args.kubeconfig)
        
        if args.command == "list":
            policies = manager.list_policies(args.namespace)
            
            if not policies:
                print(f"No network policies found in namespace {args.namespace}")
            else:
                print(f"\n📋 Network Policies in {args.namespace} ({len(policies)}):\n")
                for policy in policies:
                    print(f"  - {policy['name']}")
                    if policy['created']:
                        print(f"    Created: {policy['created']}")
                    print()
                    
        elif args.command == "create":
            with open(args.policy, 'r') as f:
                policy = json.load(f)
            
            result = manager.create_policy(args.namespace, policy)
            
            if result['status'] == 'success':
                print(f"✅ Network policy '{result['policy']}' created in {args.namespace}")
            else:
                print(f"❌ Error: {result.get('error')}")
                return 1
                
        elif args.command == "apply-default":
            result = manager.apply_default_policies(args.namespace)
            
            if result['status'] == 'success':
                print(f"✅ Default deny-all policy applied to {args.namespace}")
            else:
                print(f"❌ Error: {result.get('error')}")
                return 1
                
        elif args.command == "validate":
            with open(args.policy, 'r') as f:
                policy = json.load(f)
            
            result = manager.validate_policy(policy)
            
            if result['valid']:
                print("✅ Network policy is valid")
                if result['warnings']:
                    print("\n⚠️  Warnings:")
                    for warning in result['warnings']:
                        print(f"  - {warning}")
            else:
                print("❌ Network policy has errors:")
                for error in result['errors']:
                    print(f"  - {error}")
                return 1
        
        return 0
        
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())

