#!/usr/bin/env python3

import pytest
import os
import sys
import subprocess
from unittest.mock import patch, MagicMock

# Add parent directory to path to import module under test
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the module under test
from git_config import GitConfig


@pytest.fixture
def mock_subprocess():
    """Mock subprocess for testing without executing shell commands."""
    with patch('subprocess.check_call') as mock_check_call, \
         patch('subprocess.check_output') as mock_check_output:
        
        # Configure default successful behavior
        mock_check_call.return_value = 0
        mock_check_output.return_value = "mocked output"
        
        yield {
            'check_call': mock_check_call,
            'check_output': mock_check_output
        }


class TestGitConfig:
    """Unit tests for GitConfig class."""
    
    def test_init(self, mock_subprocess):
        """Test initialization and git availability check."""
        # Arrange & Act
        git_config = GitConfig()
        
        # Assert
        mock_subprocess['check_output'].assert_called_once_with(['git', '--version'], stderr=subprocess.STDOUT)
    
    def test_setup_identity(self, mock_subprocess):
        """Test setting up Git identity."""
        # Arrange
        git_config = GitConfig()
        
        # Act
        result = git_config.setup_identity("Test User", "test@example.com")
        
        # Assert
        assert result is True
        mock_subprocess['check_call'].assert_any_call(['git', 'config', '--global', 'user.name', 'Test User'])
        mock_subprocess['check_call'].assert_any_call(['git', 'config', '--global', 'user.email', 'test@example.com'])
    
    def test_setup_identity_defaults(self, mock_subprocess):
        """Test setting up Git identity with default values."""
        # Arrange
        git_config = GitConfig()
        
        # Configure check_output to raise an exception for user.name
        mock_subprocess['check_output'].side_effect = subprocess.CalledProcessError(1, "git config user.name")
        
        # Act
        result = git_config.setup_identity()
        
        # Assert
        assert result is True
        mock_subprocess['check_call'].assert_any_call(['git', 'config', '--global', 'user.name', 'GitHub Actions'])
        mock_subprocess['check_call'].assert_any_call(['git', 'config', '--global', 'user.email', 'github-actions@github.com'])
    
    def test_setup_identity_already_configured(self, mock_subprocess):
        """Test setting up Git identity when already configured."""
        # Arrange
        git_config = GitConfig()
        
        # Configure check_output to return existing values
        def side_effect(*args, **kwargs):
            if args[0] == ['git', '--version']:
                return "git version 2.30.0"
            elif args[0] == ['git', 'config', 'user.name']:
                return "Existing User"
            elif args[0] == ['git', 'config', 'user.email']:
                return "existing@example.com"
            return "mocked output"
        
        mock_subprocess['check_output'].side_effect = side_effect
        
        # Act
        result = git_config.setup_identity()
        
        # Assert
        assert result is True
        # Should not call check_call for user.name or user.email
        for call in mock_subprocess['check_call'].call_args_list:
            assert not (len(call[0]) > 0 and call[0][0] == ['git', 'config', '--global', 'user.name'])
            assert not (len(call[0]) > 0 and call[0][0] == ['git', 'config', '--global', 'user.email'])
    
    def test_configure_safe_directory(self, mock_subprocess):
        """Test configuring safe directory."""
        # Arrange
        git_config = GitConfig()
        
        # Act
        result = git_config.configure_safe_directory("/custom/path")
        
        # Assert
        assert result is True
        mock_subprocess['check_call'].assert_any_call(['git', 'config', '--global', '--add', 'safe.directory', '/custom/path'])
    
    def test_configure_safe_directory_default(self, mock_subprocess):
        """Test configuring safe directory with default path."""
        # Arrange
        git_config = GitConfig("/default/path")
        
        # Act
        result = git_config.configure_safe_directory()
        
        # Assert
        assert result is True
        mock_subprocess['check_call'].assert_any_call(['git', 'config', '--global', '--add', 'safe.directory', '/default/path'])
    
    def test_setup_github_token(self, mock_subprocess):
        """Test setting up GitHub token."""
        # Arrange
        git_config = GitConfig()
        os.environ['GITHUB_TOKEN'] = 'test-token'
        os.environ['GITHUB_REPOSITORY'] = 'test-org/test-repo'
        
        # Act
        result = git_config.setup_github_token()
        
        # Assert
        assert result is True
        mock_subprocess['check_call'].assert_any_call([
            'git', 'remote', 'set-url', 'origin', 
            'https://x-access-token:test-token@github.com/test-org/test-repo.git'
        ])
        
        # Clean up
        del os.environ['GITHUB_TOKEN']
        del os.environ['GITHUB_REPOSITORY']
    
    def test_setup_github_token_missing_env(self, mock_subprocess):
        """Test setting up GitHub token with missing environment variables."""
        # Arrange
        git_config = GitConfig()
        if 'GITHUB_TOKEN' in os.environ:
            del os.environ['GITHUB_TOKEN']
        if 'GITHUB_REPOSITORY' in os.environ:
            del os.environ['GITHUB_REPOSITORY']
        
        # Act
        result = git_config.setup_github_token()
        
        # Assert
        assert result is False
    
    def test_setup_git_config(self, mock_subprocess):
        """Test setting up multiple Git configuration options."""
        # Arrange
        git_config = GitConfig()
        options = {
            'core.autocrlf': 'input',
            'core.fileMode': 'false'
        }
        
        # Act
        result = git_config.setup_git_config(options)
        
        # Assert
        assert result is True
        mock_subprocess['check_call'].assert_any_call(['git', 'config', '--global', 'core.autocrlf', 'input'])
        mock_subprocess['check_call'].assert_any_call(['git', 'config', '--global', 'core.fileMode', 'false'])
    
    def test_is_inside_work_tree_true(self, mock_subprocess):
        """Test checking if inside work tree when true."""
        # Arrange
        git_config = GitConfig()
        mock_subprocess['check_output'].return_value = "true"
        
        # Act
        result = git_config.is_inside_work_tree()
        
        # Assert
        assert result is True
        mock_subprocess['check_output'].assert_any_call(['git', 'rev-parse', '--is-inside-work-tree'], text=True)
    
    def test_is_inside_work_tree_false(self, mock_subprocess):
        """Test checking if inside work tree when false."""
        # Arrange
        git_config = GitConfig()
        mock_subprocess['check_output'].side_effect = subprocess.CalledProcessError(128, "git rev-parse")
        
        # Act
        result = git_config.is_inside_work_tree()
        
        # Assert
        assert result is False