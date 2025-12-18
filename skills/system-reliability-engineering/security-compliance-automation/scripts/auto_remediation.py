#!/usr/bin/env python3
"""
Automated Remediation

Automatically remediate security and compliance issues in Kubernetes.

Usage:
    # Remediate non-compliant resources
    python auto_remediation.py remediate --namespace production
    
    # Dry run (show what would be remediated)
    python auto_remediation.py remediate --namespace production --dry-run
    
    # Remediate specific resource
    python auto_remediation.py remediate-resource --kind Pod --name my-pod --namespace default
"""

import argparse
import sys
from typing import Dict, List, Optional

try:
    import kubernetes
    from kubernetes.client.rest import ApiException
except ImportError:
    print("❌ Error: kubernetes not installed. Install with: pip install kubernetes")
    sys.exit(1)


class AutoRemediation:
    """Automated remediation for Kubernetes resources."""
    
    def __init__(self, kubeconfig: Optional[str] = None):
        """
        Initialize auto remediation.
        
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
        
        self.core_v1 = kubernetes.client.CoreV1Api()
        self.apps_v1 = kubernetes.client.AppsV1Api()

    def remediate_namespace(
        self,
        namespace: str,
        dry_run: bool = False
    ) -> Dict:
        """
        Remediate all non-compliant resources in a namespace.
        
        Args:
            namespace: Namespace to remediate
            dry_run: If True, don't actually remediate
            
        Returns:
            Dictionary with remediation results
        """
        results = {
            'namespace': namespace,
            'remediated': [],
            'failed': [],
            'dry_run': dry_run,
        }
        
        print(f"🔧 Remediating namespace: {namespace} (dry_run={dry_run})...\n")
        
        # Get all pods
        try:
            pods = self.core_v1.list_namespaced_pod(namespace)
            
            for pod in pods.items:
                remediation = self._remediate_pod(pod, dry_run)
                if remediation['remediated']:
                    results['remediated'].append({
                        'kind': 'Pod',
                        'name': pod.metadata.name,
                        'actions': remediation['actions'],
                    })
                elif remediation['error']:
                    results['failed'].append({
                        'kind': 'Pod',
                        'name': pod.metadata.name,
                        'error': remediation['error'],
                    })
        except ApiException as e:
            print(f"❌ Error listing pods: {e}")
            results['error'] = str(e)
        
        return results

    def _remediate_pod(self, pod, dry_run: bool = False) -> Dict:
        """
        Remediate a pod to ensure compliance.
        
        Args:
            pod: Pod object
            dry_run: If True, don't actually remediate
            
        Returns:
            Dictionary with remediation results
        """
        actions = []
        needs_update = False
        pod_body = None
        
        try:
            # Check if running as root
            if pod.spec.security_context and pod.spec.security_context.run_as_user == 0:
                if not dry_run:
                    if not pod.spec.security_context:
                        pod.spec.security_context = kubernetes.client.V1SecurityContext()
                    pod.spec.security_context.run_as_user = 1000
                    pod.spec.security_context.run_as_non_root = True
                    needs_update = True
                    actions.append('Set runAsUser to 1000 (non-root)')
                else:
                    actions.append('[DRY RUN] Would set runAsUser to 1000')
            
            # Check resource limits
            for container in pod.spec.containers:
                if not container.resources or not container.resources.limits:
                    if not dry_run:
                        if not container.resources:
                            container.resources = kubernetes.client.V1ResourceRequirements()
                        if not container.resources.limits:
                            container.resources.limits = {}
                        container.resources.limits['cpu'] = '500m'
                        container.resources.limits['memory'] = '512Mi'
                        needs_update = True
                        actions.append(f'Set resource limits for {container.name}')
                    else:
                        actions.append(f'[DRY RUN] Would set resource limits for {container.name}')
            
            if needs_update and not dry_run:
                # Note: Pods cannot be updated directly, need to patch or recreate
                # This is a simplified example - real implementation would use patches
                print(f"  ⚠️  Pod {pod.metadata.name} needs remediation but cannot be updated directly")
                print(f"     Consider using patches or recreating the pod")
                return {
                    'remediated': False,
                    'actions': actions,
                    'error': 'Pods cannot be updated directly',
                }
            
            return {
                'remediated': len(actions) > 0,
                'actions': actions,
            }
            
        except Exception as e:
            return {
                'remediated': False,
                'error': str(e),
            }

    def remediate_resource(
        self,
        kind: str,
        name: str,
        namespace: str,
        dry_run: bool = False
    ) -> Dict:
        """
        Remediate a specific resource.
        
        Args:
            kind: Resource kind (Pod, Deployment, etc.)
            name: Resource name
            namespace: Namespace
            dry_run: If True, don't actually remediate
            
        Returns:
            Dictionary with remediation results
        """
        print(f"🔧 Remediating {kind}/{name} in {namespace} (dry_run={dry_run})...")
        
        if kind.lower() == 'pod':
            try:
                pod = self.core_v1.read_namespaced_pod(name, namespace)
                return self._remediate_pod(pod, dry_run)
            except ApiException as e:
                return {
                    'remediated': False,
                    'error': f'Error reading pod: {e}',
                }
        else:
            return {
                'remediated': False,
                'error': f'Remediation for {kind} not implemented',
            }


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Automated Remediation - Remediate security and compliance issues",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "--kubeconfig",
        help="Path to kubeconfig file"
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be remediated without actually doing it"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Remediate namespace
    ns_parser = subparsers.add_parser("remediate", help="Remediate namespace")
    ns_parser.add_argument("--namespace", required=True, help="Namespace to remediate")
    
    # Remediate resource
    res_parser = subparsers.add_parser("remediate-resource", help="Remediate specific resource")
    res_parser.add_argument("--kind", required=True, help="Resource kind (Pod, Deployment, etc.)")
    res_parser.add_argument("--name", required=True, help="Resource name")
    res_parser.add_argument("--namespace", required=True, help="Namespace")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        remediator = AutoRemediation(kubeconfig=args.kubeconfig)
        
        if args.command == "remediate":
            results = remediator.remediate_namespace(args.namespace, dry_run=args.dry_run)
            
            print(f"\n📊 Remediation Results:")
            print(f"  Remediated: {len(results['remediated'])}")
            print(f"  Failed: {len(results['failed'])}")
            
            if results['remediated']:
                print(f"\n✅ Remediated Resources:")
                for item in results['remediated']:
                    print(f"  - {item['kind']}/{item['name']}")
                    for action in item['actions']:
                        print(f"    • {action}")
            
            if results['failed']:
                print(f"\n❌ Failed Resources:")
                for item in results['failed']:
                    print(f"  - {item['kind']}/{item['name']}: {item['error']}")
                    
        elif args.command == "remediate-resource":
            results = remediator.remediate_resource(
                args.kind,
                args.name,
                args.namespace,
                dry_run=args.dry_run
            )
            
            if results.get('remediated'):
                print(f"\n✅ Remediated {args.kind}/{args.name}")
                for action in results.get('actions', []):
                    print(f"  • {action}")
            else:
                print(f"\n❌ Failed to remediate {args.kind}/{args.name}")
                if 'error' in results:
                    print(f"  Error: {results['error']}")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())

