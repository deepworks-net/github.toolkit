#!/usr/bin/env python3
"""
Bridge Test Harness
Orchestrates comprehensive testing of the FCM-to-GitHub bridge system.
"""

import os
import sys
import json
import yaml
import subprocess
import tempfile
import shutil
from pathlib import Path
from datetime import datetime
import hashlib

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

try:
    from generator import FCMToActionBridge, FCMParser
    from validator import BridgeValidator
    PYTHON_AVAILABLE = True
except ImportError:
    PYTHON_AVAILABLE = False
    print("Warning: Python implementation not available, using shell-based testing")

class BridgeTestHarness:
    """Comprehensive test harness for FCM bridge system."""
    
    def __init__(self, project_root=None):
        self.project_root = Path(project_root) if project_root else Path('.')
        self.test_results = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'tests': [],
            'summary': {
                'total': 0,
                'passed': 0,
                'failed': 0,
                'skipped': 0
            }
        }
        
        # Initialize components if Python is available
        if PYTHON_AVAILABLE:
            self.bridge = FCMToActionBridge(self.project_root)
            self.validator = BridgeValidator(self.project_root)
        else:
            self.bridge = None
            self.validator = None
    
    def log_test(self, name, status, message="", details=None):
        """Log a test result."""
        test_result = {
            'name': name,
            'status': status,  # 'passed', 'failed', 'skipped'
            'message': message,
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }
        if details:
            test_result['details'] = details
        
        self.test_results['tests'].append(test_result)
        self.test_results['summary']['total'] += 1
        self.test_results['summary'][status] += 1
        
        # Print immediate feedback
        status_icon = {'passed': '✓', 'failed': '✗', 'skipped': '○'}[status]
        print(f"  {status_icon} {name}: {message}")
    
    def run_unit_tests(self):
        """Run unit tests for individual components."""
        print("\n=== Running Unit Tests ===")
        
        if not PYTHON_AVAILABLE:
            self.log_test("Unit Tests", "skipped", "Python not available")
            return
        
        # Test FCM Parser
        try:
            test_fcm_path = self.project_root / '.bridge' / 'tests' / 'fixtures' / 'minimal.fcm'
            if test_fcm_path.exists():
                parser = FCMParser(test_fcm_path)
                if parser.parsed['metadata'].get('model') == 'test.minimal':
                    self.log_test("FCM Parser", "passed", "Successfully parsed test FCM")
                else:
                    self.log_test("FCM Parser", "failed", "FCM parsing returned unexpected results")
            else:
                self.log_test("FCM Parser", "failed", "Test FCM fixture not found")
        except Exception as e:
            self.log_test("FCM Parser", "failed", f"Parser error: {str(e)}")
        
        # Test Action Generator
        try:
            if test_fcm_path.exists():
                # Generate to temporary location
                temp_dir = Path(tempfile.mkdtemp())
                temp_bridge = FCMToActionBridge(temp_dir)
                
                # Create required directory structure
                (temp_dir / 'axioms' / 'test').mkdir(parents=True)
                (temp_dir / 'actions' / 'core').mkdir(parents=True)
                (temp_dir / '.bridge').mkdir()
                
                # Copy test FCM
                test_fcm_copy = temp_dir / 'axioms' / 'test' / 'minimal.fcm'
                shutil.copy2(test_fcm_path, test_fcm_copy)
                
                # Generate action
                action_path = temp_bridge.generate_action_yml(test_fcm_copy)
                
                if action_path.exists() and (action_path.parent / 'Dockerfile').exists():
                    self.log_test("Action Generator", "passed", "Successfully generated action structure")
                else:
                    self.log_test("Action Generator", "failed", "Generated action incomplete")
                
                # Clean up
                shutil.rmtree(temp_dir)
            else:
                self.log_test("Action Generator", "failed", "Test FCM fixture not found")
        except Exception as e:
            self.log_test("Action Generator", "failed", f"Generator error: {str(e)}")
    
    def run_integration_tests(self):
        """Run integration tests for component interaction."""
        print("\n=== Running Integration Tests ===")
        
        # Test complete FCM-to-Action cycle
        self.test_generation_cycle()
        
        # Test bridge validation
        self.test_bridge_validation()
        
        # Test existing action compatibility
        self.test_existing_action_parity()
    
    def test_generation_cycle(self):
        """Test complete FCM to action generation cycle."""
        try:
            test_fcm_path = self.project_root / '.bridge' / 'tests' / 'fixtures' / 'minimal.fcm'
            
            if not test_fcm_path.exists():
                self.log_test("Generation Cycle", "failed", "Test FCM not found")
                return
            
            if PYTHON_AVAILABLE and self.bridge:
                # Python-based test
                action_path = self.bridge.generate_action_yml(test_fcm_path)
                
                # Verify files were created
                required_files = ['action.yml', 'Dockerfile', 'entrypoint.sh', '.bridge-sync']
                missing_files = []
                
                for file_name in required_files:
                    if not (action_path.parent / file_name).exists():
                        missing_files.append(file_name)
                
                if missing_files:
                    self.log_test("Generation Cycle", "failed", 
                                f"Missing files: {', '.join(missing_files)}")
                else:
                    self.log_test("Generation Cycle", "passed", 
                                "Complete action structure generated")
            else:
                # Shell-based test
                result = subprocess.run([
                    'bash', str(self.project_root / '.bridge' / 'generate.sh'),
                    str(test_fcm_path)
                ], capture_output=True, text=True, cwd=self.project_root)
                
                if result.returncode == 0:
                    # Check if action was generated
                    expected_action = self.project_root / 'actions' / 'core' / 'minimal'
                    if expected_action.exists() and (expected_action / 'action.yml').exists():
                        self.log_test("Generation Cycle", "passed", 
                                    "Action generated via shell script")
                    else:
                        self.log_test("Generation Cycle", "failed", 
                                    "Shell generation did not create expected files")
                else:
                    self.log_test("Generation Cycle", "failed", 
                                f"Shell generation failed: {result.stderr}")
                    
        except Exception as e:
            self.log_test("Generation Cycle", "failed", f"Cycle test error: {str(e)}")
    
    def test_bridge_validation(self):
        """Test bridge validation functionality."""
        try:
            if PYTHON_AVAILABLE and self.validator:
                # Python-based validation
                results = self.validator.validate_all()
                
                if results['valid']:
                    self.log_test("Bridge Validation", "passed", 
                                f"All {len(results['checks'])} validation checks passed")
                else:
                    failed_checks = [c for c in results['checks'] if not c['passed']]
                    self.log_test("Bridge Validation", "failed", 
                                f"{len(failed_checks)} validation checks failed",
                                details={'failed_checks': [c['name'] for c in failed_checks]})
            else:
                # Shell-based validation
                result = subprocess.run([
                    'bash', str(self.project_root / '.bridge' / 'validate.sh')
                ], capture_output=True, text=True, cwd=self.project_root)
                
                if result.returncode == 0:
                    self.log_test("Bridge Validation", "passed", 
                                "Shell validation completed successfully")
                else:
                    self.log_test("Bridge Validation", "failed", 
                                f"Shell validation failed: {result.stderr}")
                    
        except Exception as e:
            self.log_test("Bridge Validation", "failed", f"Validation error: {str(e)}")
    
    def test_existing_action_parity(self):
        """Test that generated actions maintain parity with existing ones."""
        try:
            # Find existing tag-operations action
            existing_action = self.project_root / 'actions' / 'core' / 'tag_operations'
            generated_action = self.project_root / 'actions' / 'core' / 'tag-operations'
            
            if not existing_action.exists():
                self.log_test("Action Parity", "skipped", "Original tag_operations not found")
                return
            
            if not generated_action.exists():
                self.log_test("Action Parity", "failed", "Generated tag-operations not found")
                return
            
            # Compare action.yml files
            try:
                with open(existing_action / 'action.yml', 'r') as f:
                    existing_config = yaml.safe_load(f)
                
                with open(generated_action / 'action.yml', 'r') as f:
                    # Skip header comments for generated file
                    content = f.read()
                    yaml_content = '\n'.join(line for line in content.split('\n') 
                                           if not line.strip().startswith('#'))
                    generated_config = yaml.safe_load(yaml_content)
                
                # Compare key structures
                differences = []
                
                # Check inputs exist
                existing_inputs = set(existing_config.get('inputs', {}).keys())
                generated_inputs = set(generated_config.get('inputs', {}).keys())
                
                if existing_inputs - generated_inputs:
                    differences.append(f"Missing inputs: {existing_inputs - generated_inputs}")
                
                if generated_inputs - existing_inputs:
                    differences.append(f"Extra inputs: {generated_inputs - existing_inputs}")
                
                if differences:
                    self.log_test("Action Parity", "failed", 
                                f"Structure differences: {'; '.join(differences)}")
                else:
                    self.log_test("Action Parity", "passed", 
                                "Generated action structure matches existing")
                    
            except Exception as e:
                self.log_test("Action Parity", "failed", f"Comparison error: {str(e)}")
                
        except Exception as e:
            self.log_test("Action Parity", "failed", f"Parity test error: {str(e)}")
    
    def run_end_to_end_tests(self):
        """Run end-to-end tests with real GitHub Actions."""
        print("\n=== Running End-to-End Tests ===")
        
        # For now, just verify that generated actions have valid structure
        self.test_action_structure_validity()
    
    def test_action_structure_validity(self):
        """Test that generated actions have valid GitHub Action structure."""
        try:
            actions_dir = self.project_root / 'actions' / 'core'
            
            if not actions_dir.exists():
                self.log_test("Action Structure", "skipped", "No actions directory found")
                return
            
            valid_actions = 0
            invalid_actions = []
            
            for action_dir in actions_dir.iterdir():
                if not action_dir.is_dir():
                    continue
                
                action_yml = action_dir / 'action.yml'
                if not action_yml.exists():
                    invalid_actions.append(f"{action_dir.name}: no action.yml")
                    continue
                
                try:
                    with open(action_yml, 'r') as f:
                        content = f.read()
                    
                    # Skip header comments for parsing
                    yaml_content = '\n'.join(line for line in content.split('\n') 
                                           if not line.strip().startswith('#'))
                    
                    config = yaml.safe_load(yaml_content)
                    
                    # Check required fields
                    required_fields = ['name', 'runs']
                    missing_fields = [field for field in required_fields 
                                    if field not in config]
                    
                    if missing_fields:
                        invalid_actions.append(f"{action_dir.name}: missing {missing_fields}")
                    else:
                        valid_actions += 1
                        
                except Exception as e:
                    invalid_actions.append(f"{action_dir.name}: parse error - {str(e)}")
            
            if invalid_actions:
                self.log_test("Action Structure", "failed", 
                            f"{len(invalid_actions)} invalid actions",
                            details={'invalid_actions': invalid_actions})
            else:
                self.log_test("Action Structure", "passed", 
                            f"All {valid_actions} actions have valid structure")
                
        except Exception as e:
            self.log_test("Action Structure", "failed", f"Structure test error: {str(e)}")
    
    def run_purity_tests(self):
        """Run architectural purity tests."""
        print("\n=== Running Purity Tests ===")
        
        # Test 1: No hardcoded values in FCMs
        self.test_fcm_purity()
        
        # Test 2: All generated actions have sync files
        self.test_sync_file_presence()
        
        # Test 3: No manual edits in generated files
        self.test_manual_edit_detection()
    
    def test_fcm_purity(self):
        """Test that FCMs contain no hardcoded operational values."""
        try:
            violations = []
            axioms_dir = self.project_root / 'axioms'
            
            if not axioms_dir.exists():
                self.log_test("FCM Purity", "skipped", "No axioms directory found")
                return
            
            for fcm_file in axioms_dir.rglob('*.fcm'):
                content = fcm_file.read_text()
                
                # Check for version numbers (should be parameterized)
                import re
                version_matches = re.findall(r'\b\d+\.\d+\.\d+\b', content)
                for match in version_matches:
                    violations.append(f"{fcm_file.name}: hardcoded version {match}")
                
                # Check for absolute paths
                path_matches = re.findall(r'/[a-zA-Z0-9_/-]+', content)
                for match in path_matches:
                    if not match.startswith('/usr/') and not match.startswith('/bin/'):
                        violations.append(f"{fcm_file.name}: hardcoded path {match}")
            
            if violations:
                self.log_test("FCM Purity", "failed", 
                            f"{len(violations)} purity violations",
                            details={'violations': violations})
            else:
                self.log_test("FCM Purity", "passed", "No purity violations found in FCMs")
                
        except Exception as e:
            self.log_test("FCM Purity", "failed", f"Purity test error: {str(e)}")
    
    def test_sync_file_presence(self):
        """Test that all generated actions have sync files."""
        try:
            actions_dir = self.project_root / 'actions' / 'core'
            
            if not actions_dir.exists():
                self.log_test("Sync Files", "skipped", "No actions directory found")
                return
            
            missing_sync = []
            
            for action_dir in actions_dir.iterdir():
                if action_dir.is_dir():
                    sync_file = action_dir / '.bridge-sync'
                    if not sync_file.exists():
                        missing_sync.append(action_dir.name)
            
            if missing_sync:
                self.log_test("Sync Files", "failed", 
                            f"Missing sync files: {', '.join(missing_sync)}")
            else:
                total_actions = len([d for d in actions_dir.iterdir() if d.is_dir()])
                self.log_test("Sync Files", "passed", 
                            f"All {total_actions} actions have sync files")
                
        except Exception as e:
            self.log_test("Sync Files", "failed", f"Sync test error: {str(e)}")
    
    def test_manual_edit_detection(self):
        """Test detection of manual edits in generated files."""
        try:
            manual_edits = []
            actions_dir = self.project_root / 'actions' / 'core'
            
            if not actions_dir.exists():
                self.log_test("Manual Edits", "skipped", "No actions directory found")
                return
            
            for action_dir in actions_dir.iterdir():
                if not action_dir.is_dir():
                    continue
                
                action_yml = action_dir / 'action.yml'
                if action_yml.exists():
                    content = action_yml.read_text()
                    
                    # Check for generation markers
                    if '# Generated from' not in content:
                        manual_edits.append(f"{action_dir.name}: missing generation header")
                    elif '# DO NOT EDIT' not in content:
                        manual_edits.append(f"{action_dir.name}: missing edit warning")
            
            if manual_edits:
                self.log_test("Manual Edits", "failed", 
                            f"Possible manual edits: {', '.join(manual_edits)}")
            else:
                self.log_test("Manual Edits", "passed", "No manual edits detected")
                
        except Exception as e:
            self.log_test("Manual Edits", "failed", f"Edit detection error: {str(e)}")
    
    def run_all_tests(self):
        """Run complete test suite."""
        print("=== Bridge Test Harness ===")
        print(f"Timestamp: {self.test_results['timestamp']}")
        print(f"Project Root: {self.project_root}")
        print(f"Python Available: {PYTHON_AVAILABLE}")
        
        # Run all test categories
        self.run_unit_tests()
        self.run_integration_tests()
        self.run_end_to_end_tests()
        self.run_purity_tests()
        
        # Generate summary
        print(f"\n=== Test Summary ===")
        summary = self.test_results['summary']
        print(f"Total Tests: {summary['total']}")
        print(f"Passed: {summary['passed']}")
        print(f"Failed: {summary['failed']}")
        print(f"Skipped: {summary['skipped']}")
        
        success_rate = (summary['passed'] / summary['total'] * 100) if summary['total'] > 0 else 0
        print(f"Success Rate: {success_rate:.1f}%")
        
        # Save detailed results
        results_file = self.project_root / '.bridge' / 'test-results.json'
        with open(results_file, 'w') as f:
            json.dump(self.test_results, f, indent=2)
        
        print(f"\nDetailed results saved to: {results_file}")
        
        # Return exit code
        return 0 if summary['failed'] == 0 else 1

def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Bridge Test Harness')
    parser.add_argument('--project-root', default='.', help='Project root directory')
    parser.add_argument('--unit', action='store_true', help='Run only unit tests')
    parser.add_argument('--integration', action='store_true', help='Run only integration tests')
    parser.add_argument('--e2e', action='store_true', help='Run only end-to-end tests')
    parser.add_argument('--purity', action='store_true', help='Run only purity tests')
    parser.add_argument('--all', action='store_true', help='Run all tests (default)')
    
    args = parser.parse_args()
    
    # Default to all tests if no specific category selected
    if not any([args.unit, args.integration, args.e2e, args.purity]):
        args.all = True
    
    harness = BridgeTestHarness(args.project_root)
    
    if args.unit or args.all:
        harness.run_unit_tests()
    
    if args.integration or args.all:
        harness.run_integration_tests()
    
    if args.e2e or args.all:
        harness.run_end_to_end_tests()
    
    if args.purity or args.all:
        harness.run_purity_tests()
    
    if args.all:
        return harness.run_all_tests()
    else:
        # Generate summary for partial runs
        summary = harness.test_results['summary']
        print(f"\nPartial Test Summary: {summary['passed']}/{summary['total']} passed")
        return 0 if summary['failed'] == 0 else 1

if __name__ == '__main__':
    exit(main())