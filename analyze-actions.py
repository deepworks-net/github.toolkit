#!/usr/bin/env python3
"""
Action Analysis for Repository Reorganization - Phase 2
Model: github.toolkit.reorganization v1.0.0

Analyzes existing actions to prepare for FCM transformation.
"""

import os
import yaml
import json
from pathlib import Path
from typing import Dict, List, Any, Set
from dataclasses import dataclass, field, asdict
from collections import defaultdict

@dataclass
class ActionAnalysis:
    """Analysis results for a single action."""
    name: str
    path: str
    type: str  # 'core' or 'composite'
    domain: str  # 'git', 'version', 'release', 'github'
    inputs: Dict[str, Any] = field(default_factory=dict)
    outputs: Dict[str, Any] = field(default_factory=dict)
    hardcoded_values: List[Dict[str, Any]] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    patterns: List[str] = field(default_factory=list)
    docker_info: Dict[str, Any] = field(default_factory=dict)
    implementation_files: List[str] = field(default_factory=list)
    test_files: List[str] = field(default_factory=list)

class ActionAnalyzer:
    """Analyzes GitHub Actions for reorganization."""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.actions_dir = self.project_root / "actions"
        self.analyses: List[ActionAnalysis] = []
        
    def analyze_all_actions(self) -> None:
        """Analyze all actions in the repository."""
        print("Analyzing GitHub Actions...")
        
        # Analyze core actions
        core_dir = self.actions_dir / "core"
        if core_dir.exists():
            for action_dir in core_dir.iterdir():
                if action_dir.is_dir() and (action_dir / "action.yml").exists():
                    self.analyze_action(action_dir, "core")
        
        # Analyze composite actions
        composite_dir = self.actions_dir / "composite"
        if composite_dir.exists():
            for action_dir in composite_dir.iterdir():
                if action_dir.is_dir() and (action_dir / "action.yml").exists():
                    self.analyze_action(action_dir, "composite")
    
    def analyze_action(self, action_path: Path, action_type: str) -> ActionAnalysis:
        """Analyze a single action."""
        action_name = action_path.name
        print(f"\nAnalyzing {action_type} action: {action_name}")
        
        analysis = ActionAnalysis(
            name=action_name,
            path=str(action_path.relative_to(self.project_root)),
            type=action_type,
            domain=self.determine_domain(action_name)
        )
        
        # Load action.yml
        action_yml_path = action_path / "action.yml"
        if action_yml_path.exists():
            with open(action_yml_path, 'r') as f:
                action_config = yaml.safe_load(f)
                
            # Extract inputs and outputs
            analysis.inputs = action_config.get('inputs', {})
            analysis.outputs = action_config.get('outputs', {})
            
            # Check for hardcoded values in action.yml
            self.find_hardcoded_values_in_yaml(action_config, analysis)
        
        # Analyze implementation files
        self.analyze_implementation_files(action_path, analysis)
        
        # Analyze Dockerfile
        dockerfile_path = action_path / "Dockerfile"
        if dockerfile_path.exists():
            self.analyze_dockerfile(dockerfile_path, analysis)
        
        # Find test files
        test_dir = action_path / "tests"
        if test_dir.exists():
            analysis.test_files = [str(f.relative_to(action_path)) 
                                   for f in test_dir.glob("*.py")]
        
        # Identify patterns
        self.identify_patterns(analysis)
        
        self.analyses.append(analysis)
        return analysis
    
    def determine_domain(self, action_name: str) -> str:
        """Determine the domain of an action based on its name."""
        if 'branch' in action_name or 'tag' in action_name or 'commit' in action_name:
            return 'git'
        elif 'version' in action_name:
            return 'version'
        elif 'release' in action_name or 'changelog' in action_name:
            return 'release'
        else:
            return 'github'
    
    def find_hardcoded_values_in_yaml(self, config: Dict, analysis: ActionAnalysis) -> None:
        """Find hardcoded values in YAML configuration."""
        # Check for version numbers
        yaml_str = str(config)
        import re
        
        # Version patterns
        version_matches = re.findall(r'\b\d+\.\d+\.\d+\b', yaml_str)
        for match in version_matches:
            analysis.hardcoded_values.append({
                'type': 'version',
                'value': match,
                'location': 'action.yml'
            })
    
    def analyze_implementation_files(self, action_path: Path, analysis: ActionAnalysis) -> None:
        """Analyze Python/shell implementation files."""
        # Find Python files
        py_files = list(action_path.glob("*.py"))
        if action_path / "src" in action_path.iterdir():
            py_files.extend((action_path / "src").glob("*.py"))
        
        for py_file in py_files:
            analysis.implementation_files.append(str(py_file.relative_to(action_path)))
            self.analyze_python_file(py_file, analysis)
        
        # Find shell scripts
        sh_files = list(action_path.glob("*.sh"))
        for sh_file in sh_files:
            analysis.implementation_files.append(str(sh_file.relative_to(action_path)))
    
    def analyze_python_file(self, py_file: Path, analysis: ActionAnalysis) -> None:
        """Analyze a Python file for hardcoded values and dependencies."""
        try:
            with open(py_file, 'r') as f:
                content = f.read()
            
            # Find imports (dependencies)
            import re
            import_matches = re.findall(r'^(?:from|import)\s+(\S+)', content, re.MULTILINE)
            for imp in import_matches:
                base_module = imp.split('.')[0]
                if base_module not in ['os', 'sys', 'json', 'yaml', 're', 'subprocess']:
                    analysis.dependencies.append(base_module)
            
            # Find hardcoded strings that might be configuration
            string_matches = re.findall(r'["\']([^"\']+)["\']', content)
            for match in string_matches:
                # Check for paths
                if '/' in match and not match.startswith('http'):
                    analysis.hardcoded_values.append({
                        'type': 'path',
                        'value': match,
                        'location': str(py_file.name)
                    })
                # Check for version-like strings
                elif re.match(r'^\d+\.\d+\.\d+$', match):
                    analysis.hardcoded_values.append({
                        'type': 'version',
                        'value': match,
                        'location': str(py_file.name)
                    })
        except Exception as e:
            print(f"  Warning: Could not analyze {py_file}: {e}")
    
    def analyze_dockerfile(self, dockerfile_path: Path, analysis: ActionAnalysis) -> None:
        """Analyze Dockerfile for configuration."""
        try:
            with open(dockerfile_path, 'r') as f:
                content = f.read()
            
            # Extract base image
            import re
            from_match = re.search(r'^FROM\s+(.+)$', content, re.MULTILINE)
            if from_match:
                analysis.docker_info['base_image'] = from_match.group(1)
            
            # Find version pins
            version_matches = re.findall(r'[=><]+\s*(\d+\.\d+(?:\.\d+)?)', content)
            for match in version_matches:
                analysis.hardcoded_values.append({
                    'type': 'version',
                    'value': match,
                    'location': 'Dockerfile'
                })
        except Exception as e:
            print(f"  Warning: Could not analyze Dockerfile: {e}")
    
    def identify_patterns(self, analysis: ActionAnalysis) -> None:
        """Identify common patterns in the action."""
        patterns = []
        
        # Git operation pattern
        if analysis.domain == 'git':
            if 'branch' in analysis.name:
                patterns.append('git-branch-operation')
            elif 'tag' in analysis.name:
                patterns.append('git-tag-operation')
            elif 'commit' in analysis.name:
                patterns.append('git-commit-operation')
        
        # Version manipulation pattern
        if analysis.domain == 'version':
            patterns.append('version-manipulation')
        
        # File update pattern
        if any('file' in inp.lower() or 'path' in inp.lower() 
               for inp in analysis.inputs.keys()):
            patterns.append('file-update')
        
        # GitHub API pattern
        if 'github' in str(analysis.dependencies).lower():
            patterns.append('github-api-interaction')
        
        analysis.patterns = patterns
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate analysis report."""
        report = {
            'summary': {
                'total_actions': len(self.analyses),
                'core_actions': len([a for a in self.analyses if a.type == 'core']),
                'composite_actions': len([a for a in self.analyses if a.type == 'composite']),
                'domains': defaultdict(int),
                'patterns': defaultdict(int),
                'hardcoded_values': defaultdict(int)
            },
            'actions': []
        }
        
        # Aggregate statistics
        for analysis in self.analyses:
            report['summary']['domains'][analysis.domain] += 1
            
            for pattern in analysis.patterns:
                report['summary']['patterns'][pattern] += 1
            
            for hardcoded in analysis.hardcoded_values:
                report['summary']['hardcoded_values'][hardcoded['type']] += 1
            
            # Add action details
            report['actions'].append(asdict(analysis))
        
        return report
    
    def generate_migration_plan(self) -> Dict[str, Any]:
        """Generate migration plan for Phase 2."""
        plan = {
            'phase2_tasks': []
        }
        
        for analysis in self.analyses:
            task = {
                'action': analysis.name,
                'steps': []
            }
            
            # Step 1: Create FCM
            task['steps'].append({
                'step': 'create_fcm',
                'description': f'Create axioms/{analysis.domain}/{analysis.name}.fcm',
                'preserve': ['inputs', 'outputs', 'behavior'],
                'remove': ['docker_details', 'implementation']
            })
            
            # Step 2: Extract parameters
            if analysis.hardcoded_values:
                task['steps'].append({
                    'step': 'extract_parameters',
                    'description': 'Replace hardcoded values with parameters',
                    'values': analysis.hardcoded_values
                })
            
            # Step 3: Create template
            if analysis.docker_info:
                task['steps'].append({
                    'step': 'create_template',
                    'description': f'Create mechanics/actions/{analysis.name}.template',
                    'from': f'{analysis.path}/Dockerfile'
                })
            
            # Step 4: External package
            if analysis.implementation_files:
                task['steps'].append({
                    'step': 'create_package',
                    'description': f'Publish to github.com/deepworks-net/{analysis.name}-action',
                    'files': analysis.implementation_files
                })
            
            plan['phase2_tasks'].append(task)
        
        return plan

def main():
    """Main entry point."""
    analyzer = ActionAnalyzer()
    
    print("=== GitHub Actions Analysis for Repository Reorganization ===")
    print("Model: github.toolkit.reorganization v1.0.0")
    print()
    
    # Analyze all actions
    analyzer.analyze_all_actions()
    
    # Generate report
    report = analyzer.generate_report()
    
    print("\n=== Analysis Summary ===")
    print(f"Total actions analyzed: {report['summary']['total_actions']}")
    print(f"Core actions: {report['summary']['core_actions']}")
    print(f"Composite actions: {report['summary']['composite_actions']}")
    
    print("\nActions by domain:")
    for domain, count in report['summary']['domains'].items():
        print(f"  {domain}: {count}")
    
    print("\nCommon patterns found:")
    for pattern, count in report['summary']['patterns'].items():
        print(f"  {pattern}: {count}")
    
    print("\nHardcoded values found:")
    for value_type, count in report['summary']['hardcoded_values'].items():
        print(f"  {value_type}: {count}")
    
    # Generate migration plan
    migration_plan = analyzer.generate_migration_plan()
    
    # Save reports
    with open('action-analysis-report.json', 'w') as f:
        json.dump(report, f, indent=2)
    print("\nDetailed report saved to: action-analysis-report.json")
    
    with open('phase2-migration-plan.json', 'w') as f:
        json.dump(migration_plan, f, indent=2)
    print("Migration plan saved to: phase2-migration-plan.json")
    
    print("\n=== Next Steps ===")
    print("1. Review action-analysis-report.json for detailed findings")
    print("2. Review phase2-migration-plan.json for migration tasks")
    print("3. Begin Phase 2 transformation following the migration plan")

if __name__ == "__main__":
    main()