#!/usr/bin/env python3
"""
Chaos Monkey

Randomly terminate pods and resources to test system resilience.

Usage:
    # Run chaos monkey
    python chaos_monkey.py run --experiment-type pod-delete
    
    # Enable/disable
    python chaos_monkey.py enable
    python chaos_monkey.py disable
    
    # Set probability
    python chaos_monkey.py set-probability --probability 0.1
"""

import argparse
import random
import sys
from typing import Dict, List, Optional

try:
    import kubernetes
    from kubernetes.client.rest import ApiException
except ImportError:
    print("❌ Error: kubernetes not installed. Install with: pip install kubernetes")
    sys.exit(1)


class ChaosMonkey:
    """Chaos Monkey for Kubernetes - Randomly terminate resources."""
    
    def __init__(self, enabled: bool = True, probability: float = 0.1, kubeconfig: Optional[str] = None):
        """
        Initialize Chaos Monkey.
        
        Args:
            enabled: Whether chaos monkey is enabled
            probability: Probability of chaos (0.0 to 1.0)
            kubeconfig: Path to kubeconfig file (optional)
        """
        self.enabled = enabled
        self.probability = probability
        
        if kubeconfig:
            kubernetes.config.load_kube_config(config_file=kubeconfig)
        else:
            try:
                kubernetes.config.load_incluster_config()
            except:
                kubernetes.config.load_kube_config()
        
        self.core_v1 = kubernetes.client.CoreV1Api()
        self.apps_v1 = kubernetes.client.AppsV1Api()

    def run_experiment(self, experiment_type: str) -> Dict:
        """
        Run a chaos experiment.
        
        Args:
            experiment_type: Type of experiment (pod-delete, node-drain, cpu-stress, etc.)
            
        Returns:
            Dictionary with experiment results
        """
        if not self.enabled:
            return {
                'status': 'skipped',
                'reason': 'Chaos Monkey is disabled',
            }

        if random.random() > self.probability:
            return {
                'status': 'skipped',
                'reason': f'Random skip (probability: {self.probability})',
            }

        try:
            if experiment_type == 'pod-delete':
                return self._delete_random_pod()
            elif experiment_type == 'node-drain':
                return self._drain_random_node()
            elif experiment_type == 'cpu-stress':
                return self._stress_cpu()
            elif experiment_type == 'memory-stress':
                return self._stress_memory()
            elif experiment_type == 'network-partition':
                return self._partition_network()
            else:
                return {
                    'status': 'error',
                    'error': f'Unknown experiment type: {experiment_type}',
                }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
            }

    def _delete_random_pod(self) -> Dict:
        """Delete a random pod from a deployment."""
        try:
            # Get all deployments
            deployments = self.apps_v1.list_deployment_for_all_namespaces()
            
            # Filter to deployments with chaos annotation
            chaos_deployments = [
                d for d in deployments.items
                if d.metadata.annotations and 
                d.metadata.annotations.get('chaos.enabled') == 'true'
            ]
            
            if not chaos_deployments:
                return {
                    'status': 'skipped',
                    'reason': 'No deployments with chaos.enabled=true annotation found',
                }
            
            # Pick random deployment
            deployment = random.choice(chaos_deployments)
            namespace = deployment.metadata.namespace
            app_label = deployment.metadata.labels.get('app') or deployment.metadata.name
            
            # Get pods for this deployment
            pods = self.core_v1.list_namespaced_pod(
                namespace,
                label_selector=f"app={app_label}"
            )
            
            if not pods.items:
                return {
                    'status': 'skipped',
                    'reason': f'No pods found for deployment {deployment.metadata.name}',
                }
            
            # Pick random pod
            pod = random.choice(pods.items)
            pod_name = pod.metadata.name
            
            # Delete pod
            self.core_v1.delete_namespaced_pod(
                pod_name,
                namespace,
                grace_period_seconds=0
            )
            
            print(f"💥 Chaos Monkey: Deleted pod {pod_name} in namespace {namespace}")
            
            return {
                'status': 'success',
                'experiment': 'pod-delete',
                'pod': pod_name,
                'namespace': namespace,
                'deployment': deployment.metadata.name,
            }
            
        except ApiException as e:
            return {
                'status': 'error',
                'error': f'Kubernetes API error: {e}',
            }

    def _drain_random_node(self) -> Dict:
        """Drain a random node (placeholder - requires node access)."""
        return {
            'status': 'not_implemented',
            'message': 'Node draining requires additional permissions and implementation',
        }

    def _stress_cpu(self) -> Dict:
        """Stress CPU on random pod (placeholder)."""
        return {
            'status': 'not_implemented',
            'message': 'CPU stress requires additional tools (stress-ng)',
        }

    def _stress_memory(self) -> Dict:
        """Stress memory on random pod (placeholder)."""
        return {
            'status': 'not_implemented',
            'message': 'Memory stress requires additional tools',
        }

    def _partition_network(self) -> Dict:
        """Create network partition (placeholder)."""
        return {
            'status': 'not_implemented',
            'message': 'Network partition requires network policy manipulation',
        }


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Chaos Monkey - Randomly terminate resources to test resilience",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "--kubeconfig",
        help="Path to kubeconfig file"
    )
    
    parser.add_argument(
        "--probability",
        type=float,
        default=0.1,
        help="Probability of chaos (0.0 to 1.0, default: 0.1)"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Run command
    run_parser = subparsers.add_parser("run", help="Run chaos experiment")
    run_parser.add_argument(
        "--experiment-type",
        choices=['pod-delete', 'node-drain', 'cpu-stress', 'memory-stress', 'network-partition'],
        default='pod-delete',
        help="Type of experiment to run"
    )
    
    # Enable/disable
    subparsers.add_parser("enable", help="Enable Chaos Monkey")
    subparsers.add_parser("disable", help="Disable Chaos Monkey")
    
    # Set probability
    prob_parser = subparsers.add_parser("set-probability", help="Set chaos probability")
    prob_parser.add_argument("--probability", type=float, required=True, help="Probability (0.0 to 1.0)")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        enabled = args.command != 'disable'
        monkey = ChaosMonkey(
            enabled=enabled,
            probability=args.probability,
            kubeconfig=args.kubeconfig
        )
        
        if args.command == "run":
            result = monkey.run_experiment(args.experiment_type)
            
            if result['status'] == 'success':
                print(f"✅ Experiment completed: {result.get('experiment')}")
                print(f"   Pod: {result.get('pod')}")
                print(f"   Namespace: {result.get('namespace')}")
            elif result['status'] == 'skipped':
                print(f"⏭️  Experiment skipped: {result.get('reason')}")
            else:
                print(f"❌ Experiment failed: {result.get('error', 'Unknown error')}")
                
        elif args.command in ["enable", "disable"]:
            status = "enabled" if enabled else "disabled"
            print(f"✅ Chaos Monkey {status}")
            
        elif args.command == "set-probability":
            monkey.probability = args.probability
            print(f"✅ Probability set to {args.probability}")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())

