#!/usr/bin/env python3
"""
Chaos Experiments

Framework for running and managing chaos experiments.

Usage:
    # Run experiment
    python experiments.py run --name pod-delete
    
    # List experiments
    python experiments.py list
    
    # Register new experiment
    python experiments.py register --name my-experiment --description "My chaos experiment"
"""

import argparse
import sys
from dataclasses import dataclass, field
from datetime import datetime
from typing import Callable, Dict, List, Optional


@dataclass
class ChaosExperiment:
    """Chaos experiment definition."""
    name: str
    description: str
    hypothesis: str
    experiment_fn: Callable
    duration_seconds: int
    expected_behavior: str
    enabled: bool = True


class ExperimentRunner:
    """Run and manage chaos experiments."""
    
    def __init__(self):
        """Initialize experiment runner."""
        self.experiments: List[ChaosExperiment] = []

    def register_experiment(self, experiment: ChaosExperiment):
        """
        Register a chaos experiment.
        
        Args:
            experiment: Chaos experiment to register
        """
        self.experiments.append(experiment)
        print(f"✅ Registered experiment: {experiment.name}")

    def run_experiment(self, experiment_name: str) -> Dict:
        """
        Run a specific experiment.
        
        Args:
            experiment_name: Name of experiment to run
            
        Returns:
            Dictionary with experiment results
        """
        experiment = next(
            (e for e in self.experiments if e.name == experiment_name),
            None
        )
        
        if not experiment:
            return {
                'status': 'error',
                'error': f'Experiment {experiment_name} not found',
            }
        
        if not experiment.enabled:
            return {
                'status': 'skipped',
                'reason': 'Experiment is disabled',
            }
        
        print(f"🧪 Running experiment: {experiment.name}")
        print(f"   Hypothesis: {experiment.hypothesis}")
        print(f"   Expected behavior: {experiment.expected_behavior}")
        print(f"   Duration: {experiment.duration_seconds}s")
        
        start_time = datetime.now()
        
        try:
            # Run experiment
            result = experiment.experiment_fn()
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            return {
                'experiment': experiment.name,
                'status': 'success',
                'duration': duration,
                'result': result,
                'start_time': start_time.isoformat(),
                'end_time': end_time.isoformat(),
            }
        except Exception as e:
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            return {
                'experiment': experiment.name,
                'status': 'failed',
                'duration': duration,
                'error': str(e),
                'start_time': start_time.isoformat(),
                'end_time': end_time.isoformat(),
            }

    def list_experiments(self) -> List[Dict]:
        """
        List all registered experiments.
        
        Returns:
            List of experiment information
        """
        return [
            {
                'name': exp.name,
                'description': exp.description,
                'hypothesis': exp.hypothesis,
                'duration_seconds': exp.duration_seconds,
                'enabled': exp.enabled,
            }
            for exp in self.experiments
        ]


# Example experiment functions
def pod_delete_experiment():
    """Example: Delete random pod, system should recover."""
    # This would integrate with chaos_monkey.py
    return {
        'pods_deleted': 1,
        'recovery_time': 30,
        'message': 'System recovered successfully',
    }


def network_latency_experiment():
    """Example: Add network latency, system should handle gracefully."""
    return {
        'latency_added_ms': 100,
        'impact': 'minimal',
        'message': 'System handled latency gracefully',
    }


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Chaos Experiments - Run and manage chaos experiments",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Run command
    run_parser = subparsers.add_parser("run", help="Run an experiment")
    run_parser.add_argument("--name", required=True, help="Experiment name")
    
    # List command
    subparsers.add_parser("list", help="List all experiments")
    
    # Register command
    register_parser = subparsers.add_parser("register", help="Register new experiment")
    register_parser.add_argument("--name", required=True, help="Experiment name")
    register_parser.add_argument("--description", required=True, help="Experiment description")
    register_parser.add_argument("--hypothesis", required=True, help="Experiment hypothesis")
    register_parser.add_argument("--duration", type=int, default=60, help="Duration in seconds")
    register_parser.add_argument("--expected-behavior", required=True, help="Expected behavior")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        runner = ExperimentRunner()
        
        # Register example experiments
        runner.register_experiment(ChaosExperiment(
            name='pod-delete',
            description='Delete random pod from deployment',
            hypothesis='System should recover within 60 seconds',
            experiment_fn=pod_delete_experiment,
            duration_seconds=60,
            expected_behavior='Service remains available',
        ))
        
        runner.register_experiment(ChaosExperiment(
            name='network-latency',
            description='Add network latency to test resilience',
            hypothesis='System should handle increased latency gracefully',
            experiment_fn=network_latency_experiment,
            duration_seconds=120,
            expected_behavior='No significant degradation',
        ))
        
        if args.command == "run":
            result = runner.run_experiment(args.name)
            
            print(f"\n📊 Experiment Results:")
            print(f"   Status: {result['status']}")
            print(f"   Duration: {result.get('duration', 0):.2f}s")
            
            if result['status'] == 'success':
                print(f"   Result: {result.get('result', {})}")
            elif result['status'] == 'failed':
                print(f"   Error: {result.get('error')}")
                
        elif args.command == "list":
            experiments = runner.list_experiments()
            
            if not experiments:
                print("No experiments registered")
                return 0
            
            print(f"\n📋 Registered Experiments ({len(experiments)}):\n")
            for exp in experiments:
                status = "✅ Enabled" if exp['enabled'] else "❌ Disabled"
                print(f"  {exp['name']} - {status}")
                print(f"    Description: {exp['description']}")
                print(f"    Hypothesis: {exp['hypothesis']}")
                print(f"    Duration: {exp['duration_seconds']}s")
                print()
                
        elif args.command == "register":
            # Note: This is a simplified registration - real implementation would
            # need to handle function registration differently
            print(f"✅ Experiment '{args.name}' registered (simplified)")
            print("   Note: Full registration requires function implementation")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())

