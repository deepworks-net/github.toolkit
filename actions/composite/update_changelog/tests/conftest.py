import os
import pytest
import subprocess
from unittest.mock import MagicMock, patch


@pytest.fixture
def mock_subprocess():
    """Mock subprocess for compatibility."""
    with patch('subprocess.check_call') as mock_check_call, \
         patch('subprocess.check_output') as mock_check_output, \
         patch('subprocess.run') as mock_run:
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
    """Set environment variables expected by the action."""
    env_vars = {
        'GITHUB_REPOSITORY': 'test-org/test-repo',
        'GITHUB_TOKEN': 'mock-token',
        'GITHUB_WORKSPACE': '/github/workspace',
        'GITHUB_OUTPUT': '/tmp/github_output'
    }
    original = os.environ.copy()
    for k, v in env_vars.items():
        os.environ[k] = v
    with open(env_vars['GITHUB_OUTPUT'], 'w') as fh:
        fh.write('')
    yield env_vars
    os.environ.clear()
    os.environ.update(original)
    if os.path.exists(env_vars['GITHUB_OUTPUT']):
        os.remove(env_vars['GITHUB_OUTPUT'])
