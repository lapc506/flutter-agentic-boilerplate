#!/usr/bin/env python3
"""
Security Admission Controller

Validate pod security requirements in Kubernetes admission webhook.

Usage:
    # Run as webhook server
    python admission_controller.py serve --port 8443
    
    # Validate pod spec
    python admission_controller.py validate --pod-spec pod.json
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


class SecurityAdmissionController:
    """Security admission controller for Kubernetes."""
    
    def __init__(self, kubeconfig: Optional[str] = None):
        """
        Initialize admission controller.
        
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
        
        self.admission_api = kubernetes.client.AdmissionregistrationV1Api()

    def validate_pod(self, pod_spec: Dict) -> Dict:
        """
        Validate pod security requirements.
        
        Args:
            pod_spec: Pod specification dictionary
            
        Returns:
            Dictionary with validation results
        """
        violations = []
        warnings = []

        containers = pod_spec.get('spec', {}).get('containers', [])
        
        # Check for privileged containers
        for container in containers:
            container_name = container.get('name', 'unknown')
            security_context = container.get('securityContext', {})
            
            if security_context.get('privileged'):
                violations.append({
                    'container': container_name,
                    'violation': 'Privileged containers not allowed',
                    'severity': 'error',
                })

            # Check for root user
            run_as_user = security_context.get('runAsUser')
            if run_as_user == 0:
                violations.append({
                    'container': container_name,
                    'violation': 'Container must not run as root (runAsUser=0)',
                    'severity': 'error',
                })

            # Check for resource limits
            resources = container.get('resources', {})
            if not resources.get('limits'):
                warnings.append({
                    'container': container_name,
                    'warning': 'Container should have resource limits',
                    'severity': 'warning',
                })

            # Check for read-only root filesystem
            read_only = security_context.get('readOnlyRootFilesystem')
            if read_only is not True:
                warnings.append({
                    'container': container_name,
                    'warning': 'Consider using read-only root filesystem',
                    'severity': 'warning',
                })

        # Check pod-level security context
        pod_security_context = pod_spec.get('spec', {}).get('securityContext', {})
        if not pod_security_context.get('runAsNonRoot'):
            warnings.append({
                'pod': 'root',
                'warning': 'Pod should set runAsNonRoot=true',
                'severity': 'warning',
            })

        return {
            'valid': len(violations) == 0,
            'violations': violations,
            'warnings': warnings,
        }

    def validate_deployment(self, deployment_spec: Dict) -> Dict:
        """
        Validate deployment security requirements.
        
        Args:
            deployment_spec: Deployment specification dictionary
            
        Returns:
            Dictionary with validation results
        """
        pod_template = deployment_spec.get('spec', {}).get('template', {})
        return self.validate_pod(pod_template)


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Security Admission Controller - Validate pod security requirements",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "--kubeconfig",
        help="Path to kubeconfig file"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Validate command
    validate_parser = subparsers.add_parser("validate", help="Validate pod spec")
    validate_parser.add_argument("--pod-spec", help="Path to pod spec JSON file")
    validate_parser.add_argument("--deployment-spec", help="Path to deployment spec JSON file")
    
    # Serve command (simplified - full webhook implementation would be more complex)
    serve_parser = subparsers.add_parser("serve", help="Run as webhook server (placeholder)")
    serve_parser.add_argument("--port", type=int, default=8443, help="Server port")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        controller = SecurityAdmissionController(kubeconfig=args.kubeconfig)
        
        if args.command == "validate":
            if args.pod_spec:
                with open(args.pod_spec, 'r') as f:
                    pod_spec = json.load(f)
                result = controller.validate_pod(pod_spec)
            elif args.deployment_spec:
                with open(args.deployment_spec, 'r') as f:
                    deployment_spec = json.load(f)
                result = controller.validate_deployment(deployment_spec)
            else:
                print("❌ Error: --pod-spec or --deployment-spec required")
                return 1
            
            if result['valid']:
                print("✅ Pod spec is valid")
            else:
                print("❌ Pod spec has violations:")
                for violation in result['violations']:
                    print(f"  - {violation['container']}: {violation['violation']}")
            
            if result['warnings']:
                print("\n⚠️  Warnings:")
                for warning in result['warnings']:
                    print(f"  - {warning.get('container', 'pod')}: {warning['warning']}")
                    
        elif args.command == "serve":
            print("⚠️  Full webhook server implementation requires additional setup")
            print("   This is a placeholder - implement webhook server with Flask/FastAPI")
            print(f"   Would serve on port {args.port}")
        
        return 0 if result.get('valid', False) else 1
        
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())

