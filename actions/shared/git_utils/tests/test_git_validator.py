#!/usr/bin/env python3

import pytest
import os
import sys
import subprocess
import re
from unittest.mock import patch, MagicMock

# Add parent directory to path to import module under test
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the module under test
from git_validator import GitValidator


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


class TestGitValidator:
    """Unit tests for GitValidator class."""
    
    def test_is_valid_repository(self, mock_subprocess):
        """Test checking if directory is a valid Git repository."""
        # Arrange
        validator = GitValidator()
        
        # Act
        result = validator.is_valid_repository()
        
        # Assert
        assert result is True
        mock_subprocess['check_output'].assert_called_once_with(['git', 'rev-parse', '--git-dir'], stderr=subprocess.STDOUT)
    
    def test_is_valid_repository_not_a_repo(self, mock_subprocess):
        """Test checking if directory is not a valid Git repository."""
        # Arrange
        validator = GitValidator()
        mock_subprocess['check_output'].side_effect = subprocess.CalledProcessError(128, "git rev-parse")
        
        # Act
        result = validator.is_valid_repository()
        
        # Assert
        assert result is False
    
    def test_is_valid_branch_name_valid(self):
        """Test validating branch names with valid names."""
        # Arrange
        validator = GitValidator()
        valid_names = [
            'main',
            'feature/new-feature',
            'bugfix/123',
            'release-1.0',
            'v1.0.0',
            'fix_123'
        ]
        
        # Act & Assert
        for name in valid_names:
            assert validator.is_valid_branch_name(name) is True
    
    def test_is_valid_branch_name_invalid(self):
        """Test validating branch names with invalid names."""
        # Arrange
        validator = GitValidator()
        invalid_names = [
            '',  # Empty
            '-feature',  # Starts with dash
            'feature..branch',  # Contains double dots
            'feature branch',  # Contains space
            'feature~branch',  # Contains tilde
            'feature^branch',  # Contains caret
            'feature:branch',  # Contains colon
            'feature?branch',  # Contains question mark
            'feature*branch',  # Contains asterisk
            'feature[branch',  # Contains square bracket
            'feature\\branch',  # Contains backslash
        ]
        
        # Act & Assert
        for name in invalid_names:
            assert validator.is_valid_branch_name(name) is False
    
    def test_is_valid_tag_name(self):
        """Test validating tag names."""
        # Arrange
        validator = GitValidator()
        
        # The tag name validation uses the same logic as branch names
        # Just test a couple cases to ensure it's wired up correctly
        
        # Act & Assert
        assert validator.is_valid_tag_name('v1.0.0') is True
        assert validator.is_valid_tag_name('') is False
        assert validator.is_valid_tag_name('tag with space') is False
    
    def test_branch_exists_local(self, mock_subprocess):
        """Test checking if a local branch exists."""
        # Arrange
        validator = GitValidator()
        
        # Act
        result = validator.branch_exists('main')
        
        # Assert
        assert result is True
        mock_subprocess['check_output'].assert_called_once_with(
            ['git', 'show-ref', '--verify', 'refs/heads/main'], 
            stderr=subprocess.STDOUT
        )
    
    def test_branch_exists_local_not_found(self, mock_subprocess):
        """Test checking if a local branch doesn't exist."""
        # Arrange
        validator = GitValidator()
        mock_subprocess['check_output'].side_effect = subprocess.CalledProcessError(1, "git show-ref")
        
        # Act
        result = validator.branch_exists('non-existent')
        
        # Assert
        assert result is False
    
    def test_branch_exists_remote(self, mock_subprocess):
        """Test checking if a remote branch exists."""
        # Arrange
        validator = GitValidator()
        mock_subprocess['check_output'].return_value = "abcdef1234567890 refs/remotes/origin/main"
        
        # Act
        result = validator.branch_exists('main', remote=True)
        
        # Assert
        assert result is True
        mock_subprocess['check_output'].assert_called_once_with(['git', 'ls-remote', '--heads', 'origin', 'main'], text=True)
    
    def test_branch_exists_remote_not_found(self, mock_subprocess):
        """Test checking if a remote branch doesn't exist."""
        # Arrange
        validator = GitValidator()
        mock_subprocess['check_output'].return_value = ""
        
        # Act
        result = validator.branch_exists('non-existent', remote=True)
        
        # Assert
        assert result is False
    
    def test_tag_exists(self, mock_subprocess):
        """Test checking if a tag exists."""
        # Arrange
        validator = GitValidator()
        
        # Act
        result = validator.tag_exists('v1.0.0')
        
        # Assert
        assert result is True
        mock_subprocess['check_output'].assert_called_once_with(
            ['git', 'show-ref', '--verify', 'refs/tags/v1.0.0'], 
            stderr=subprocess.STDOUT
        )
    
    def test_commit_exists(self, mock_subprocess):
        """Test checking if a commit exists."""
        # Arrange
        validator = GitValidator()
        
        # Act
        result = validator.commit_exists('abcdef1234567890')
        
        # Assert
        assert result is True
        mock_subprocess['check_output'].assert_called_once_with(
            ['git', 'rev-parse', '--verify', 'abcdef1234567890^{commit}'], 
            stderr=subprocess.STDOUT
        )
    
    def test_commit_exists_not_found(self, mock_subprocess):
        """Test checking if a commit doesn't exist."""
        # Arrange
        validator = GitValidator()
        mock_subprocess['check_output'].side_effect = subprocess.CalledProcessError(128, "git rev-parse")
        
        # Act
        result = validator.commit_exists('non-existent')
        
        # Assert
        assert result is False
    
    def test_is_valid_file_path(self, mock_subprocess):
        """Test validating a file path."""
        # Arrange
        validator = GitValidator()
        mock_subprocess['check_output'].return_value = "/repo/root"
        
        # Act
        result = validator.is_valid_file_path('/repo/root/file.txt')
        
        # Assert
        assert result is True
        mock_subprocess['check_output'].assert_called_once_with(['git', 'rev-parse', '--show-toplevel'], text=True)
    
    def test_is_valid_file_path_invalid(self):
        """Test validating invalid file paths."""
        # Arrange
        validator = GitValidator()
        invalid_paths = [
            'file;rm -rf /',  # Command injection
            'file&echo hack',  # Command injection
            'file|cat /etc/passwd',  # Command injection
            'file>output',  # Redirection
            'file`rm -rf /`',  # Command substitution
            'file$(rm -rf /)',  # Command substitution
            'file\nrm -rf /',  # Newline
        ]
        
        # Act & Assert
        for path in invalid_paths:
            assert validator.is_valid_file_path(path) is False
    
    def test_is_valid_ref(self, mock_subprocess):
        """Test validating a Git reference."""
        # Arrange
        validator = GitValidator()
        
        # Act
        result = validator.is_valid_ref('main')
        
        # Assert
        assert result is True
        mock_subprocess['check_output'].assert_called_once_with(['git', 'rev-parse', '--verify', 'main'], stderr=subprocess.STDOUT)
    
    def test_pattern_to_regex(self):
        """Test converting Git patterns to regex patterns."""
        # Arrange
        validator = GitValidator()
        
        # Test patterns
        test_cases = [
            ('v1.*', 'v1.0.0', True),      # Wildcard match
            ('v1.*', 'v2.0.0', False),     # Wildcard no match
            ('release-?', 'release-1', True),  # Single char wildcard match
            ('release-?', 'release-10', False),  # Single char wildcard no match
            ('feature/*', 'feature/x', True),  # Directory wildcard match
            ('feature/*', 'bug/x', False),  # Directory wildcard no match
            ('v[12].*', 'v1.0.0', True),   # Character class match
            ('v[12].*', 'v3.0.0', False),  # Character class no match
        ]
        
        # Act & Assert
        for pattern, test_str, should_match in test_cases:
            regex = validator.pattern_to_regex(pattern)
            assert bool(regex.match(test_str)) is should_match
    
    def test_safe_git_command(self, mock_subprocess):
        """Test safely executing Git commands."""
        # Arrange
        validator = GitValidator()
        mock_subprocess['check_output'].return_value = "command output"
        
        # Act
        success, output = validator.safe_git_command(['git', 'status'])
        
        # Assert
        assert success is True
        assert output == "command output"
        mock_subprocess['check_output'].assert_called_once_with(['git', 'status'], text=True, stderr=subprocess.STDOUT)
    
    def test_safe_git_command_not_git(self):
        """Test safely executing non-Git commands."""
        # Arrange
        validator = GitValidator()
        
        # Act
        success, output = validator.safe_git_command(['ls', '-la'])
        
        # Assert
        assert success is False
        assert "Not a git command" in output
    
    def test_safe_git_command_dangerous(self):
        """Test safely executing dangerous Git commands."""
        # Arrange
        validator = GitValidator()
        dangerous_commands = [
            ['git', '--upload-pack=evil'],
            ['git', '--exec', 'evil'],
            ['git', '-c', 'evil.config=value'],
            ['git', '--config', 'evil.config=value'],
            ['git', '--git-dir', '/etc'],
            ['git', '--work-tree', '/etc'],
        ]
        
        # Act & Assert
        for cmd in dangerous_commands:
            success, output = validator.safe_git_command(cmd)
            assert success is False
            assert "Potentially dangerous argument" in output