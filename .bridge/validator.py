#!/usr/bin/env python3
"""
Bridge Alignment Validator
Model: github.toolkit.bridge v1.0.0

Validates that generated actions are aligned with their FCM sources.
"""

import os
import json
import yaml
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Any

class BridgeValidator:
    """Validate bridge alignment between FCMs and generated actions."""
    
    def __init__(self, project_root: Path = Path('.')):
        self.project_root = project_root
        self.bridge_dir = project_root / '.bridge'
        self.actions_dir = project_root / 'actions'
        self.axioms_dir = project_root / 'axioms'
        
        # Load manifest
        self.manifest_path = self.bridge_dir / 'manifest.json'
        self.manifest = self._load_manifest()
        
        # Validation results
        self.results = {
            'valid': True,
            'checks': [],
            'errors': [],
            'warnings': []
        }
    
    def _load_manifest(self) -> Dict[str, Any]:
        """Load bridge manifest."""
        if self.manifest_path.exists():
            with open(self.manifest_path, 'r') as f:
                return json.load(f)
        return {'mappings': {}, 'generated': {}}
    
    def validate_all(self) -> Dict[str, Any]:
        """Run all validation checks."""
        print("=== Bridge Alignment Validation ===")
        print(f"Timestamp: {datetime.utcnow().isoformat()}Z")
        print()
        
        # Check 1: Verify all FCMs have corresponding actions
        self._check_fcm_coverage()
        
        # Check 2: Verify all generated actions have sync files
        self._check_sync_files()
        
        # Check 3: Verify checksums match
        self._check_checksums()
        
        # Check 4: Verify no manual edits
        self._check_manual_edits()
        
        # Check 5: Verify manifest completeness
        self._check_manifest()
        
        # Check 6: Verify GitHub compatibility
        self._check_github_compatibility()
        
        return self.results
    
    def _add_check(self, name: str, passed: bool, message: str):
        """Add a validation check result."""
        self.results['checks'].append({
            'name': name,
            'passed': passed,
            'message': message
        })
        if not passed:
            self.results['valid'] = False
    
    def _add_error(self, error: str):
        """Add an error."""
        self.results['errors'].append(error)
        self.results['valid'] = False
    
    def _add_warning(self, warning: str):
        """Add a warning."""
        self.results['warnings'].append(warning)
    
    def _check_fcm_coverage(self):
        """Check that all FCMs have corresponding generated actions."""
        print("Checking FCM coverage...")
        
        fcm_files = []
        for domain_dir in self.axioms_dir.iterdir():
            if domain_dir.is_dir():
                fcm_files.extend(domain_dir.glob('*.fcm'))
        
        missing_actions = []
        for fcm_path in fcm_files:
            rel_fcm = str(fcm_path.relative_to(self.project_root))
            if rel_fcm not in self.manifest['mappings']:
                missing_actions.append(rel_fcm)
        
        if missing_actions:
            self._add_check(
                'FCM Coverage',
                False,
                f"Missing actions for FCMs: {', '.join(missing_actions)}"
            )
        else:
            self._add_check(
                'FCM Coverage',
                True,
                f"All {len(fcm_files)} FCMs have generated actions"
            )
    
    def _check_sync_files(self):
        """Check that all generated actions have sync files."""
        print("Checking sync files...")
        
        action_dirs = []
        core_dir = self.actions_dir / 'core'
        if core_dir.exists():
            action_dirs.extend([d for d in core_dir.iterdir() if d.is_dir()])
        
        missing_sync = []
        for action_dir in action_dirs:
            sync_file = action_dir / '.bridge-sync'
            if not sync_file.exists():
                missing_sync.append(str(action_dir.relative_to(self.project_root)))
        
        if missing_sync:
            self._add_check(
                'Sync Files',
                False,
                f"Missing sync files in: {', '.join(missing_sync)}"
            )
        else:
            self._add_check(
                'Sync Files',
                True,
                f"All {len(action_dirs)} actions have sync files"
            )
    
    def _check_checksums(self):
        """Verify that FCM checksums match sync files."""
        print("Checking checksums...")
        
        mismatches = []
        for fcm_path, action_path in self.manifest['mappings'].items():
            fcm_full_path = self.project_root / fcm_path
            action_full_path = self.project_root / action_path
            sync_file = action_full_path / '.bridge-sync'
            
            if fcm_full_path.exists() and sync_file.exists():
                # Calculate current checksum
                with open(fcm_full_path, 'rb') as f:
                    current_checksum = f"sha256:{hashlib.sha256(f.read()).hexdigest()}"
                
                # Load stored checksum
                with open(sync_file, 'r') as f:
                    sync_data = json.load(f)
                    stored_checksum = sync_data.get('checksum', '')
                
                if current_checksum != stored_checksum:
                    mismatches.append(fcm_path)
        
        if mismatches:
            self._add_check(
                'Checksum Validation',
                False,
                f"Checksum mismatches for: {', '.join(mismatches)}"
            )
            self._add_warning("FCMs have been modified without regenerating actions")
        else:
            self._add_check(
                'Checksum Validation',
                True,
                "All checksums match"
            )
    
    def _check_manual_edits(self):
        """Check for manual edits in generated files."""
        print("Checking for manual edits...")
        
        manual_edit_indicators = []
        
        for _, action_path in self.manifest['mappings'].items():
            action_yml_path = self.project_root / action_path / 'action.yml'
            
            if action_yml_path.exists():
                with open(action_yml_path, 'r') as f:
                    content = f.read()
                
                # Check for generation header
                if '# Generated from' not in content:
                    manual_edit_indicators.append(str(action_yml_path.relative_to(self.project_root)))
                elif '# DO NOT EDIT' not in content:
                    manual_edit_indicators.append(str(action_yml_path.relative_to(self.project_root)))
        
        if manual_edit_indicators:
            self._add_check(
                'Manual Edit Detection',
                False,
                f"Possible manual edits in: {', '.join(manual_edit_indicators)}"
            )
        else:
            self._add_check(
                'Manual Edit Detection',
                True,
                "No manual edits detected"
            )
    
    def _check_manifest(self):
        """Check manifest completeness."""
        print("Checking manifest...")
        
        issues = []
        
        # Check that all mappings have generation info
        for fcm_path, action_path in self.manifest['mappings'].items():
            if action_path not in self.manifest['generated']:
                issues.append(f"Missing generation info for {action_path}")
        
        if issues:
            self._add_check(
                'Manifest Completeness',
                False,
                f"Manifest issues: {'; '.join(issues)}"
            )
        else:
            self._add_check(
                'Manifest Completeness',
                True,
                "Manifest is complete and consistent"
            )
    
    def _check_github_compatibility(self):
        """Check that generated actions are GitHub-compatible."""
        print("Checking GitHub compatibility...")
        
        compatibility_issues = []
        
        for _, action_path in self.manifest['mappings'].items():
            action_yml_path = self.project_root / action_path / 'action.yml'
            
            if action_yml_path.exists():
                try:
                    with open(action_yml_path, 'r') as f:
                        # Skip header comments
                        lines = f.readlines()
                        yaml_content = ''
                        for line in lines:
                            if not line.strip().startswith('#'):
                                yaml_content += line
                        
                        action_config = yaml.safe_load(yaml_content)
                    
                    # Check required fields
                    if 'name' not in action_config:
                        compatibility_issues.append(f"{action_yml_path}: missing 'name'")
                    if 'runs' not in action_config:
                        compatibility_issues.append(f"{action_yml_path}: missing 'runs'")
                    if 'runs' in action_config and 'using' not in action_config['runs']:
                        compatibility_issues.append(f"{action_yml_path}: missing 'runs.using'")
                
                except Exception as e:
                    compatibility_issues.append(f"{action_yml_path}: {e}")
        
        if compatibility_issues:
            self._add_check(
                'GitHub Compatibility',
                False,
                f"Issues found: {'; '.join(compatibility_issues)}"
            )
        else:
            self._add_check(
                'GitHub Compatibility',
                True,
                "All actions are GitHub-compatible"
            )
    
    def generate_report(self) -> str:
        """Generate validation report."""
        report = []
        report.append("=== Bridge Validation Report ===")
        report.append(f"Generated: {datetime.utcnow().isoformat()}Z")
        report.append(f"Overall Status: {'VALID' if self.results['valid'] else 'INVALID'}")
        report.append("")
        
        report.append("Validation Checks:")
        for check in self.results['checks']:
            status = "✓" if check['passed'] else "✗"
            report.append(f"  {status} {check['name']}: {check['message']}")
        
        if self.results['errors']:
            report.append("")
            report.append("Errors:")
            for error in self.results['errors']:
                report.append(f"  - {error}")
        
        if self.results['warnings']:
            report.append("")
            report.append("Warnings:")
            for warning in self.results['warnings']:
                report.append(f"  - {warning}")
        
        report.append("")
        report.append("Summary:")
        report.append(f"  Total Checks: {len(self.results['checks'])}")
        report.append(f"  Passed: {sum(1 for c in self.results['checks'] if c['passed'])}")
        report.append(f"  Failed: {sum(1 for c in self.results['checks'] if not c['passed'])}")
        report.append(f"  Errors: {len(self.results['errors'])}")
        report.append(f"  Warnings: {len(self.results['warnings'])}")
        
        return '\n'.join(report)

def main():
    """Main entry point."""
    validator = BridgeValidator()
    results = validator.validate_all()
    
    # Generate and print report
    report = validator.generate_report()
    print()
    print(report)
    
    # Save report
    report_path = Path('.bridge/validation-report.txt')
    with open(report_path, 'w') as f:
        f.write(report)
    
    print(f"\nReport saved to: {report_path}")
    
    # Exit with appropriate code
    return 0 if results['valid'] else 1

if __name__ == '__main__':
    exit(main())