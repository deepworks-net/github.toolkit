#!/usr/bin/env python3

import os
import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing file operations."""
    temp_path = tempfile.mkdtemp()
    yield temp_path
    # Cleanup
    shutil.rmtree(temp_path, ignore_errors=True)


@pytest.fixture
def mock_github_env(temp_dir):
    """Mock GitHub Actions environment variables."""
    github_output = os.path.join(temp_dir, 'github_output')
    
    env_vars = {
        'GITHUB_WORKSPACE': temp_dir,
        'GITHUB_OUTPUT': github_output
    }
    
    # Create empty GITHUB_OUTPUT file
    Path(github_output).touch()
    
    original_environ = os.environ.copy()
    
    # Set environment variables for testing
    for key, value in env_vars.items():
        os.environ[key] = value
    
    yield env_vars
    
    # Restore original environment
    os.environ.clear()
    os.environ.update(original_environ)


@pytest.fixture
def sample_files(temp_dir):
    """Create sample files for testing."""
    files = {}
    
    # Create a text file
    text_file = Path(temp_dir) / 'sample.txt'
    text_file.write_text('Hello, World!')
    files['text_file'] = str(text_file)
    
    # Create a JSON file
    json_file = Path(temp_dir) / 'data.json'
    json_file.write_text('{"key": "value"}')
    files['json_file'] = str(json_file)
    
    # Create a subdirectory with a file
    subdir = Path(temp_dir) / 'subdir'
    subdir.mkdir()
    sub_file = subdir / 'nested.txt'
    sub_file.write_text('Nested content')
    files['sub_file'] = str(sub_file)
    files['subdir'] = str(subdir)
    
    return files


@pytest.fixture
def file_operation_inputs():
    """Provide sample inputs for file operations."""
    return {
        'create': {
            'action': 'create',
            'file_path': 'test_create.txt',
            'content': 'Test content',
            'encoding': 'utf-8',
            'create_dirs': 'true',
            'overwrite': 'false'
        },
        'read': {
            'action': 'read',
            'file_path': 'test_file.txt',
            'encoding': 'utf-8'
        },
        'search': {
            'action': 'search',
            'pattern': '*.txt'
        }
    }