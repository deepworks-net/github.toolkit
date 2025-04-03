#!/usr/bin/env python3

import pytest
import os
import sys
import subprocess
import tempfile
from unittest.mock import patch, MagicMock

# Add parent directory to path to import module under test
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the module under test
from git_errors import GitErrors


@pytest.fixture
def mock_github_output():
    """Create a temporary file for GitHub output."""
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as f:
        github_output = f.name
    
    # Set environment variable
    original_github_output = os.environ.get('GITHUB_OUTPUT')
    os.environ['GITHUB_OUTPUT'] = github_output
    
    yield github_output
    
    # Clean up
    if os.path.exists(github_output):
        os.remove(github_output)
    
    # Restore original environment
    if original_github_output:
        os.environ['GITHUB_OUTPUT'] = original_github_output
    else:
        del os.environ['GITHUB_OUTPUT']


class TestGitErrors:
    """Unit tests for GitErrors class."""
    
    def test_init_with_custom_output(self):
        """Test initialization with custom GitHub output path."""
        # Arrange & Act
        errors = GitErrors("/custom/path")
        
        # Assert
        assert errors.github_output == "/custom/path"
    
    def test_init_with_environment_variable(self):
        """Test initialization with GitHub output from environment."""
        # Arrange
        os.environ['GITHUB_OUTPUT'] = "/env/path"
        
        # Act
        errors = GitErrors()
        
        # Assert
        assert errors.github_output == "/env/path"
        
        # Clean up
        del os.environ['GITHUB_OUTPUT']
    
    def test_set_github_output(self, mock_github_output):
        """Test setting GitHub output."""
        # Arrange
        errors = GitErrors()
        
        # Act
        errors._set_github_output("test_key", "test_value")
        
        # Assert
        with open(mock_github_output, 'r') as f:
            content = f.read()
        assert "test_key=test_value" in content
    
    def test_get_detailed_error_known_pattern(self):
        """Test getting detailed error with a known pattern."""
        # Arrange
        errors = GitErrors()
        error = subprocess.CalledProcessError(1, "git checkout branch")
        error.output = "error: pathspec 'branch' did not match any file(s) known to git"
        
        # Act
        message = errors._get_detailed_error(error)
        
        # Assert
        assert "Command 'git checkout branch' failed with exit code 1" in message
        assert "does not exist" in message
    
    def test_get_detailed_error_unknown_pattern(self):
        """Test getting detailed error with an unknown pattern."""
        # Arrange
        errors = GitErrors()
        error = subprocess.CalledProcessError(1, "git custom-command")
        error.output = "Unknown error occurred"
        
        # Act
        message = errors._get_detailed_error(error)
        
        # Assert
        assert "Command 'git custom-command' failed with exit code 1" in message
        assert "Unknown error occurred" in message
    
    def test_handle_git_error(self, mock_github_output):
        """Test handling Git error."""
        # Arrange
        errors = GitErrors()
        error = subprocess.CalledProcessError(1, "git command")
        error.output = "Error output"
        
        # Act
        message = errors.handle_git_error(error, "Test context")
        
        # Assert
        assert "Test context" in message
        
        # Check GitHub output
        with open(mock_github_output, 'r') as f:
            content = f.read()
        assert "result=failure" in content
    
    def test_handle_git_error_no_exit(self):
        """Test handling Git error without exiting."""
        # Arrange
        errors = GitErrors()
        error = subprocess.CalledProcessError(1, "git command")
        error.output = "Error output"
        
        # Act
        message = errors.handle_git_error(error, exit_on_error=False)
        
        # Assert
        assert "Command 'git command' failed with exit code 1" in message
    
    def test_handle_specific_errors(self, mock_github_output):
        """Test handling specific Git errors."""
        # Arrange
        errors = GitErrors()
        error = subprocess.CalledProcessError(1, "git command")
        error.output = "Error output"
        
        # Test different specific handlers
        test_cases = [
            (errors.handle_checkout_error, "branch", "Failed to checkout branch"),
            (errors.handle_push_error, "refs/heads/main", "Failed to push"),
            (errors.handle_merge_error, "", "Failed to merge"),
            (errors.handle_tag_error, "", "Failed in tag operation"),
            (errors.handle_clone_error, "", "Failed to clone repository"),
            (errors.handle_commit_error, "", "Failed to commit"),
            (errors.handle_fetch_error, "", "Failed to fetch"),
        ]
        
        # Act & Assert
        for handler, param, expected_text in test_cases:
            if param:
                message = handler(error, param)
            else:
                message = handler(error)
            assert expected_text in message
    
    def test_handle_tag_error_with_details(self):
        """Test handling tag error with action and tag."""
        # Arrange
        errors = GitErrors()
        error = subprocess.CalledProcessError(1, "git tag -a v1.0.0")
        error.output = "Error output"
        
        # Act
        message = errors.handle_tag_error(error, "create", "v1.0.0")
        
        # Assert
        assert "Failed to create tag 'v1.0.0'" in message
    
    def test_handle_clone_error_with_sanitization(self):
        """Test handling clone error with URL sanitization."""
        # Arrange
        errors = GitErrors()
        error = subprocess.CalledProcessError(1, "git clone")
        error.output = "Error output"
        
        # Act
        message = errors.handle_clone_error(error, "https://token@github.com/org/repo.git")
        
        # Assert
        assert "Failed to clone repository 'https://***@github.com/org/repo.git'" in message
    
    def test_handle_commit_error_with_message(self):
        """Test handling commit error with message."""
        # Arrange
        errors = GitErrors()
        error = subprocess.CalledProcessError(1, "git commit")
        error.output = "Error output"
        
        # Act
        message = errors.handle_commit_error(error, "A very long commit message that should be truncated in the error output")
        
        # Assert
        assert "Failed to commit with message 'A very long commit message t...'" in message