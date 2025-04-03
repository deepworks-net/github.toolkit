#!/usr/bin/env python3

import os
import pytest
import subprocess
from unittest.mock import MagicMock, patch


@pytest.fixture
def mock_subprocess():
    """Mock subprocess for testing without executing shell commands."""
    with patch('subprocess.check_call') as mock_check_call, \
         patch('subprocess.check_output') as mock_check_output, \
         patch('subprocess.run') as mock_run:
        
        # Configure default successful behavior
        mock_check_call.return_value = 0
        mock_check_output.return_value = "mocked output"
        
        mock_run_instance = MagicMock()
        mock_run_instance.stdout = "mocked stdout"
        mock_run_instance.stderr = ""
        mock_run_instance.returncode = 0
        mock_run.return_value = mock_run_instance
        
        yield {
            'check_call': mock_check_call,
            'check_output': mock_check_output,
            'run': mock_run
        }


@pytest.fixture
def mock_git_env():
    """Mock environment variables for git operations."""
    env_vars = {
        'GITHUB_REPOSITORY': 'test-org/test-repo',
        'GITHUB_TOKEN': 'mock-token',
        'GITHUB_WORKSPACE': '/github/workspace',
        'GITHUB_OUTPUT': '/tmp/github_output'
    }
    
    original_environ = os.environ.copy()
    
    # Set environment variables for testing
    for key, value in env_vars.items():
        os.environ[key] = value
    
    # Create GITHUB_OUTPUT file
    with open(env_vars['GITHUB_OUTPUT'], 'w') as f:
        f.write('')
    
    yield env_vars
    
    # Restore original environment
    os.environ.clear()
    os.environ.update(original_environ)
    
    # Clean up GITHUB_OUTPUT file
    if os.path.exists(env_vars['GITHUB_OUTPUT']):
        os.remove(env_vars['GITHUB_OUTPUT'])


@pytest.fixture
def branch_outputs():
    """Provide sample git branch command outputs for testing."""
    return {
        'show_current': "feature/test-branch",
        'list_local': "* main\n  develop\n  feature/test-branch",
        'list_remote': "* main\n  develop\n  feature/test-branch\n  remotes/origin/main\n  remotes/origin/develop",
        'list_pattern': "  feature/test-branch\n  feature/another-branch"
    }