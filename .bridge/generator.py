#!/usr/bin/env python3
"""
FCM to GitHub Action Bridge Generator
Model: github.toolkit.bridge v1.0.0

Generates GitHub-compatible action.yml files from FCM definitions.
"""

import os
import re
import json
import yaml
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional

class FCMParser:
    """Parse FCM (Formal Conceptual Model) files."""
    
    def __init__(self, fcm_path: Path):
        self.fcm_path = fcm_path
        self.content = self._read_fcm()
        self.parsed = self._parse_content()
    
    def _read_fcm(self) -> str:
        """Read FCM file content."""
        with open(self.fcm_path, 'r') as f:
            return f.read()
    
    def _parse_content(self) -> Dict[str, Any]:
        """Parse FCM content into structured data."""
        parsed = {
            'metadata': {},
            'capability': '',
            'parameters': [],
            'outputs': [],
            'interface': {},
            'dependencies': [],
            'patterns': []
        }
        
        current_section = None
        current_list = None
        
        for line in self.content.strip().split('\n'):
            line = line.strip()
            
            # Skip empty lines and comments
            if not line or line.startswith('#'):
                continue
            
            # Parse metadata
            if line.startswith('Model:'):
                parsed['metadata']['model'] = line.split(':', 1)[1].strip()
            elif line.startswith('Version:'):
                parsed['metadata']['version'] = line.split(':', 1)[1].strip()
            elif line.startswith('Layer:'):
                parsed['metadata']['layer'] = line.split(':', 1)[1].strip()
            elif line.startswith('Domain:'):
                parsed['metadata']['domain'] = line.split(':', 1)[1].strip()
            
            # Parse sections
            elif line.startswith('Capability:'):
                parsed['capability'] = line.split(':', 1)[1].strip()
                current_section = 'capability'
            
            elif line == 'Parameters:':
                current_section = 'parameters'
                current_list = 'parameters'
            
            elif line == 'Outputs:':
                current_section = 'outputs'
                current_list = 'outputs'
            
            elif line == 'Interface:':
                current_section = 'interface'
                current_list = None
            
            elif line == 'Dependencies:':
                current_section = 'dependencies'
                current_list = 'dependencies'
            
            elif line == 'Patterns:':
                current_section = 'patterns'
                current_list = 'patterns'
            
            # Parse list items
            elif line.startswith('- ') and current_list:
                item = line[2:].strip()
                if current_list in ['parameters', 'outputs']:
                    # Parse parameter/output definition
                    parsed[current_list].append(self._parse_parameter(item))
                else:
                    parsed[current_list].append(item)
            
            # Parse interface properties
            elif current_section == 'interface' and ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()
                
                # Handle list values
                if value.startswith('[') and value.endswith(']'):
                    value = [v.strip() for v in value[1:-1].split(',')]
                
                parsed['interface'][key] = value
        
        return parsed
    
    def _parse_parameter(self, param_str: str) -> Dict[str, Any]:
        """Parse parameter definition string."""
        # Format: name: type (constraints) [optional]
        param = {'name': '', 'type': 'string', 'required': True, 'constraints': None}
        
        # Check if optional
        if '(optional)' in param_str:
            param['required'] = False
            param_str = param_str.replace('(optional)', '').strip()
        
        # Parse name and type
        if ':' in param_str:
            name, type_info = param_str.split(':', 1)
            param['name'] = name.strip()
            
            # Parse type and constraints
            type_info = type_info.strip()
            if '|' in type_info:
                # Enum type
                param['type'] = 'choice'
                param['constraints'] = type_info.split('|')
            else:
                param['type'] = type_info.split()[0]
        else:
            param['name'] = param_str.strip()
        
        return param

class FCMToActionBridge:
    """Generate GitHub Actions from FCM definitions."""
    
    def __init__(self, project_root: Path = Path('.')):
        self.project_root = project_root
        self.bridge_dir = project_root / '.bridge'
        self.actions_dir = project_root / 'actions'
        self.axioms_dir = project_root / 'axioms'
        self.patterns_dir = project_root / 'patterns'
        self.mechanics_dir = project_root / 'mechanics'
        
        # Load manifest
        self.manifest_path = self.bridge_dir / 'manifest.json'
        self.manifest = self._load_manifest()
    
    def _load_manifest(self) -> Dict[str, Any]:
        """Load bridge manifest."""
        if self.manifest_path.exists():
            with open(self.manifest_path, 'r') as f:
                return json.load(f)
        return {'mappings': {}, 'generated': {}}
    
    def _save_manifest(self):
        """Save bridge manifest."""
        with open(self.manifest_path, 'w') as f:
            json.dump(self.manifest, f, indent=2)
    
    def generate_action_yml(self, fcm_path: Path) -> Path:
        """Generate action.yml from FCM."""
        parser = FCMParser(fcm_path)
        fcm = parser.parsed
        
        # Determine output path
        domain = fcm['metadata'].get('domain', 'misc')
        model_name = fcm['metadata']['model'].split('.')[-1]
        action_name = model_name.replace('_', '-')
        
        output_dir = self.actions_dir / 'core' / action_name
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate action.yml content
        action_yml = {
            'name': f"{action_name.replace('-', ' ').title()}",
            'description': fcm['capability'],
            'inputs': {},
            'outputs': {},
            'runs': {
                'using': 'docker',
                'image': 'Dockerfile'
            }
        }
        
        # Add generated metadata comment
        header_comment = f"""# Generated from {fcm_path.relative_to(self.project_root)}
# Model: {fcm['metadata']['model']} v{fcm['metadata'].get('version', '1.0.0')}
# Generated: {datetime.utcnow().isoformat()}Z
# DO NOT EDIT - Changes will be overwritten by bridge generator
"""
        
        # Process parameters into inputs
        for param in fcm['parameters']:
            input_def = {
                'description': f"{param['name'].replace('_', ' ').title()}",
                'required': param['required']
            }
            
            # Add default value if not required
            if not param['required']:
                input_def['default'] = ''
            
            # Add enum values if choice type
            if param['type'] == 'choice' and param['constraints']:
                input_def['description'] += f" (Options: {', '.join(param['constraints'])})"
            
            action_yml['inputs'][param['name']] = input_def
        
        # Process outputs
        for output in fcm['outputs']:
            output_name = output['name'] if isinstance(output, dict) else output
            action_yml['outputs'][output_name] = {
                'description': f"{output_name.replace('_', ' ').title()}"
            }
        
        # Write action.yml
        action_yml_path = output_dir / 'action.yml'
        with open(action_yml_path, 'w') as f:
            f.write(header_comment)
            yaml.dump(action_yml, f, default_flow_style=False, sort_keys=False)
        
        # Generate Dockerfile
        self._generate_dockerfile(fcm, output_dir)
        
        # Generate bridge sync file
        self._generate_sync_file(fcm_path, output_dir)
        
        # Update manifest
        rel_fcm_path = str(fcm_path.relative_to(self.project_root))
        rel_action_path = str(output_dir.relative_to(self.project_root))
        
        self.manifest['mappings'][rel_fcm_path] = rel_action_path
        self.manifest['generated'][rel_action_path] = {
            'source': rel_fcm_path,
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'model_version': fcm['metadata'].get('version', '1.0.0')
        }
        self._save_manifest()
        
        return action_yml_path
    
    def _generate_dockerfile(self, fcm: Dict[str, Any], output_dir: Path):
        """Generate Dockerfile from FCM interface definition."""
        interface = fcm['interface']
        
        # Determine base image
        base_image = interface.get('image', 'python:3.9-slim')
        
        # Build Dockerfile content
        dockerfile_lines = [
            f"# Generated from FCM - DO NOT EDIT",
            f"FROM {base_image}",
            "",
            "# Install system requirements"
        ]
        
        # Add system requirements
        requirements = interface.get('requirements', [])
        if requirements:
            if 'git' in requirements:
                dockerfile_lines.append("RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*")
            
        dockerfile_lines.extend([
            "",
            "# Copy implementation",
            "COPY entrypoint.sh /entrypoint.sh",
            "RUN chmod +x /entrypoint.sh",
            "",
            "ENTRYPOINT [\"/entrypoint.sh\"]"
        ])
        
        # Write Dockerfile
        dockerfile_path = output_dir / 'Dockerfile'
        with open(dockerfile_path, 'w') as f:
            f.write('\n'.join(dockerfile_lines))
        
        # Generate placeholder entrypoint
        self._generate_entrypoint(fcm, output_dir)
    
    def _generate_entrypoint(self, fcm: Dict[str, Any], output_dir: Path):
        """Generate entrypoint script placeholder."""
        model_name = fcm['metadata']['model'].split('.')[-1]
        
        entrypoint_content = f"""#!/bin/bash
# Generated entrypoint for {model_name}
# Implementation should be provided by external package

echo "Action: {model_name}"
echo "Capability: {fcm['capability']}"
echo ""
echo "This is a generated placeholder."
echo "Actual implementation should be at: github.com/deepworks-net/{model_name}-action"

# Pass through to external implementation
# exec python -m {model_name}_action "$@"
"""
        
        entrypoint_path = output_dir / 'entrypoint.sh'
        with open(entrypoint_path, 'w') as f:
            f.write(entrypoint_content)
        
        # Make executable
        os.chmod(entrypoint_path, 0o755)
    
    def _generate_sync_file(self, fcm_path: Path, output_dir: Path):
        """Generate bridge sync metadata file."""
        # Calculate FCM checksum
        with open(fcm_path, 'rb') as f:
            checksum = hashlib.sha256(f.read()).hexdigest()
        
        sync_data = {
            'source': str(fcm_path.relative_to(self.project_root)),
            'generated': datetime.utcnow().isoformat() + 'Z',
            'version': '1.0.0',
            'checksum': f"sha256:{checksum}"
        }
        
        sync_path = output_dir / '.bridge-sync'
        with open(sync_path, 'w') as f:
            json.dump(sync_data, f, indent=2)
    
    def generate_all(self):
        """Generate all actions from FCMs."""
        generated = []
        
        # Process all axioms
        for domain_dir in self.axioms_dir.iterdir():
            if domain_dir.is_dir():
                for fcm_file in domain_dir.glob('*.fcm'):
                    print(f"Generating action from: {fcm_file}")
                    try:
                        action_path = self.generate_action_yml(fcm_file)
                        generated.append(action_path)
                        print(f"  ✓ Generated: {action_path}")
                    except Exception as e:
                        print(f"  ✗ Error: {e}")
        
        return generated

def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='FCM to GitHub Action Bridge Generator')
    parser.add_argument('fcm_path', nargs='?', help='Path to FCM file')
    parser.add_argument('--generate-all', action='store_true', help='Generate all actions from FCMs')
    parser.add_argument('--project-root', default='.', help='Project root directory')
    
    args = parser.parse_args()
    
    bridge = FCMToActionBridge(Path(args.project_root))
    
    if args.generate_all:
        print("Generating all actions from FCMs...")
        generated = bridge.generate_all()
        print(f"\nGenerated {len(generated)} actions")
    elif args.fcm_path:
        fcm_path = Path(args.fcm_path)
        if not fcm_path.exists():
            print(f"Error: FCM file not found: {fcm_path}")
            return 1
        
        print(f"Generating action from: {fcm_path}")
        action_path = bridge.generate_action_yml(fcm_path)
        print(f"Generated: {action_path}")
    else:
        parser.print_help()
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())