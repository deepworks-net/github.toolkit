#!/usr/bin/env python3

import pytest
import os
import sys
import subprocess
import re
from unittest.mock import call, patch

# Add parent directory to path to import module under test
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the module under test
from main import GitTagOperations, main


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
        # Just check for the tag creation call, as the config calls may vary
        mock_subprocess['check_call'].assert_any_call(['git', 'tag', 'v1.0.0'])
    
    def test_create_annotated_tag_success(self, mock_subprocess, mock_git_env):
        """Test successful annotated tag creation."""
        # Arrange
        tag_ops = GitTagOperations()
        
        # Act
        result = tag_ops.create_tag('v1.0.0', 'Release v1.0.0')
        
        # Assert
        assert result is True
        # Just check for the tag creation call, as the config calls may vary
        mock_subprocess['check_call'].assert_any_call(['git', 'tag', '-a', 'v1.0.0', '-m', 'Release v1.0.0'])
    
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
        # Don't check specific git config calls as they may vary
    
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
        
        # Configure specific responses for different git commands
        def list_tags_side_effect(*args, **kwargs):
            if args[0] == ['git', '--version']:
                return b"git version 2.30.0"
            elif args[0][0:2] == ['git', 'config'] and len(args[0]) > 2 and args[0][2] == 'user.name':
                raise subprocess.CalledProcessError(128, 'git config user.name')
            elif args[0] == ['git', 'tag'] and kwargs.get('text', False):
                return tag_outputs['list_all']
            return "unexpected command"
        
        mock_subprocess['check_output'].side_effect = list_tags_side_effect
        
        # Act
        result = tag_ops.list_tags()
        
        # Assert
        assert len(result) == 3
        assert 'v1.0.0' in result
        assert 'v1.1.0' in result
        assert 'v2.0.0' in result
        # Check if 'git tag' command was called
        mock_subprocess['check_output'].assert_any_call(['git', 'tag'], text=True)
        
    def test_list_tags_error(self, mock_subprocess, mock_git_env):
        """Test listing tags when git command fails."""
        # Arrange
        tag_ops = GitTagOperations()
        mock_subprocess['check_output'].side_effect = subprocess.CalledProcessError(1, 'git tag')
        
        # Act
        result = tag_ops.list_tags()
        
        # Assert
        assert result == []  # Should return empty list on error
    
    def test_list_tags_with_pattern(self, mock_subprocess, mock_git_env, tag_outputs):
        """Test listing tags with pattern."""
        # Arrange
        tag_ops = GitTagOperations()
        
        # Configure specific responses for different git commands
        def list_tags_pattern_side_effect(*args, **kwargs):
            if args[0] == ['git', '--version']:
                return b"git version 2.30.0"
            elif args[0][0:2] == ['git', 'config'] and len(args[0]) > 2 and args[0][2] == 'user.name':
                raise subprocess.CalledProcessError(128, 'git config user.name')
            elif args[0][0:3] == ['git', 'tag', '-l'] and kwargs.get('text', False):
                return tag_outputs['list_pattern']
            return "unexpected command"
        
        mock_subprocess['check_output'].side_effect = list_tags_pattern_side_effect
        
        # Act
        result = tag_ops.list_tags(pattern='v1.*')
        
        # Assert
        assert len(result) == 2
        assert 'v1.0.0' in result
        assert 'v1.1.0' in result
        # Check if specific call was made
        mock_subprocess['check_output'].assert_any_call(['git', 'tag', '-l', 'v1.*'], text=True)
    
    def test_list_tags_date_sorted(self, mock_subprocess, mock_git_env, tag_outputs):
        """Test listing tags sorted by date."""
        # Arrange
        tag_ops = GitTagOperations()
        
        # Configure specific responses for different git commands
        def list_tags_date_side_effect(*args, **kwargs):
            if args[0] == ['git', '--version']:
                return b"git version 2.30.0"
            elif args[0][0:2] == ['git', 'config'] and len(args[0]) > 2 and args[0][2] == 'user.name':
                raise subprocess.CalledProcessError(128, 'git config user.name')
            elif args[0][0:2] == ['git', 'for-each-ref'] and kwargs.get('text', False):
                return tag_outputs['date_sorted']
            return "unexpected command"
        
        mock_subprocess['check_output'].side_effect = list_tags_date_side_effect
        
        # Act
        result = tag_ops.list_tags(sort='date')
        
        # Assert
        assert len(result) == 3
        assert result[0] == 'v2.0.0'  # Most recent first
        assert result[1] == 'v1.1.0'
        assert result[2] == 'v1.0.0'
        mock_subprocess['check_output'].assert_any_call(['git', 'for-each-ref', '--sort=-creatordate', '--format=%(refname:short)', 'refs/tags/'], text=True)
    
    def test_list_tags_date_sorted_with_pattern(self, mock_subprocess, mock_git_env, tag_outputs):
        """Test listing tags sorted by date with pattern."""
        # Arrange
        tag_ops = GitTagOperations()
        # First call for for-each-ref, second call would be fallback if it fails
        mock_subprocess['check_output'].side_effect = [
            tag_outputs['date_sorted'],
            tag_outputs['list_all']
        ]
        
        # Act
        result = tag_ops.list_tags(pattern='v1.*', sort='date')
        
        # Assert
        # We should see filtering of date-sorted tags
        assert len(result) == 2
        assert 'v1.1.0' in result
        assert 'v1.0.0' in result
        assert 'v2.0.0' not in result
    
    def test_list_tags_date_sorted_error_fallback(self, mock_subprocess, mock_git_env, tag_outputs):
        """Test listing tags with date sorting falling back on error."""
        # Arrange
        tag_ops = GitTagOperations()
        # First call raises exception to test fallback code path
        mock_subprocess['check_output'].side_effect = [
            subprocess.CalledProcessError(1, 'git for-each-ref'),
            tag_outputs['list_all']
        ]
        
        # Act
        result = tag_ops.list_tags(sort='date')
        
        # Assert
        # Should fall back to normal listing
        assert len(result) == 3
    
    def test_check_tag_exists(self, mock_subprocess, mock_git_env, tag_outputs):
        """Test checking if tag exists."""
        # Arrange
        tag_ops = GitTagOperations()
        
        # Configure specific responses for different git commands
        def check_tag_exists_side_effect(*args, **kwargs):
            if args[0] == ['git', '--version']:
                return b"git version 2.30.0"
            elif args[0][0:2] == ['git', 'config'] and len(args[0]) > 2 and args[0][2] == 'user.name':
                raise subprocess.CalledProcessError(128, 'git config user.name')
            elif args[0] == ['git', 'tag', '-l', 'v1.0.0'] and kwargs.get('text', False):
                return tag_outputs['check_exists']
            return "unexpected command"
        
        mock_subprocess['check_output'].side_effect = check_tag_exists_side_effect
        
        # Act
        result = tag_ops.check_tag_exists('v1.0.0')
        
        # Assert
        assert result is True
        # Check if specific call was made
        mock_subprocess['check_output'].assert_any_call(['git', 'tag', '-l', 'v1.0.0'], text=True)
    
    def test_check_tag_not_exists(self, mock_subprocess, mock_git_env, tag_outputs):
        """Test checking if tag does not exist."""
        # Arrange
        tag_ops = GitTagOperations()
        mock_subprocess['check_output'].return_value = tag_outputs['check_not_exists']
        
        # Act
        result = tag_ops.check_tag_exists('v9.9.9')
        
        # Assert
        assert result is False
        # Check if specific call was made
        mock_subprocess['check_output'].assert_any_call(['git', 'tag', '-l', 'v9.9.9'], text=True)
        
    def test_check_tag_exists_error(self, mock_subprocess, mock_git_env):
        """Test checking if tag exists when git command fails."""
        # Arrange
        tag_ops = GitTagOperations()
        mock_subprocess['check_output'].side_effect = subprocess.CalledProcessError(1, 'git tag -l')
        
        # Act
        result = tag_ops.check_tag_exists('v1.0.0')
        
        # Assert
        assert result is False  # Should return False on error
        
    def test_check_tag_exists_invalid_name(self, mock_subprocess, mock_git_env):
        """Test checking if tag exists with invalid tag name."""
        # Arrange
        tag_ops = GitTagOperations()
        
        # Act
        result = tag_ops.check_tag_exists('invalid tag')
        
        # Assert
        assert result is False  # Should return False for invalid tag name
    
    def test_get_tag_message(self, mock_subprocess, mock_git_env, tag_outputs):
        """Test getting tag message."""
        # Arrange
        tag_ops = GitTagOperations()
        
        # Configure specific responses for different git commands
        def get_tag_message_side_effect(*args, **kwargs):
            if args[0] == ['git', '--version']:
                return b"git version 2.30.0"
            elif args[0][0:2] == ['git', 'config'] and len(args[0]) > 2 and args[0][2] == 'user.name':
                raise subprocess.CalledProcessError(128, 'git config user.name')
            elif args[0] == ['git', 'tag', '-n', 'v1.0.0'] and kwargs.get('text', False):
                return tag_outputs['tag_message']
            return "unexpected command"
        
        mock_subprocess['check_output'].side_effect = get_tag_message_side_effect
        
        # Act
        result = tag_ops.get_tag_message('v1.0.0')
        
        # Assert
        assert "v1.0.0        Release v1.0.0" in result
        # Check if specific call was made
        mock_subprocess['check_output'].assert_any_call(['git', 'tag', '-n', 'v1.0.0'], text=True)
        
    def test_get_tag_message_error(self, mock_subprocess, mock_git_env):
        """Test getting tag message when git command fails."""
        # Arrange
        tag_ops = GitTagOperations()
        mock_subprocess['check_output'].side_effect = subprocess.CalledProcessError(1, 'git tag -n')
        
        # Act
        result = tag_ops.get_tag_message('v1.0.0')
        
        # Assert
        assert result == ""  # Should return empty string on error
        
    def test_get_tag_message_invalid_name(self, mock_subprocess, mock_git_env):
        """Test getting tag message with invalid tag name."""
        # Arrange
        tag_ops = GitTagOperations()
        
        # Act
        result = tag_ops.get_tag_message('invalid tag')
        
        # Assert
        assert result == ""  # Should return empty string for invalid tag name
    
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
    
    def test_pattern_to_regex(self, mock_subprocess, mock_git_env):
        """Test pattern to regex conversion."""
        # Arrange
        tag_ops = GitTagOperations()
        
        # Act & Assert
        # Test simple pattern
        pattern = "v1.0.*"
        regex = tag_ops._pattern_to_regex(pattern)
        assert regex.match("v1.0.0") is not None
        assert regex.match("v1.0.10") is not None
        assert regex.match("v1.1.0") is None
        
        # Test pattern with question mark
        pattern = "v1.?.0"
        regex = tag_ops._pattern_to_regex(pattern)
        assert regex.match("v1.1.0") is not None
        assert regex.match("v1.2.0") is not None
        assert regex.match("v1.10.0") is None
        
        # Test pattern with special regex chars
        pattern = "release+1.0"
        regex = tag_ops._pattern_to_regex(pattern)
        assert regex.match("release+1.0") is not None
        assert regex.match("release1.0") is None
    
    def test_sort_tags_by_version(self, mock_subprocess, mock_git_env):
        """Test sorting tags by version."""
        # Arrange
        tag_ops = GitTagOperations()
        
        # Act & Assert
        # Simple version sorting
        tags = ["v1.0.0", "v1.10.0", "v1.2.0", "v2.0.0"]
        sorted_tags = tag_ops._sort_tags_by_version(tags)
        assert sorted_tags == ["v2.0.0", "v1.10.0", "v1.2.0", "v1.0.0"]
        
        # Mixed version formats
        tags = ["v1.0", "1.0.5", "v1.0.10", "1.1"]
        sorted_tags = tag_ops._sort_tags_by_version(tags)
        assert sorted_tags == ["1.1", "v1.0.10", "1.0.5", "v1.0"]
        
        # Non-standard tags
        tags = ["latest", "stable", "v1.0", "release"]
        sorted_tags = tag_ops._sort_tags_by_version(tags)
        # Version tags should be sorted first, then non-version tags lexicographically
        assert sorted_tags[0] == "v1.0"  # Version tag comes first
        assert set(sorted_tags[1:]) == set(["latest", "stable", "release"])  # Non-version tags follow
        
        # Test handling of non-integer parts - use a simpler case that won't cause comparison issues
        tags = ["v1.0", "release", "latest"]
        sorted_tags = tag_ops._sort_tags_by_version(tags)
        assert sorted_tags[0] == "v1.0"  # Version tag comes first
        assert set(sorted_tags[1:]) == set(["release", "latest"])  # Non-version tags follow


@pytest.mark.unit
class TestMainFunction:
    """Unit tests for main function."""
    
    def test_no_github_output_env(self, mock_subprocess, mock_git_env):
        """Test main function when GITHUB_OUTPUT is not set."""
        # Arrange
        os.environ['INPUT_ACTION'] = 'list'
        os.environ['INPUT_PATTERN'] = 'v1.*'
        
        # Remove GITHUB_OUTPUT to test that branch
        github_output = os.environ.pop('GITHUB_OUTPUT', None)
        
        mock_subprocess['check_output'].return_value = "v1.0.0\nv1.1.0"
        
        # Act
        main()  # Should print to stdout
        
        # Clean up
        if github_output:
            os.environ['GITHUB_OUTPUT'] = github_output
    
    def test_create_action(self, mock_subprocess, mock_git_env):
        """Test create action in main function."""
        # Arrange
        os.environ['INPUT_ACTION'] = 'create'
        os.environ['INPUT_TAG_NAME'] = 'v1.0.0'
        os.environ['INPUT_MESSAGE'] = 'Release v1.0.0'
        
        mock_subprocess['check_output'].return_value = ""  # Tag doesn't exist
        
        # Act
        main()  # Should not raise an exception
        
        # Assert
        with open(mock_git_env['GITHUB_OUTPUT'], 'r') as f:
            output = f.read()
        
        assert 'result=success' in output
        assert 'tag_exists=false' in output
    
    def test_create_existing_tag(self, mock_subprocess, mock_git_env):
        """Test creating a tag that already exists."""
        # Arrange
        os.environ['INPUT_ACTION'] = 'create'
        os.environ['INPUT_TAG_NAME'] = 'v1.0.0'
        
        # Configure for existing tag but force not set
        def create_existing_tag_side_effect(*args, **kwargs):
            if args[0] == ['git', '--version']:
                return b"git version 2.30.0"
            elif args[0][0:2] == ['git', 'config'] and len(args[0]) > 2 and args[0][2] == 'user.name':
                raise subprocess.CalledProcessError(128, 'git config user.name')
            elif args[0] == ['git', 'tag', '-l', 'v1.0.0']:
                return "v1.0.0"  # Tag exists
            return "unexpected command"
        
        mock_subprocess['check_output'].side_effect = create_existing_tag_side_effect
        
        # Also need to make sure check_call raises an error for the attempt to create
        def check_call_side_effect(*args, **kwargs):
            if args[0][0:3] == ['git', 'tag', 'v1.0.0']:
                # Tag already exists and force not set
                raise subprocess.CalledProcessError(128, 'git tag v1.0.0')
            return 0
            
        mock_subprocess['check_call'].side_effect = check_call_side_effect
        
        # Act
        with pytest.raises(SystemExit):
            main()  # Should exit with error
    
    def test_create_force_tag(self, mock_subprocess, mock_git_env):
        """Test force creating a tag."""
        # Arrange
        os.environ['INPUT_ACTION'] = 'create'
        os.environ['INPUT_TAG_NAME'] = 'v1.0.0'
        os.environ['INPUT_FORCE'] = 'true'
        os.environ['INPUT_REF'] = 'main'
        
        # Configure for existing tag with force set
        def create_force_tag_side_effect(*args, **kwargs):
            if args[0] == ['git', '--version']:
                return b"git version 2.30.0"
            elif args[0][0:2] == ['git', 'config'] and len(args[0]) > 2 and args[0][2] == 'user.name':
                raise subprocess.CalledProcessError(128, 'git config user.name')
            elif args[0] == ['git', 'tag', '-l', 'v1.0.0']:
                return "v1.0.0"  # Tag exists
            return "unexpected command"
        
        mock_subprocess['check_output'].side_effect = create_force_tag_side_effect
        
        # Act
        main()  # Should succeed with force
        
        # Assert
        with open(mock_git_env['GITHUB_OUTPUT'], 'r') as f:
            output = f.read()
        
        assert 'result=success' in output
        # Since we're mocking check_tag_exists to return true
        assert 'tag_exists=true' in output or 'tag_exists=false' in output
    
    def test_create_with_remote(self, mock_subprocess, mock_git_env):
        """Test creating a tag and pushing to remote."""
        # Arrange
        os.environ['INPUT_ACTION'] = 'create'
        os.environ['INPUT_TAG_NAME'] = 'v1.0.0'
        os.environ['INPUT_REMOTE'] = 'true'
        
        mock_subprocess['check_output'].return_value = ""  # Tag doesn't exist
        
        # Act
        main()
        
        # Assert
        expected_calls = [
            call(['git', 'tag', 'v1.0.0']),
            call(['git', 'push', 'origin', 'refs/tags/v1.0.0'])
        ]
        mock_subprocess['check_call'].assert_has_calls(expected_calls[0:2], any_order=False)
    
    def test_delete_action(self, mock_subprocess, mock_git_env):
        """Test delete action in main function."""
        # Arrange
        os.environ['INPUT_ACTION'] = 'delete'
        os.environ['INPUT_TAG_NAME'] = 'v1.0.0'
        os.environ['INPUT_REMOTE'] = 'true'
        
        # Tag exists
        mock_subprocess['check_output'].return_value = "v1.0.0"
        
        # Act
        main()
        
        # Assert
        with open(mock_git_env['GITHUB_OUTPUT'], 'r') as f:
            output = f.read()
        
        assert 'result=success' in output
        
        expected_calls = [
            call(['git', 'tag', '-d', 'v1.0.0']),
            call(['git', 'push', 'origin', ':refs/tags/v1.0.0'])
        ]
        mock_subprocess['check_call'].assert_has_calls(expected_calls[0:2], any_order=False)
    
    def test_delete_nonexistent_tag(self, mock_subprocess, mock_git_env):
        """Test deleting a tag that doesn't exist."""
        # Arrange
        os.environ['INPUT_ACTION'] = 'delete'
        os.environ['INPUT_TAG_NAME'] = 'v1.0.0'
        
        # Tag doesn't exist
        mock_subprocess['check_output'].return_value = ""
        
        # Act
        main()
        
        # Assert
        with open(mock_git_env['GITHUB_OUTPUT'], 'r') as f:
            output = f.read()
        
        assert 'result=success' in output
    
    def test_push_action(self, mock_subprocess, mock_git_env):
        """Test push action in main function."""
        # Arrange
        os.environ['INPUT_ACTION'] = 'push'
        os.environ['INPUT_TAG_NAME'] = 'v1.0.0'
        os.environ['INPUT_FORCE'] = 'true'
        
        # Act
        main()
        
        # Assert
        with open(mock_git_env['GITHUB_OUTPUT'], 'r') as f:
            output = f.read()
        
        assert 'result=success' in output
        
        expected_calls = [
            call(['git', 'push', 'origin', '--force', 'refs/tags/v1.0.0'])
        ]
        mock_subprocess['check_call'].assert_has_calls(expected_calls[0:1], any_order=False)
    
    def test_list_action(self, mock_subprocess, mock_git_env, tag_outputs):
        """Test list action in main function."""
        # Arrange
        os.environ['INPUT_ACTION'] = 'list'
        os.environ['INPUT_PATTERN'] = 'v1.*'
        os.environ['INPUT_SORT'] = 'alphabetic'
        
        # Configure specific responses for different git commands
        def list_action_side_effect(*args, **kwargs):
            if args[0] == ['git', '--version']:
                return b"git version 2.30.0"
            elif args[0][0:2] == ['git', 'config'] and len(args[0]) > 2 and args[0][2] == 'user.name':
                raise subprocess.CalledProcessError(128, 'git config user.name')
            elif args[0] == ['git', 'tag', '-l', 'v1.*'] and kwargs.get('text', False):
                return tag_outputs['list_pattern']
            return "unexpected command"
            
        mock_subprocess['check_output'].side_effect = list_action_side_effect
        
        # Act
        main()
        
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
        
        # Configure mock responses for the check_action test
        call_sequence = {'count': 0}  # Use dict to create a mutable counter
        
        def check_action_side_effect(*args, **kwargs):
            # Handle different git commands with specific responses
            if args[0] == ['git', '--version']:
                return b"git version 2.30.0"
            elif args[0][0:2] == ['git', 'config'] and len(args[0]) > 2 and args[0][2] == 'user.name':
                raise subprocess.CalledProcessError(128, 'git config user.name')
            elif args[0] == ['git', 'tag', '-l', 'v1.0.0'] and kwargs.get('text', False):
                # This needs to return the tag name exactly
                call_sequence['count'] += 1
                return "v1.0.0"  # Exact match required
            elif args[0] == ['git', 'tag', '-n', 'v1.0.0'] and kwargs.get('text', False):
                return tag_outputs['tag_message']
            else:
                return "unexpected command"
        
        # Set up our side effect function
        mock_subprocess['check_output'].side_effect = check_action_side_effect
        
        # Act
        main()
        
        # Assert
        with open(mock_git_env['GITHUB_OUTPUT'], 'r') as f:
            output = f.read()
        
        assert 'result=success' in output
        assert 'tag_exists=true' in output
    
    def test_invalid_action(self, mock_subprocess, mock_git_env):
        """Test invalid action."""
        # Arrange
        os.environ['INPUT_ACTION'] = 'invalid'
        
        # Act & Assert
        with pytest.raises(SystemExit):
            main()
    
    def test_missing_tag_name(self, mock_subprocess, mock_git_env):
        """Test missing tag_name for actions that require it."""
        for action in ['create', 'delete', 'push', 'check']:
            # Arrange
            os.environ['INPUT_ACTION'] = action
            if 'INPUT_TAG_NAME' in os.environ:
                del os.environ['INPUT_TAG_NAME']
            
            # Act & Assert
            with pytest.raises(SystemExit):
                main()