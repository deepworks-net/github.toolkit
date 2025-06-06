#!/usr/bin/env python3
"""
Unit tests for FCM to Action Generator
Tests the generation of GitHub Actions from FCM definitions.
"""

import unittest
import tempfile
import yaml
import json
from pathlib import Path
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

try:
    from generator import FCMToActionBridge, FCMParser
except ImportError:
    # Create mock classes for testing without Python available
    class FCMParser:
        def __init__(self, fcm_path):
            self.parsed = {
                'metadata': {'model': 'test.minimal', 'version': '1.0.0', 'domain': 'test'},
                'capability': 'Test action',
                'parameters': [{'name': 'message', 'type': 'string', 'required': True}],
                'outputs': [{'name': 'result'}],
                'interface': {'type': 'docker', 'image': 'python:3.9-slim'}
            }
    
    class FCMToActionBridge:
        def __init__(self, project_root=Path('.')):
            self.project_root = project_root
            
        def generate_action_yml(self, fcm_path):
            return Path('test-action.yml')

class TestFCMToActionBridge(unittest.TestCase):
    """Test FCM to GitHub Action generation."""
    
    def setUp(self):
        """Set up test environment."""
        # Create temporary directory structure
        self.temp_dir = Path(tempfile.mkdtemp())
        self.axioms_dir = self.temp_dir / 'axioms' / 'test'
        self.actions_dir = self.temp_dir / 'actions' / 'core'
        self.bridge_dir = self.temp_dir / '.bridge'
        
        # Create directories
        self.axioms_dir.mkdir(parents=True)
        self.actions_dir.mkdir(parents=True)
        self.bridge_dir.mkdir(parents=True)
        
        # Create test FCM
        self.test_fcm = self.axioms_dir / 'test-action.fcm'
        self.test_fcm.write_text("""Model: test.action
Version: 1.0.0
Layer: Axiom
Domain: test

Capability: Test action for validation

Parameters:
  - message: string
  - count: number (optional)
  - action: create|delete

Outputs:
  - result
  - status

Interface:
  type: docker
  image: python:3.9-slim
  requirements: []
""")
        
        # Initialize bridge
        self.bridge = FCMToActionBridge(self.temp_dir)
    
    def tearDown(self):
        """Clean up test environment."""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_bridge_initialization(self):
        """Test bridge initializes correctly."""
        self.assertEqual(self.bridge.project_root, self.temp_dir)
        self.assertEqual(self.bridge.axioms_dir, self.temp_dir / 'axioms')
        self.assertEqual(self.bridge.actions_dir, self.temp_dir / 'actions')
    
    def test_action_yml_generation(self):
        """Test generation of action.yml from FCM."""
        # Generate action
        action_path = self.bridge.generate_action_yml(self.test_fcm)
        
        # Verify file was created
        self.assertTrue(action_path.exists())
        
        # Load and verify content
        with open(action_path, 'r') as f:
            content = f.read()
        
        # Should contain generation header
        self.assertIn('# Generated from', content)
        self.assertIn('# DO NOT EDIT', content)
        
        # Parse YAML content (skip header comments)
        yaml_lines = []
        for line in content.split('\n'):
            if not line.strip().startswith('#'):
                yaml_lines.append(line)
        
        action_config = yaml.safe_load('\n'.join(yaml_lines))
        
        # Verify basic structure
        self.assertIn('name', action_config)
        self.assertIn('description', action_config)
        self.assertIn('inputs', action_config)
        self.assertIn('outputs', action_config)
        self.assertIn('runs', action_config)
        
        # Verify content
        self.assertEqual(action_config['name'], 'Test Action')
        self.assertEqual(action_config['description'], 'Test action for validation')
        
        # Verify inputs
        inputs = action_config['inputs']
        self.assertIn('message', inputs)
        self.assertIn('count', inputs)
        self.assertIn('action', inputs)
        
        # Required parameter
        self.assertTrue(inputs['message']['required'])
        
        # Optional parameter should have default
        self.assertFalse(inputs['count']['required'])
        self.assertEqual(inputs['count']['default'], '')
        
        # Choice parameter should have description with options
        self.assertIn('create, delete', inputs['action']['description'])
        
        # Verify outputs
        outputs = action_config['outputs']
        self.assertIn('result', outputs)
        self.assertIn('status', outputs)
        
        # Verify runs configuration
        runs = action_config['runs']
        self.assertEqual(runs['using'], 'docker')
        self.assertEqual(runs['image'], 'Dockerfile')
    
    def test_dockerfile_generation(self):
        """Test generation of Dockerfile."""
        # Generate action (includes Dockerfile)
        action_path = self.bridge.generate_action_yml(self.test_fcm)
        dockerfile_path = action_path.parent / 'Dockerfile'
        
        # Verify Dockerfile was created
        self.assertTrue(dockerfile_path.exists())
        
        # Verify content
        dockerfile_content = dockerfile_path.read_text()
        
        self.assertIn('# Generated from FCM - DO NOT EDIT', dockerfile_content)
        self.assertIn('FROM python:3.9-slim', dockerfile_content)
        self.assertIn('COPY entrypoint.sh /entrypoint.sh', dockerfile_content)
        self.assertIn('ENTRYPOINT ["/entrypoint.sh"]', dockerfile_content)
    
    def test_entrypoint_generation(self):
        """Test generation of entrypoint script."""
        # Generate action (includes entrypoint)
        action_path = self.bridge.generate_action_yml(self.test_fcm)
        entrypoint_path = action_path.parent / 'entrypoint.sh'
        
        # Verify entrypoint was created
        self.assertTrue(entrypoint_path.exists())
        
        # Verify it's executable
        import stat
        mode = entrypoint_path.stat().st_mode
        self.assertTrue(mode & stat.S_IEXEC)
        
        # Verify content
        entrypoint_content = entrypoint_path.read_text()
        
        self.assertIn('#!/bin/bash', entrypoint_content)
        self.assertIn('Action: test-action', entrypoint_content)
        self.assertIn('Generated placeholder', entrypoint_content)
        self.assertIn('github.com/deepworks-net/test-action-action', entrypoint_content)
    
    def test_sync_file_generation(self):
        """Test generation of bridge sync metadata."""
        # Generate action (includes sync file)
        action_path = self.bridge.generate_action_yml(self.test_fcm)
        sync_path = action_path.parent / '.bridge-sync'
        
        # Verify sync file was created
        self.assertTrue(sync_path.exists())
        
        # Verify content
        with open(sync_path, 'r') as f:
            sync_data = json.load(f)
        
        self.assertIn('source', sync_data)
        self.assertIn('generated', sync_data)
        self.assertIn('version', sync_data)
        self.assertIn('checksum', sync_data)
        
        # Verify source path is relative
        source_path = sync_data['source']
        self.assertTrue(source_path.startswith('axioms/'))
        
        # Verify checksum format
        checksum = sync_data['checksum']
        self.assertTrue(checksum.startswith('sha256:'))
    
    def test_manifest_update(self):
        """Test manifest is updated after generation."""
        # Generate action
        action_path = self.bridge.generate_action_yml(self.test_fcm)
        
        # Load manifest
        manifest_path = self.bridge_dir / 'manifest.json'
        self.assertTrue(manifest_path.exists())
        
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
        
        # Verify mapping was added
        fcm_rel_path = str(self.test_fcm.relative_to(self.temp_dir))
        action_rel_path = str(action_path.parent.relative_to(self.temp_dir))
        
        self.assertIn(fcm_rel_path, manifest['mappings'])
        self.assertEqual(manifest['mappings'][fcm_rel_path], action_rel_path)
        
        # Verify generation info was added
        self.assertIn(action_rel_path, manifest['generated'])
        gen_info = manifest['generated'][action_rel_path]
        
        self.assertEqual(gen_info['source'], fcm_rel_path)
        self.assertIn('timestamp', gen_info)
        self.assertIn('model_version', gen_info)
    
    def test_domain_inference(self):
        """Test correct domain inference from action name."""
        test_cases = [
            ('branch-operations', 'git'),
            ('tag-operations', 'git'),
            ('commit-operations', 'git'),
            ('version-calculator', 'version'),
            ('version-updater', 'version'),
            ('release-notes', 'release'),
            ('update-changelog', 'release'),
            ('some-action', 'github')  # fallback
        ]
        
        for action_name, expected_domain in test_cases:
            domain = self.bridge._determine_domain(action_name)
            self.assertEqual(domain, expected_domain, 
                           f"Expected domain {expected_domain} for {action_name}, got {domain}")
    
    def test_parameter_type_handling(self):
        """Test different parameter types are handled correctly."""
        # Create FCM with various parameter types
        fcm_content = """Model: test.types
Capability: Test parameter types

Parameters:
  - string_param: string
  - choice_param: option1|option2|option3
  - boolean_param: boolean
  - optional_param: string (optional)
  - number_param: number

Outputs:
  - result

Interface:
  type: docker
  image: python:3.9-slim
"""
        
        fcm_path = self.axioms_dir / 'type-test.fcm'
        fcm_path.write_text(fcm_content)
        
        # Generate action
        action_path = self.bridge.generate_action_yml(fcm_path)
        
        # Load generated action
        with open(action_path, 'r') as f:
            content = f.read()
        
        # Parse YAML (skip header)
        yaml_lines = [line for line in content.split('\n') if not line.strip().startswith('#')]
        action_config = yaml.safe_load('\n'.join(yaml_lines))
        
        inputs = action_config['inputs']
        
        # Required string parameter
        self.assertTrue(inputs['string_param']['required'])
        
        # Choice parameter should have options in description
        self.assertIn('option1, option2, option3', inputs['choice_param']['description'])
        
        # Optional parameter should not be required and have default
        self.assertFalse(inputs['optional_param']['required'])
        self.assertEqual(inputs['optional_param']['default'], '')

class TestErrorHandling(unittest.TestCase):
    """Test error handling in bridge generation."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.bridge = FCMToActionBridge(self.temp_dir)
    
    def tearDown(self):
        """Clean up."""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_missing_fcm_file(self):
        """Test handling of missing FCM file."""
        missing_fcm = self.temp_dir / 'missing.fcm'
        
        with self.assertRaises(FileNotFoundError):
            self.bridge.generate_action_yml(missing_fcm)
    
    def test_invalid_fcm_format(self):
        """Test handling of invalid FCM format."""
        # Create invalid FCM
        invalid_fcm = self.temp_dir / 'invalid.fcm'
        invalid_fcm.write_text("This is not a valid FCM format")
        
        # Should handle gracefully (parser might have defaults)
        try:
            result = self.bridge.generate_action_yml(invalid_fcm)
            # If it doesn't raise an exception, verify it creates some output
            self.assertIsInstance(result, Path)
        except Exception as e:
            # If it does raise an exception, it should be informative
            self.assertIn('FCM', str(e).upper())

if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)