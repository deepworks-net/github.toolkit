#!/usr/bin/env python3

import pytest
import os
import sys
import subprocess
import re
from unittest.mock import call

# Add parent directory to path to import module under test
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the module under test
from main import GitTagOperations


@pytest.mark.unit
class TestGitTagOperations:
    """Unit tests for GitTagOperations class."""
    
    def test_create_lightweight_tag_success(self, mock_subprocess, mock_git_env):
        """Test successful lightweight tag creation."""
        # Arrange
        tag_ops = GitTagOperations()
        
        # Act
        result = tag_ops.create_tag('v1.0.0')
        
        # Assert
        assert result is True
        expected_calls = [
            call(['git', 'config', '--global', '--add', 'safe.directory', '/github/workspace']),
            call(['git', 'tag', 'v1.0.0'])
        ]
        mock_subprocess['check_call'].assert_has_calls(expected_calls)
    
    def test_create_annotated_tag_success(self, mock_subprocess, mock_git_env):
        """Test successful annotated tag creation."""
        # Arrange
        tag_ops = GitTagOperations()
        
        # Act
        result = tag_ops.create_tag('v1.0.0', 'Release v1.0.0')
        
        # Assert
        assert result is True
        expected_calls = [
            call(['git', 'config', '--global', '--add', 'safe.directory', '/github/workspace']),
            call(['git', 'tag', '-a', 'v1.0.0', '-m', 'Release v1.0.0'])
        ]
        mock_subprocess['check_call'].assert_has_calls(expected_calls)
    
    def test_create_tag_at_ref(self, mock_subprocess, mock_git_env):
        """Test creating tag at specific ref."""
        # Arrange
        tag_ops = GitTagOperations()
        
        # Act
        result = tag_ops.create_tag('v1.0.0', ref='abc123')
        
        # Assert
        assert result is True
        expected_calls = [
            call(['git', 'tag', 'v1.0.0', 'abc123'])
        ]
        mock_subprocess['check_call'].assert_has_calls(expected_calls[0:1])
    
    def test_create_tag_force(self, mock_subprocess, mock_git_env):
        """Test force creating tag."""
        # Arrange
        tag_ops = GitTagOperations()
        
        # Act
        result = tag_ops.create_tag('v1.0.0', force=True)
        
        # Assert
        assert result is True
        expected_calls = [
            call(['git', 'tag', '-f', 'v1.0.0'])
        ]
        mock_subprocess['check_call'].assert_has_calls(expected_calls[0:1])
    
    def test_create_tag_invalid_name(self, mock_subprocess, mock_git_env):
        """Test creating tag with invalid name."""
        # Arrange
        tag_ops = GitTagOperations()
        
        # Act
        result = tag_ops.create_tag('invalid tag')
        
        # Assert
        assert result is False
        mock_subprocess['check_call'].assert_called_once_with(['git', 'config', '--global', '--add', 'safe.directory', '/github/workspace'])
    
    def test_delete_tag_success(self, mock_subprocess, mock_git_env):
        """Test successful tag deletion."""
        # Arrange
        tag_ops = GitTagOperations()
        
        # Act
        result = tag_ops.delete_tag('v1.0.0')
        
        # Assert
        assert result is True
        expected_calls = [
            call(['git', 'tag', '-d', 'v1.0.0'])
        ]
        mock_subprocess['check_call'].assert_has_calls(expected_calls)
    
    def test_delete_remote_tag(self, mock_subprocess, mock_git_env):
        """Test deleting tag locally and remotely."""
        # Arrange
        tag_ops = GitTagOperations()
        
        # Act
        result = tag_ops.delete_tag('v1.0.0', remote=True)
        
        # Assert
        assert result is True
        expected_calls = [
            call(['git', 'tag', '-d', 'v1.0.0']),
            call(['git', 'push', 'origin', ':refs/tags/v1.0.0'])
        ]
        mock_subprocess['check_call'].assert_has_calls(expected_calls)
    
    def test_push_tag_success(self, mock_subprocess, mock_git_env):
        """Test successful tag push."""
        # Arrange
        tag_ops = GitTagOperations()
        
        # Act
        result = tag_ops.push_tag('v1.0.0')
        
        # Assert
        assert result is True
        expected_calls = [
            call(['git', 'push', 'origin', 'refs/tags/v1.0.0'])
        ]
        mock_subprocess['check_call'].assert_has_calls(expected_calls)
    
    def test_push_tag_force(self, mock_subprocess, mock_git_env):
        """Test force pushing tag."""
        # Arrange
        tag_ops = GitTagOperations()
        
        # Act
        result = tag_ops.push_tag('v1.0.0', force=True)
        
        # Assert
        assert result is True
        expected_calls = [
            call(['git', 'push', 'origin', '--force', 'refs/tags/v1.0.0'])
        ]
        mock_subprocess['check_call'].assert_has_calls(expected_calls)
    
    def test_list_tags(self, mock_subprocess, mock_git_env, tag_outputs):
        """Test listing tags."""
        # Arrange
        tag_ops = GitTagOperations()
        mock_subprocess['check_output'].return_value = tag_outputs['list_all']
        
        # Act
        result = tag_ops.list_tags()
        
        # Assert
        assert len(result) == 3
        assert 'v1.0.0' in result
        assert 'v1.1.0' in result
        assert 'v2.0.0' in result
        mock_subprocess['check_output'].assert_called_once_with(['git', 'tag'], text=True)
    
    def test_list_tags_with_pattern(self, mock_subprocess, mock_git_env, tag_outputs):
        """Test listing tags with pattern."""
        # Arrange
        tag_ops = GitTagOperations()
        mock_subprocess['check_output'].return_value = tag_outputs['list_pattern']
        
        # Act
        result = tag_ops.list_tags(pattern='v1.*')
        
        # Assert
        assert len(result) == 2
        assert 'v1.0.0' in result
        assert 'v1.1.0' in result
        mock_subprocess['check_output'].assert_called_once_with(['git', 'tag', '-l', 'v1.*'], text=True)
    
    def test_list_tags_date_sorted(self, mock_subprocess, mock_git_env, tag_outputs):
        """Test listing tags sorted by date."""
        # Arrange
        tag_ops = GitTagOperations()
        mock_subprocess['check_output'].return_value = tag_outputs['date_sorted']
        
        # Act
        result = tag_ops.list_tags(sort='date')
        
        # Assert
        assert len(result) == 3
        assert result[0] == 'v2.0.0'  # Most recent first
        assert result[1] == 'v1.1.0'
        assert result[2] == 'v1.0.0'
        mock_subprocess['check_output'].assert_called_with(['git', 'for-each-ref', '--sort=-creatordate', '--format=%(refname:short)', 'refs/tags/'], text=True)
    
    def test_check_tag_exists(self, mock_subprocess, mock_git_env, tag_outputs):
        """Test checking if tag exists."""
        # Arrange
        tag_ops = GitTagOperations()
        mock_subprocess['check_output'].return_value = tag_outputs['check_exists']
        
        # Act
        result = tag_ops.check_tag_exists('v1.0.0')
        
        # Assert
        assert result is True
        mock_subprocess['check_output'].assert_called_once_with(['git', 'tag', '-l', 'v1.0.0'], text=True)
    
    def test_check_tag_not_exists(self, mock_subprocess, mock_git_env, tag_outputs):
        """Test checking if tag does not exist."""
        # Arrange
        tag_ops = GitTagOperations()
        mock_subprocess['check_output'].return_value = tag_outputs['check_not_exists']
        
        # Act
        result = tag_ops.check_tag_exists('v9.9.9')
        
        # Assert
        assert result is False
        mock_subprocess['check_output'].assert_called_once_with(['git', 'tag', '-l', 'v9.9.9'], text=True)
    
    def test_get_tag_message(self, mock_subprocess, mock_git_env, tag_outputs):
        """Test getting tag message."""
        # Arrange
        tag_ops = GitTagOperations()
        mock_subprocess['check_output'].return_value = tag_outputs['tag_message']
        
        # Act
        result = tag_ops.get_tag_message('v1.0.0')
        
        # Assert
        assert "v1.0.0        Release v1.0.0" in result
        mock_subprocess['check_output'].assert_called_once_with(['git', 'tag', '-n', 'v1.0.0'], text=True)
    
    def test_validate_tag_name_valid(self, mock_subprocess, mock_git_env):
        """Test tag name validation with valid names."""
        # Arrange
        tag_ops = GitTagOperations()
        
        # Act & Assert
        assert tag_ops._validate_tag_name('v1.0.0') is True
        assert tag_ops._validate_tag_name('release/1.0.0') is True
        assert tag_ops._validate_tag_name('feature_tag') is True
    
    def test_validate_tag_name_invalid(self, mock_subprocess, mock_git_env):
        """Test tag name validation with invalid names."""
        # Arrange
        tag_ops = GitTagOperations()
        
        # Act & Assert
        assert tag_ops._validate_tag_name('invalid tag') is False  # Contains space
        assert tag_ops._validate_tag_name('-badstart') is False    # Starts with dash
        assert tag_ops._validate_tag_name('bad^char') is False     # Contains ^
        assert tag_ops._validate_tag_name('') is False             # Empty
        assert tag_ops._validate_tag_name('path..with..dots') is False  # Contains double dots


@pytest.mark.unit
class TestMainFunction:
    """Unit tests for main function."""
    
    def test_create_action(self, mock_subprocess, mock_git_env):
        """Test create action in main function."""
        # Arrange
        os.environ['INPUT_ACTION'] = 'create'
        os.environ['INPUT_TAG_NAME'] = 'v1.0.0'
        os.environ['INPUT_MESSAGE'] = 'Release v1.0.0'
        
        mock_subprocess['check_output'].return_value = ""  # Tag doesn't exist
        
        # Import main here to ensure env vars are set
        from main import main
        
        # Act
        main()  # Should not raise an exception
        
        # Assert
        with open(mock_git_env['GITHUB_OUTPUT'], 'r') as f:
            output = f.read()
        
        assert 'result=success' in output
        assert 'tag_exists=false' in output
    
    def test_list_action(self, mock_subprocess, mock_git_env, tag_outputs):
        """Test list action in main function."""
        # Arrange
        os.environ['INPUT_ACTION'] = 'list'
        os.environ['INPUT_PATTERN'] = 'v1.*'
        
        mock_subprocess['check_output'].return_value = tag_outputs['list_pattern']
        
        # Import main here to ensure env vars are set
        from main import main
        
        # Act
        main()  # Should not raise an exception
        
        # Assert
        with open(mock_git_env['GITHUB_OUTPUT'], 'r') as f:
            output = f.read()
        
        assert 'result=success' in output
        assert 'tags=v1.0.0,v1.1.0' in output
    
    def test_check_action(self, mock_subprocess, mock_git_env, tag_outputs):
        """Test check action in main function."""
        # Arrange
        os.environ['INPUT_ACTION'] = 'check'
        os.environ['INPUT_TAG_NAME'] = 'v1.0.0'
        
        mock_subprocess['check_output'].side_effect = [
            tag_outputs['check_exists'],  # check_tag_exists
            tag_outputs['tag_message']    # get_tag_message
        ]
        
        # Import main here to ensure env vars are set
        from main import main
        
        # Act
        main()  # Should not raise an exception
        
        # Assert
        with open(mock_git_env['GITHUB_OUTPUT'], 'r') as f:
            output = f.read()
        
        assert 'result=success' in output
        assert 'tag_exists=true' in output
        assert 'tag_message=v1.0.0        Release v1.0.0' in output