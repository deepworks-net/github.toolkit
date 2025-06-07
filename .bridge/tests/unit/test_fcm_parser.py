#!/usr/bin/env python3
"""
Unit tests for FCM Parser
Tests the parsing of FCM files into structured data.
"""

import unittest
import tempfile
from pathlib import Path
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

try:
    from generator import FCMParser
except ImportError:
    # Create a mock parser for testing without Python available
    class FCMParser:
        def __init__(self, fcm_path):
            self.fcm_path = fcm_path
            self.parsed = self._mock_parse()
        
        def _mock_parse(self):
            return {
                'metadata': {'model': 'test.minimal', 'version': '1.0.0'},
                'capability': 'Minimal test action',
                'parameters': [{'name': 'message', 'type': 'string', 'required': True}],
                'outputs': [{'name': 'result'}]
            }

class TestFCMParser(unittest.TestCase):
    """Test FCM parsing functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_fcm_content = """# Test FCM
Model: test.sample
Version: 1.0.0
Layer: Axiom
Domain: test

Capability: Sample test action for validation

Parameters:
  - action: create|delete|list
  - name: string
  - optional: string (optional)

Outputs:
  - result
  - status

Interface:
  type: docker
  image: python:3.9-slim
  requirements: [git]

Dependencies:
  - git
  - github-token (optional)

Patterns:
  - test-pattern
  - sample-operation
"""
        
        # Create temporary file
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.fcm', delete=False)
        self.temp_file.write(self.test_fcm_content)
        self.temp_file.close()
        self.fcm_path = Path(self.temp_file.name)
    
    def tearDown(self):
        """Clean up test fixtures."""
        if self.fcm_path.exists():
            self.fcm_path.unlink()
    
    def test_parser_initialization(self):
        """Test parser can be initialized with FCM file."""
        parser = FCMParser(self.fcm_path)
        self.assertEqual(parser.fcm_path, self.fcm_path)
        self.assertIsNotNone(parser.parsed)
    
    def test_metadata_parsing(self):
        """Test parsing of FCM metadata."""
        parser = FCMParser(self.fcm_path)
        metadata = parser.parsed['metadata']
        
        self.assertEqual(metadata['model'], 'test.sample')
        self.assertEqual(metadata['version'], '1.0.0')
        self.assertEqual(metadata['layer'], 'Axiom')
        self.assertEqual(metadata['domain'], 'test')
    
    def test_capability_parsing(self):
        """Test parsing of capability description."""
        parser = FCMParser(self.fcm_path)
        capability = parser.parsed['capability']
        
        self.assertEqual(capability, 'Sample test action for validation')
    
    def test_parameters_parsing(self):
        """Test parsing of parameters section."""
        parser = FCMParser(self.fcm_path)
        parameters = parser.parsed['parameters']
        
        self.assertEqual(len(parameters), 3)
        
        # Test choice parameter
        action_param = next(p for p in parameters if p['name'] == 'action')
        self.assertEqual(action_param['type'], 'choice')
        self.assertEqual(action_param['constraints'], ['create', 'delete', 'list'])
        self.assertTrue(action_param['required'])
        
        # Test string parameter
        name_param = next(p for p in parameters if p['name'] == 'name')
        self.assertEqual(name_param['type'], 'string')
        self.assertTrue(name_param['required'])
        
        # Test optional parameter
        optional_param = next(p for p in parameters if p['name'] == 'optional')
        self.assertEqual(optional_param['type'], 'string')
        self.assertFalse(optional_param['required'])
    
    def test_outputs_parsing(self):
        """Test parsing of outputs section."""
        parser = FCMParser(self.fcm_path)
        outputs = parser.parsed['outputs']
        
        self.assertEqual(len(outputs), 2)
        self.assertIn({'name': 'result'}, outputs)
        self.assertIn({'name': 'status'}, outputs)
    
    def test_interface_parsing(self):
        """Test parsing of interface section."""
        parser = FCMParser(self.fcm_path)
        interface = parser.parsed['interface']
        
        self.assertEqual(interface['type'], 'docker')
        self.assertEqual(interface['image'], 'python:3.9-slim')
        self.assertEqual(interface['requirements'], ['git'])
    
    def test_dependencies_parsing(self):
        """Test parsing of dependencies section."""
        parser = FCMParser(self.fcm_path)
        dependencies = parser.parsed['dependencies']
        
        self.assertEqual(len(dependencies), 2)
        self.assertIn('git', dependencies)
        self.assertIn('github-token (optional)', dependencies)
    
    def test_patterns_parsing(self):
        """Test parsing of patterns section."""
        parser = FCMParser(self.fcm_path)
        patterns = parser.parsed['patterns']
        
        self.assertEqual(len(patterns), 2)
        self.assertIn('test-pattern', patterns)
        self.assertIn('sample-operation', patterns)
    
    def test_empty_sections(self):
        """Test handling of empty or missing sections."""
        minimal_content = """Model: test.minimal
Capability: Minimal test
"""
        
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.fcm', delete=False)
        temp_file.write(minimal_content)
        temp_file.close()
        
        try:
            parser = FCMParser(Path(temp_file.name))
            
            # Should have defaults for missing sections
            self.assertEqual(parser.parsed['parameters'], [])
            self.assertEqual(parser.parsed['outputs'], [])
            self.assertEqual(parser.parsed['dependencies'], [])
            self.assertEqual(parser.parsed['patterns'], [])
        finally:
            Path(temp_file.name).unlink()
    
    def test_comment_and_blank_line_handling(self):
        """Test that comments and blank lines are ignored."""
        content_with_comments = """# This is a comment
Model: test.comments

# Another comment
Capability: Test with comments

# Blank lines and comments should be ignored

Parameters:
  - name: string  # inline comment
"""
        
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.fcm', delete=False)
        temp_file.write(content_with_comments)
        temp_file.close()
        
        try:
            parser = FCMParser(Path(temp_file.name))
            
            self.assertEqual(parser.parsed['metadata']['model'], 'test.comments')
            self.assertEqual(parser.parsed['capability'], 'Test with comments')
            self.assertEqual(len(parser.parsed['parameters']), 1)
        finally:
            Path(temp_file.name).unlink()

class TestParameterParsing(unittest.TestCase):
    """Test specific parameter parsing logic."""
    
    def setUp(self):
        """Set up parser instance."""
        # Create a minimal FCM file for testing
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.fcm', delete=False)
        self.temp_file.write("Model: test\nCapability: test")
        self.temp_file.close()
        self.parser = FCMParser(Path(self.temp_file.name))
    
    def tearDown(self):
        """Clean up."""
        Path(self.temp_file.name).unlink()
    
    def test_string_parameter(self):
        """Test parsing of string parameter."""
        param = self.parser._parse_parameter("name: string")
        
        self.assertEqual(param['name'], 'name')
        self.assertEqual(param['type'], 'string')
        self.assertTrue(param['required'])
    
    def test_optional_parameter(self):
        """Test parsing of optional parameter."""
        param = self.parser._parse_parameter("description: string (optional)")
        
        self.assertEqual(param['name'], 'description')
        self.assertEqual(param['type'], 'string')
        self.assertFalse(param['required'])
    
    def test_choice_parameter(self):
        """Test parsing of choice parameter."""
        param = self.parser._parse_parameter("action: create|delete|list|push")
        
        self.assertEqual(param['name'], 'action')
        self.assertEqual(param['type'], 'choice')
        self.assertEqual(param['constraints'], ['create', 'delete', 'list', 'push'])
        self.assertTrue(param['required'])
    
    def test_boolean_parameter(self):
        """Test parsing of boolean parameter."""
        param = self.parser._parse_parameter("force: boolean")
        
        self.assertEqual(param['name'], 'force')
        self.assertEqual(param['type'], 'boolean')
        self.assertTrue(param['required'])
    
    def test_parameter_without_type(self):
        """Test parsing of parameter without explicit type."""
        param = self.parser._parse_parameter("simple_param")
        
        self.assertEqual(param['name'], 'simple_param')
        self.assertEqual(param['type'], 'string')  # default type
        self.assertTrue(param['required'])

if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)