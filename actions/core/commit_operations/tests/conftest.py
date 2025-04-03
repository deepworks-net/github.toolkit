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
        
        # Set up different responses based on the command
        def mock_check_output_side_effect(*args, **kwargs):
            if args[0][0:2] == ['git', 'config'] and args[0][2] == 'user.name':
                # Simulate user.name not configured
                raise subprocess.CalledProcessError(128, 'git config user.name')
            return "mocked output"
            
        # mock_check_output.side_effect = mock_check_output_side_effect
        
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
def commit_outputs():
    """Provide sample commit outputs for testing."""
    return {
        'git_version': b"git version 2.30.0",
        'commit_create': "0123456789abcdef0123456789abcdef01234567",
        'commit_amend': "fedcba9876543210fedcba9876543210fedcba98",
        'list_commits': "abc1234 - Add feature 1 (John Doe, 2023-04-01)\n"
                        "def5678 - Fix bug in code (Jane Smith, 2023-03-30)\n"
                        "ghi9012 - Update documentation (John Doe, 2023-03-29)",
        'list_commits_author': "abc1234 - Add feature 1 (John Doe, 2023-04-01)\n"
                                "ghi9012 - Update documentation (John Doe, 2023-03-29)",
        'list_commits_oneline': "abc1234 Add feature 1\n"
                                "def5678 Fix bug in code\n"
                                "ghi9012 Update documentation",
        'get_commit_info': "commit abc1234def5678ghi9012jkl3456mno7890pqr1234\n"
                            "Author: John Doe <john@example.com>\n"
                            "Date:   Sat Apr 1 12:34:56 2023 +0000\n\n"
                            "    Add feature 1\n\n"
                            "    This is a detailed description of the feature.",
        'get_commit_hash': "abc1234def5678ghi9012jkl3456mno7890pqr1234",
        'get_commit_author': "John Doe",
        'get_commit_date': "1617286496",  # Unix timestamp for 2023-04-01 12:34:56
        'get_commit_message': "Add feature 1",
        'cherry_pick_success': "",
        'cherry_pick_conflict': "error: could not apply abc1234... Add feature 1",
        'revert_success': "0123456789abcdef0123456789abcdef01234567",
        'revert_conflict': "error: could not revert abc1234... Add feature 1"
    }