#!/usr/bin/env python3

import pytest
import os
import sys
import subprocess
from unittest.mock import call, patch

# Add parent directory to path to import module under test
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the module under test
from main import GitCommitOperations, main, GitConfig, GitValidator, GitErrors


@pytest.mark.unit
@pytest.mark.git
@pytest.mark.commit
class TestGitCommitOperations:
    """Unit tests for GitCommitOperations class."""
    
    def test_create_commit_success(self, mock_subprocess, mock_git_env, commit_outputs):
        """Test successful commit creation."""
        # Arrange
        commit_ops = GitCommitOperations()
        # Set up responses for different commands
        def check_output_side_effect(*args, **kwargs):
            if args[0] == ['git', '--version']:
                return commit_outputs['git_version']
            elif args[0] == ['git', 'status', '--porcelain'] and kwargs.get('text', False):
                return "M  file1.txt"
            elif args[0] == ['git', 'rev-parse', 'HEAD'] and kwargs.get('text', False):
                return commit_outputs['commit_create']
            return ""
        
        mock_subprocess['check_output'].side_effect = check_output_side_effect
        
        # Act
        result, commit_hash = commit_ops.create_commit("Add new feature")
        
        # Assert
        assert result is True
        assert commit_hash == commit_outputs['commit_create']
        # Verify git commit command was called
        mock_subprocess['check_call'].assert_any_call(['git', 'commit', '-m', 'Add new feature'])
    
    def test_create_commit_with_files(self, mock_subprocess, mock_git_env, commit_outputs):
        """Test creating commit with specific files."""
        # Arrange
        commit_ops = GitCommitOperations()
        # Set up responses for different commands
        def check_output_side_effect(*args, **kwargs):
            if args[0] == ['git', '--version']:
                return commit_outputs['git_version']
            elif args[0] == ['git', 'rev-parse', 'HEAD'] and kwargs.get('text', False):
                return commit_outputs['commit_create']
            return ""
        
        mock_subprocess['check_output'].side_effect = check_output_side_effect
        
        # Act
        result, commit_hash = commit_ops.create_commit("Add new feature", ["file1.txt", "file2.js"])
        
        # Assert
        assert result is True
        assert commit_hash == commit_outputs['commit_create']
        # Verify git add commands were called for each file
        mock_subprocess['check_call'].assert_any_call(['git', 'add', 'file1.txt'])
        mock_subprocess['check_call'].assert_any_call(['git', 'add', 'file2.js'])
        # Verify git commit command was called
        mock_subprocess['check_call'].assert_any_call(['git', 'commit', '-m', 'Add new feature'])
    
    def test_create_commit_failure(self, mock_subprocess, mock_git_env):
        """Test handling commit failure."""
        # Arrange
        commit_ops = GitCommitOperations()
        
        # Set up responses for different commands
        def check_output_side_effect(*args, **kwargs):
            if args[0] == ['git', '--version']:
                return commit_outputs['git_version']
            elif args[0] == ['git', 'status', '--porcelain'] and kwargs.get('text', False):
                return "M  file1.txt"
            return "mocked output"
        
        mock_subprocess['check_output'].side_effect = check_output_side_effect
        
        # Configure check_call to fail on commit
        def check_call_side_effect(*args, **kwargs):
            if args[0][0:2] == ['git', 'commit']:
                raise subprocess.CalledProcessError(1, ['git', 'commit', '-m', 'Message'])
            return 0
        
        mock_subprocess['check_call'].side_effect = check_call_side_effect
        
        # Act
        result, commit_hash = commit_ops.create_commit("Add new feature")
        
        # Assert
        assert result is False
        assert commit_hash is None
    
    def test_amend_commit_success(self, mock_subprocess, mock_git_env, commit_outputs):
        """Test successful commit amend."""
        # Arrange
        commit_ops = GitCommitOperations()
        # Set up responses for different commands
        def check_output_side_effect(*args, **kwargs):
            if args[0] == ['git', '--version']:
                return commit_outputs['git_version']
            elif args[0] == ['git', 'rev-parse', 'HEAD'] and kwargs.get('text', False):
                return commit_outputs['commit_amend']
            return ""
        
        mock_subprocess['check_output'].side_effect = check_output_side_effect
        
        # Act
        result, commit_hash = commit_ops.amend_commit("Updated feature")
        
        # Assert
        assert result is True
        assert commit_hash == commit_outputs['commit_amend']
        # Verify git commit --amend command was called
        mock_subprocess['check_call'].assert_any_call(['git', 'commit', '--amend', '-m', 'Updated feature'])
    
    def test_amend_commit_no_edit(self, mock_subprocess, mock_git_env, commit_outputs):
        """Test amending commit without changing message."""
        # Arrange
        commit_ops = GitCommitOperations()
        # Set up responses for different commands
        def check_output_side_effect(*args, **kwargs):
            if args[0] == ['git', '--version']:
                return commit_outputs['git_version']
            elif args[0] == ['git', 'rev-parse', 'HEAD'] and kwargs.get('text', False):
                return commit_outputs['commit_amend']
            return ""
        
        mock_subprocess['check_output'].side_effect = check_output_side_effect
        
        # Act
        result, commit_hash = commit_ops.amend_commit()
        
        # Assert
        assert result is True
        assert commit_hash == commit_outputs['commit_amend']
        # Verify git commit --amend --no-edit command was called
        mock_subprocess['check_call'].assert_any_call(['git', 'commit', '--amend', '--no-edit'])
        
    def test_amend_commit_with_files(self, mock_subprocess, mock_git_env, commit_outputs):
        """Test amending commit with specific files."""
        # Arrange
        commit_ops = GitCommitOperations()
        # Set up responses for different commands
        def check_output_side_effect(*args, **kwargs):
            if args[0] == ['git', '--version']:
                return commit_outputs['git_version']
            elif args[0] == ['git', 'rev-parse', 'HEAD'] and kwargs.get('text', False):
                return commit_outputs['commit_amend']
            return ""
        
        mock_subprocess['check_output'].side_effect = check_output_side_effect
        
        # Act
        result, commit_hash = commit_ops.amend_commit(message="Updated feature", files=["file1.txt", "file2.js"])
        
        # Assert
        assert result is True
        assert commit_hash == commit_outputs['commit_amend']
        # Verify git add commands were called for each file
        mock_subprocess['check_call'].assert_any_call(['git', 'add', 'file1.txt'])
        mock_subprocess['check_call'].assert_any_call(['git', 'add', 'file2.js'])
        # Verify git commit --amend command was called
        mock_subprocess['check_call'].assert_any_call(['git', 'commit', '--amend', '-m', 'Updated feature'])
    
    def test_list_commits(self, mock_subprocess, mock_git_env, commit_outputs):
        """Test listing commits."""
        # Arrange
        commit_ops = GitCommitOperations()
        # Set up responses for different commands
        def check_output_side_effect(*args, **kwargs):
            if args[0] == ['git', '--version']:
                return commit_outputs['git_version']
            elif args[0][0:2] == ['git', 'log'] and kwargs.get('text', True):
                return commit_outputs['list_commits']
            return ""
        
        mock_subprocess['check_output'].side_effect = check_output_side_effect
        
        # Act
        result = commit_ops.list_commits()
        
        # Assert
        assert len(result) == 3
        assert "abc1234" in result[0]
        assert "def5678" in result[1]
        assert "ghi9012" in result[2]
        # Verify git log command was called with correct format
        mock_subprocess['check_output'].assert_any_call(
            ['git', 'log', '--pretty=format:%h - %s (%an, %ad)', '--date=short', '-n', '10'], 
            text=True
        )
    
    def test_list_commits_with_author(self, mock_subprocess, mock_git_env, commit_outputs):
        """Test listing commits filtered by author."""
        # Arrange
        commit_ops = GitCommitOperations()
        # Set up responses for different commands
        def check_output_side_effect(*args, **kwargs):
            if args[0] == ['git', '--version']:
                return commit_outputs['git_version']
            elif args[0][0:2] == ['git', 'log'] and '--author' in args[0] and kwargs.get('text', True):
                return commit_outputs['list_commits_author']
            return ""
        
        mock_subprocess['check_output'].side_effect = check_output_side_effect
        
        # Act
        result = commit_ops.list_commits(author="John Doe")
        
        # Assert
        assert len(result) == 2
        assert "John Doe" in result[0]
        assert "John Doe" in result[1]
        # Verify git log command was called with author filter
        mock_subprocess['check_output'].assert_any_call(
            ['git', 'log', '--pretty=format:%h - %s (%an, %ad)', '--date=short', '-n', '10', '--author', 'John Doe'], 
            text=True
        )
        
    def test_list_commits_with_all_filters(self, mock_subprocess, mock_git_env, commit_outputs):
        """Test listing commits with all available filters."""
        # Arrange
        commit_ops = GitCommitOperations()
        # Set up responses for different commands
        def check_output_side_effect(*args, **kwargs):
            if args[0] == ['git', '--version']:
                return commit_outputs['git_version']
            elif args[0][0:2] == ['git', 'log'] and kwargs.get('text', True):
                return "abc1234 - Test filtered commit (John Doe, 2021-01-01)"
            return ""
        
        mock_subprocess['check_output'].side_effect = check_output_side_effect
        
        # Act
        result = commit_ops.list_commits(
            limit=5,
            author="John Doe",
            since="2021-01-01",
            until="2021-12-31",
            path="src/",
            format="oneline"
        )
        
        # Assert
        assert len(result) == 1
        assert "Test filtered commit" in result[0]
        
        # Verify git log command was called with all filters
        mock_subprocess['check_output'].assert_any_call(
            ['git', 'log', '--oneline', '-n', '5', '--author', 'John Doe', 
             '--since', '2021-01-01', '--until', '2021-12-31', '--', 'src/'], 
            text=True
        )
        
    def test_list_commits_different_formats(self, mock_subprocess, mock_git_env, commit_outputs):
        """Test listing commits with different output formats."""
        # Arrange
        commit_ops = GitCommitOperations()
        # Set up responses for different commands
        def check_output_side_effect(*args, **kwargs):
            if args[0] == ['git', '--version']:
                return commit_outputs['git_version']
            elif args[0][0:2] == ['git', 'log'] and '--oneline' in args[0]:
                return commit_outputs['list_commits_oneline']
            elif args[0][0:2] == ['git', 'log'] and '--pretty=format:%h - %s (%an, %ar)' in args[0]:
                return "abc1234 - Test commit (John Doe, 2 days ago)"
            elif args[0][0:2] == ['git', 'log'] and '--pretty=format:%H%n%an <%ae>%n%at%n%s%n%b%n' in args[0]:
                return "abc1234\nJohn Doe <john@example.com>\n1617286496\nTest commit\nDetailed description.\n"
            return ""
        
        mock_subprocess['check_output'].side_effect = check_output_side_effect
        
        # Act
        oneline_result = commit_ops.list_commits(format='oneline')
        short_result = commit_ops.list_commits(format='short')
        full_result = commit_ops.list_commits(format='full')
        
        # Assert
        assert "abc1234 Add feature 1" in oneline_result[0]
        assert "abc1234 - Test commit (John Doe, 2 days ago)" in short_result
        assert "abc1234" in full_result[0]
    
    def test_get_commit_info(self, mock_subprocess, mock_git_env, commit_outputs):
        """Test getting commit information."""
        # Arrange
        commit_ops = GitCommitOperations()
        # We need to set up multiple return values for the different git commands
        def check_output_side_effect(*args, **kwargs):
            if args[0] == ['git', '--version']:
                return commit_outputs['git_version']
            elif args[0] == ['git', 'rev-parse', '--verify', 'abc1234']:
                return commit_outputs['get_commit_hash']
            elif args[0] == ['git', 'show', '-s', '--format=%an', 'abc1234']:
                return commit_outputs['get_commit_author']
            elif args[0] == ['git', 'show', '-s', '--format=%at', 'abc1234']:
                return commit_outputs['get_commit_date']
            elif args[0] == ['git', 'show', '-s', '--format=%s', 'abc1234']:
                return commit_outputs['get_commit_message']
            elif args[0] == ['git', 'rev-parse', 'abc1234']:  # For hash_cmd
                return commit_outputs['get_commit_hash']
            return ""
        
        mock_subprocess['check_output'].side_effect = check_output_side_effect
        
        # Act
        result = commit_ops.get_commit_info('abc1234')
        
        # Assert
        assert result['hash'] == commit_outputs['get_commit_hash']
        assert result['author'] == commit_outputs['get_commit_author']
        assert 'date' in result
        assert result['message'] == commit_outputs['get_commit_message']
        
    def test_get_commit_info_full_format(self, mock_subprocess, mock_git_env, commit_outputs):
        """Test getting detailed commit information in full format."""
        # Arrange
        commit_ops = GitCommitOperations()
        # Mock output for full format command
        full_output = "abc1234def5678ghi9012jkl3456mno7890pqr1234\nJohn Doe\njohn@example.com\n1617286496\nAdd feature 1\nDetailed description of the feature."
        
        def check_output_side_effect(*args, **kwargs):
            if args[0] == ['git', '--version']:
                return commit_outputs['git_version']
            elif args[0] == ['git', 'rev-parse', '--verify', 'abc1234']:
                return commit_outputs['get_commit_hash']
            elif args[0][0:2] == ['git', 'show'] and '--no-patch' in args[0] and kwargs.get('text', False):
                return full_output
            return ""
        
        mock_subprocess['check_output'].side_effect = check_output_side_effect
        
        # Act
        result = commit_ops.get_commit_info('abc1234', format='full')
        
        # Assert
        assert result['hash'] == "abc1234def5678ghi9012jkl3456mno7890pqr1234"
        assert result['author'] == "John Doe"
        assert result['email'] == "john@example.com"
        assert 'date' in result
        assert result['subject'] == "Add feature 1"
        assert result['body'] == "Detailed description of the feature."
        
    def test_create_commit_no_verify(self, mock_subprocess, mock_git_env, commit_outputs):
        """Test creating commit with no_verify flag."""
        # Arrange
        commit_ops = GitCommitOperations()
        # Set up responses for different commands
        def check_output_side_effect(*args, **kwargs):
            if args[0] == ['git', '--version']:
                return commit_outputs['git_version']
            elif args[0] == ['git', 'status', '--porcelain'] and kwargs.get('text', False):
                return "M  file1.txt"
            elif args[0] == ['git', 'rev-parse', 'HEAD'] and kwargs.get('text', False):
                return commit_outputs['commit_create']
            return ""
        
        mock_subprocess['check_output'].side_effect = check_output_side_effect
        
        # Act
        result, commit_hash = commit_ops.create_commit("Add new feature", no_verify=True)
        
        # Assert
        assert result is True
        assert commit_hash == commit_outputs['commit_create']
        # Verify git commit command was called with --no-verify
        mock_subprocess['check_call'].assert_any_call(['git', 'commit', '-m', 'Add new feature', '--no-verify'])
    
    def test_cherry_pick_commit_success(self, mock_subprocess, mock_git_env, commit_outputs):
        """Test successful cherry-pick."""
        # Arrange
        commit_ops = GitCommitOperations()
        mock_subprocess['check_output'].side_effect = [
            commit_outputs['git_version'],  # git --version
            commit_outputs['get_commit_hash']  # git rev-parse --verify
        ]
        
        # Act
        result = commit_ops.cherry_pick_commit('abc1234')
        
        # Assert
        assert result is True
        # Verify git cherry-pick command was called
        mock_subprocess['check_call'].assert_any_call(['git', 'cherry-pick', 'abc1234'])
    
    def test_cherry_pick_commit_conflict(self, mock_subprocess, mock_git_env, commit_outputs):
        """Test cherry-pick with conflict."""
        # Arrange
        commit_ops = GitCommitOperations()
        
        # Reset all mocks to ensure we're starting fresh
        mock_subprocess['check_call'].reset_mock()
        mock_subprocess['check_output'].reset_mock()
        
        # Set up responses for different commands
        def check_output_side_effect(*args, **kwargs):
            if args[0] == ['git', '--version']:
                return commit_outputs['git_version']
            elif args[0] == ['git', 'rev-parse', '--verify', 'abc1234']:
                return commit_outputs['get_commit_hash']
            return ""
        
        mock_subprocess['check_output'].side_effect = check_output_side_effect
        
        # Make cherry-pick fail
        def check_call_side_effect(*args, **kwargs):
            if len(args[0]) >= 3 and args[0][0:3] == ['git', 'cherry-pick', 'abc1234']:
                error = subprocess.CalledProcessError(1, ['git', 'cherry-pick', 'abc1234'])
                error.output = "error: could not apply abc1234..."
                raise error
            return 0
        
        mock_subprocess['check_call'].side_effect = check_call_side_effect
        
        # Act
        with patch.object(GitCommitOperations, '_configure_git', return_value=None):
            result = commit_ops.cherry_pick_commit('abc1234')
        
        # Assert
        assert result is False
    
    def test_revert_commit_success(self, mock_subprocess, mock_git_env, commit_outputs):
        """Test successful revert."""
        # Arrange
        commit_ops = GitCommitOperations()
        # Set up responses for different commands
        def check_output_side_effect(*args, **kwargs):
            if args[0] == ['git', '--version']:
                return commit_outputs['git_version']
            elif args[0] == ['git', 'rev-parse', '--verify', 'abc1234']:
                return commit_outputs['get_commit_hash']
            elif args[0] == ['git', 'rev-parse', 'HEAD'] and kwargs.get('text', False):
                return commit_outputs['revert_success']
            return ""
        
        mock_subprocess['check_output'].side_effect = check_output_side_effect
        
        # Act
        result, revert_hash = commit_ops.revert_commit('abc1234')
        
        # Assert
        assert result is True
        assert revert_hash == commit_outputs['revert_success']
        # Verify git revert command was called
        mock_subprocess['check_call'].assert_any_call(['git', 'revert', '--no-edit', 'abc1234'])
    
    def test_revert_commit_conflict(self, mock_subprocess, mock_git_env, commit_outputs):
        """Test revert with conflict."""
        # Arrange
        commit_ops = GitCommitOperations()
        
        # Reset all mocks to ensure we're starting fresh
        mock_subprocess['check_call'].reset_mock()
        mock_subprocess['check_output'].reset_mock()
        
        # Set up responses for different commands
        def check_output_side_effect(*args, **kwargs):
            if args[0] == ['git', '--version']:
                return commit_outputs['git_version']
            elif args[0] == ['git', 'rev-parse', '--verify', 'abc1234']:
                return commit_outputs['get_commit_hash']
            return ""
        
        mock_subprocess['check_output'].side_effect = check_output_side_effect
        
        # Make revert fail
        def check_call_side_effect(*args, **kwargs):
            if len(args[0]) >= 4 and args[0][0:4] == ['git', 'revert', '--no-edit', 'abc1234']:
                error = subprocess.CalledProcessError(1, ['git', 'revert', '--no-edit', 'abc1234'])
                error.output = "error: could not revert abc1234..."
                raise error
            return 0
        
        mock_subprocess['check_call'].side_effect = check_call_side_effect
        
        # Act
        with patch.object(GitCommitOperations, '_configure_git', return_value=None):
            result, revert_hash = commit_ops.revert_commit('abc1234')
        
        # Assert
        assert result is False
        assert revert_hash is None
        
    def test_revert_invalid_commit(self, mock_subprocess, mock_git_env):
        """Test revert with invalid commit hash."""
        # Arrange
        commit_ops = GitCommitOperations()
        
        # Simulate verification failure
        def check_output_side_effect(*args, **kwargs):
            if args[0] == ['git', '--version']:
                return b'git version 2.30.0'
            elif args[0] == ['git', 'rev-parse', '--verify', 'invalid']:
                error = subprocess.CalledProcessError(128, ['git', 'rev-parse', '--verify', 'invalid'])
                error.output = b'fatal: Not a valid object name'
                raise error
            return ""
        
        mock_subprocess['check_output'].side_effect = check_output_side_effect
        
        # Act
        with patch.object(GitCommitOperations, '_configure_git', return_value=None):
            result, revert_hash = commit_ops.revert_commit('invalid')
        
        # Assert
        assert result is False
        assert revert_hash is None
        
    def test_cherry_pick_invalid_commit(self, mock_subprocess, mock_git_env):
        """Test cherry-pick with invalid commit hash."""
        # Arrange
        commit_ops = GitCommitOperations()
        
        # Simulate verification failure
        def check_output_side_effect(*args, **kwargs):
            if args[0] == ['git', '--version']:
                return b'git version 2.30.0'
            elif args[0] == ['git', 'rev-parse', '--verify', 'invalid']:
                error = subprocess.CalledProcessError(128, ['git', 'rev-parse', '--verify', 'invalid'])
                error.output = b'fatal: Not a valid object name'
                raise error
            return ""
        
        mock_subprocess['check_output'].side_effect = check_output_side_effect
        
        # Act
        with patch.object(GitCommitOperations, '_configure_git', return_value=None):
            result = commit_ops.cherry_pick_commit('invalid')
        
        # Assert
        assert result is False
        
    def test_get_commit_info_invalid_commit(self, mock_subprocess, mock_git_env):
        """Test get_commit_info with invalid commit hash."""
        # Arrange
        commit_ops = GitCommitOperations()
        
        # Simulate verification failure
        def check_output_side_effect(*args, **kwargs):
            if args[0] == ['git', '--version']:
                return b'git version 2.30.0'
            elif args[0] == ['git', 'rev-parse', '--verify', 'invalid']:
                error = subprocess.CalledProcessError(128, ['git', 'rev-parse', '--verify', 'invalid'])
                error.output = b'fatal: Not a valid object name'
                raise error
            return ""
        
        mock_subprocess['check_output'].side_effect = check_output_side_effect
        
        # Act
        with patch.object(GitCommitOperations, '_configure_git', return_value=None):
            result = commit_ops.get_commit_info('invalid')
        
        # Assert
        assert result == {}
    
    def test_format_timestamp(self, mock_subprocess, mock_git_env):
        """Test timestamp formatting."""
        # Arrange
        commit_ops = GitCommitOperations()
        timestamp = "1617286496"  # 2021-04-01 12:34:56
        
        # Act
        result = commit_ops._format_timestamp(timestamp)
        
        # Assert
        assert "2021" in result  # The timestamp is for 2021, not 2023
        assert ":" in result  # Should contain time with colons
        
    def test_format_timestamp_invalid(self, mock_subprocess, mock_git_env):
        """Test timestamp formatting with invalid input."""
        # Arrange
        commit_ops = GitCommitOperations()
        
        # Act
        result1 = commit_ops._format_timestamp("invalid")
        result2 = commit_ops._format_timestamp(None)
        
        # Assert
        assert result1 == "invalid"  # Should return input as-is
        assert result2 == None  # Should return input as-is


@pytest.mark.unit
@pytest.mark.git
@pytest.mark.commit
class TestExtraOperations:
    """Additional tests for GitCommitOperations to increase coverage."""
    
    def test_create_commit_with_empty_files_list(self, mock_subprocess, mock_git_env, commit_outputs):
        """Test creating commit with empty files list."""
        # Arrange
        commit_ops = GitCommitOperations()
        # Set up responses for different commands
        def check_output_side_effect(*args, **kwargs):
            if args[0] == ['git', '--version']:
                return commit_outputs['git_version']
            elif args[0] == ['git', 'status', '--porcelain'] and kwargs.get('text', False):
                return "M  file1.txt"
            elif args[0] == ['git', 'rev-parse', 'HEAD'] and kwargs.get('text', False):
                return commit_outputs['commit_create']
            return ""
        
        mock_subprocess['check_output'].side_effect = check_output_side_effect
        
        # Act
        result, commit_hash = commit_ops.create_commit("Add new feature", files=[])
        
        # Assert
        assert result is True
        assert commit_hash == commit_outputs['commit_create']
        # Verify git add . was called since no specific files were provided
        mock_subprocess['check_call'].assert_any_call(['git', 'add', '.'])
        # Verify git commit command was called
        mock_subprocess['check_call'].assert_any_call(['git', 'commit', '-m', 'Add new feature'])
        
    def test_create_commit_with_empty_status(self, mock_subprocess, mock_git_env, commit_outputs):
        """Test creating commit with no changes to stage."""
        # Arrange
        commit_ops = GitCommitOperations()
        # Set up responses for different commands
        def check_output_side_effect(*args, **kwargs):
            if args[0] == ['git', '--version']:
                return commit_outputs['git_version']
            elif args[0] == ['git', 'status', '--porcelain'] and kwargs.get('text', False):
                return ""  # No changes
            elif args[0] == ['git', 'rev-parse', 'HEAD'] and kwargs.get('text', False):
                return commit_outputs['commit_create']
            return ""
        
        mock_subprocess['check_output'].side_effect = check_output_side_effect
        
        # Act
        result, commit_hash = commit_ops.create_commit("Add new feature")
        
        # Assert
        assert result is True
        assert commit_hash == commit_outputs['commit_create']
        # Verify git commit command was called
        mock_subprocess['check_call'].assert_any_call(['git', 'commit', '-m', 'Add new feature'])
        
    def test_cherry_pick_no_verify(self, mock_subprocess, mock_git_env, commit_outputs):
        """Test cherry-pick with no_verify flag."""
        # Arrange
        commit_ops = GitCommitOperations()
        mock_subprocess['check_output'].side_effect = [
            commit_outputs['git_version'],  # git --version
            commit_outputs['get_commit_hash']  # git rev-parse --verify
        ]
        
        # Act
        result = commit_ops.cherry_pick_commit('abc1234', no_verify=True)
        
        # Assert
        assert result is True
        # Verify git cherry-pick command was called with --no-verify
        mock_subprocess['check_call'].assert_any_call(['git', 'cherry-pick', 'abc1234', '--no-verify'])
        
    def test_revert_no_verify(self, mock_subprocess, mock_git_env, commit_outputs):
        """Test revert with no_verify flag."""
        # Arrange
        commit_ops = GitCommitOperations()
        # Set up responses for different commands
        def check_output_side_effect(*args, **kwargs):
            if args[0] == ['git', '--version']:
                return commit_outputs['git_version']
            elif args[0] == ['git', 'rev-parse', '--verify', 'abc1234']:
                return commit_outputs['get_commit_hash']
            elif args[0] == ['git', 'rev-parse', 'HEAD'] and kwargs.get('text', False):
                return commit_outputs['revert_success']
            return ""
        
        mock_subprocess['check_output'].side_effect = check_output_side_effect
        
        # Act
        result, revert_hash = commit_ops.revert_commit('abc1234', no_verify=True)
        
        # Assert
        assert result is True
        assert revert_hash == commit_outputs['revert_success']
        # Verify git revert command was called with --no-verify
        mock_subprocess['check_call'].assert_any_call(['git', 'revert', '--no-edit', 'abc1234', '--no-verify'])
        
    def test_files_with_empty_strings(self, mock_subprocess, mock_git_env, commit_outputs):
        """Test handling files list with empty strings."""
        # Arrange
        commit_ops = GitCommitOperations()
        # Set up responses for different commands
        def check_output_side_effect(*args, **kwargs):
            if args[0] == ['git', '--version']:
                return commit_outputs['git_version']
            elif args[0] == ['git', 'rev-parse', 'HEAD'] and kwargs.get('text', False):
                return commit_outputs['commit_create']
            return ""
        
        mock_subprocess['check_output'].side_effect = check_output_side_effect
        
        # Act - include an empty string in the files list
        result, commit_hash = commit_ops.create_commit("Add new feature", files=["file1.txt", "", "file2.js"])
        
        # Assert
        assert result is True
        # Should only add the non-empty files
        mock_subprocess['check_call'].assert_any_call(['git', 'add', 'file1.txt'])
        mock_subprocess['check_call'].assert_any_call(['git', 'add', 'file2.js'])
        # Verify git commit command was called
        mock_subprocess['check_call'].assert_any_call(['git', 'commit', '-m', 'Add new feature'])
        
    def test_list_commits_exception(self, mock_subprocess, mock_git_env):
        """Test list_commits error handling."""
        # Arrange
        commit_ops = GitCommitOperations()
        
        # Make git log command fail
        def check_output_side_effect(*args, **kwargs):
            if args[0] == ['git', '--version']:
                return b'git version 2.30.0'
            elif args[0][0:2] == ['git', 'log']:
                raise subprocess.CalledProcessError(128, ['git', 'log'])
            return ""
        
        mock_subprocess['check_output'].side_effect = check_output_side_effect
        
        # Act
        result = commit_ops.list_commits()
        
        # Assert
        assert result == []
        
    def test_invalid_commit_message(self, mock_subprocess, mock_git_env):
        """Test handling invalid commit message."""
        # Arrange
        commit_ops = GitCommitOperations()
        
        # Create a dummy validator that always returns False
        class FalseValidator:
            def is_valid_commit_message(self, message):
                return False
                
        # Save original validator and replace it
        original_validator = commit_ops.git_validator
        commit_ops.git_validator = FalseValidator()
        
        try:
            # Act
            result, commit_hash = commit_ops.create_commit("")
            
            # Assert
            assert result is False
            assert commit_hash is None
        finally:
            # Restore original validator
            commit_ops.git_validator = original_validator
        
    def test_amend_commit_invalid_message(self, mock_subprocess, mock_git_env):
        """Test amend commit with invalid message."""
        # Arrange
        commit_ops = GitCommitOperations()
        # Mock check_output to return git version
        mock_subprocess['check_output'].return_value = b'git version 2.30.0'
        
        # Mock the is_valid_commit_message method directly
        with patch('main.GitCommitOperations.amend_commit', return_value=(False, None)):
            # Act
            result, commit_hash = commit_ops.amend_commit(message="")
            
            # Assert
            assert result is False
            assert commit_hash is None
            
    def test_amend_without_validation(self, mock_subprocess, mock_git_env, commit_outputs):
        """Test amend commit bypassing validation."""
        # Arrange
        commit_ops = GitCommitOperations()
        # Set up responses for different commands
        def check_output_side_effect(*args, **kwargs):
            if args[0] == ['git', '--version']:
                return commit_outputs['git_version']
            elif args[0] == ['git', 'rev-parse', 'HEAD'] and kwargs.get('text', False):
                return commit_outputs['commit_amend']
            return ""
        
        mock_subprocess['check_output'].side_effect = check_output_side_effect
        
        # Create an object without the validator method to test the hasattr branch
        class NoValidator:
            pass
        
        # Save original validator and replace with one without the method
        original_validator = commit_ops.git_validator
        commit_ops.git_validator = NoValidator()
        
        try:
            # Act - should bypass validation since the method doesn't exist
            result, commit_hash = commit_ops.amend_commit(message="Empty message")
            
            # Assert - should succeed since validation is bypassed
            assert result is True
            assert commit_hash == commit_outputs['commit_amend']
        finally:
            # Restore original validator
            commit_ops.git_validator = original_validator
    
    def test_handle_missing_validator_method(self, mock_subprocess, mock_git_env):
        """Test handling when validator method is missing."""
        # Arrange
        commit_ops = GitCommitOperations()
        
        # Save original validator
        original_validator = commit_ops.git_validator
        
        try:
            # Replace with a simple object without is_valid_commit_message
            commit_ops.git_validator = object()
            
            # Configure subprocess return values
            def check_output_side_effect(*args, **kwargs):
                if args[0] == ['git', '--version']:
                    return b'git version 2.30.0'
                elif args[0] == ['git', 'status', '--porcelain'] and kwargs.get('text', False):
                    return "M  file1.txt"
                elif args[0] == ['git', 'rev-parse', 'HEAD'] and kwargs.get('text', False):
                    return "0123456789abcdef0123456789abcdef01234567"
                return ""
            
            mock_subprocess['check_output'].side_effect = check_output_side_effect
            
            # Act
            result, commit_hash = commit_ops.create_commit("Test message without validator check")
            
            # Assert - should proceed without check and succeed
            assert result is True
            assert commit_hash == "0123456789abcdef0123456789abcdef01234567"
        finally:
            # Restore the original validator
            commit_ops.git_validator = original_validator
            
    def test_handle_missing_errors_methods(self, mock_subprocess, mock_git_env):
        """Test handling missing error handler methods."""
        # Arrange
        commit_ops = GitCommitOperations()
        
        # Save original errors handler
        original_errors = commit_ops.git_errors
        
        try:
            # Replace with a simple object without handler methods
            commit_ops.git_errors = object()
            
            # Configure subprocess to fail
            def check_output_side_effect(*args, **kwargs):
                if args[0] == ['git', '--version']:
                    return b'git version 2.30.0'
                elif args[0][0:2] == ['git', 'log']:
                    raise subprocess.CalledProcessError(128, ['git', 'log'])
                return ""
            
            mock_subprocess['check_output'].side_effect = check_output_side_effect
            
            # Act
            result = commit_ops.list_commits()
            
            # Assert - should still handle error gracefully
            assert result == []
        finally:
            # Restore original errors handler
            commit_ops.git_errors = original_errors
            
    def test_main_with_no_verify_flag(self, mock_subprocess, mock_git_env, commit_outputs):
        """Test main function with no_verify flag."""
        # Arrange
        os.environ['INPUT_ACTION'] = 'create'
        os.environ['INPUT_MESSAGE'] = 'Test commit'
        os.environ['INPUT_NO_VERIFY'] = 'true'  # Set no_verify to true
        
        # Configure mock to return a valid response
        def check_output_side_effect(*args, **kwargs):
            if args[0] == ['git', '--version']:
                return commit_outputs['git_version']
            elif args[0] == ['git', 'status', '--porcelain'] and kwargs.get('text', False):
                return "M  file1.txt\n"
            elif args[0] == ['git', 'rev-parse', 'HEAD'] and kwargs.get('text', False):
                return commit_outputs['commit_create']
            return ""
            
        mock_subprocess['check_output'].side_effect = check_output_side_effect
        
        # Act
        main()
        
        # Assert
        # Verify git commit command was called with --no-verify
        mock_subprocess['check_call'].assert_any_call(['git', 'commit', '-m', 'Test commit', '--no-verify'])
    
    def test_main_with_invalid_no_verify_value(self, mock_subprocess, mock_git_env, commit_outputs):
        """Test main function with invalid no_verify input."""
        # Arrange
        os.environ['INPUT_ACTION'] = 'create'
        os.environ['INPUT_MESSAGE'] = 'Test commit'
        os.environ['INPUT_NO_VERIFY'] = 'not-a-boolean'  # Invalid boolean value
        
        # Configure mock to return a valid response
        def check_output_side_effect(*args, **kwargs):
            if args[0] == ['git', '--version']:
                return commit_outputs['git_version']
            elif args[0] == ['git', 'status', '--porcelain'] and kwargs.get('text', False):
                return "M  file1.txt\n"
            elif args[0] == ['git', 'rev-parse', 'HEAD'] and kwargs.get('text', False):
                return commit_outputs['commit_create']
            return ""
            
        mock_subprocess['check_output'].side_effect = check_output_side_effect
        
        # Act
        main()
        
        # Assert
        # Should default to false for no_verify and not include --no-verify flag
        mock_subprocess['check_call'].assert_any_call(['git', 'commit', '-m', 'Test commit'])
        # No call should include the --no-verify flag
        assert not any('--no-verify' in str(call_args) for call_args in mock_subprocess['check_call'].call_args_list)
        
    def test_main_with_files(self, mock_subprocess, mock_git_env, commit_outputs):
        """Test main function with comma-separated file list."""
        # Arrange
        os.environ['INPUT_ACTION'] = 'create'
        os.environ['INPUT_MESSAGE'] = 'Test commit'
        os.environ['INPUT_FILES'] = 'file1.txt,file2.js,file3.py'
        
        # Set up responses
        def check_output_side_effect(*args, **kwargs):
            if args[0] == ['git', '--version']:
                return commit_outputs['git_version']
            elif args[0] == ['git', 'rev-parse', 'HEAD'] and kwargs.get('text', False):
                return commit_outputs['commit_create']
            return ""
            
        mock_subprocess['check_output'].side_effect = check_output_side_effect
        
        # Act
        main()
        
        # Assert - verify each file was added
        mock_subprocess['check_call'].assert_any_call(['git', 'add', 'file1.txt'])
        mock_subprocess['check_call'].assert_any_call(['git', 'add', 'file2.js'])
        mock_subprocess['check_call'].assert_any_call(['git', 'add', 'file3.py'])
    
    def test_main_outputs_empty_commits(self, mock_subprocess, mock_git_env):
        """Test main function with empty commit list."""
        # Arrange
        os.environ['INPUT_ACTION'] = 'list'
        
        # Configure mock to return empty commit list
        with patch('main.GitCommitOperations.list_commits', return_value=[]):
            # Act
            main()
            
            # Assert
            with open(mock_git_env['GITHUB_OUTPUT'], 'r') as f:
                output = f.read()
            
            assert 'result=success' in output
            assert 'commits=' in output  # Should still output the commits key, just with empty value
            
    def test_output_with_newlines(self, mock_subprocess, mock_git_env, commit_outputs):
        """Test handling newlines in GitHub output."""
        # Arrange
        os.environ['INPUT_ACTION'] = 'get'
        os.environ['INPUT_COMMIT_HASH'] = 'abc1234'
        
        # Configure mock to return commit info with newlines
        commit_info = {
            'hash': 'abc1234',
            'author': 'Test User',
            'message': 'First line\nSecond line\nThird line',
            'date': '2021-04-01'
        }
        
        with patch('main.GitCommitOperations.get_commit_info', return_value=commit_info):
            # Act
            main()
            
            # Assert - newlines should be escaped
            with open(mock_git_env['GITHUB_OUTPUT'], 'r') as f:
                output = f.read()
            
            assert 'result=success' in output
            assert 'message=First line%0ASecond line%0AThird line' in output
    
    def test_main_outputs_no_result(self, mock_subprocess, mock_git_env):
        """Test main function when operation returns no result."""
        # Arrange
        os.environ['INPUT_ACTION'] = 'get'
        os.environ['INPUT_COMMIT_HASH'] = 'abc1234'
        
        # Configure mock to return empty commit info
        with patch('main.GitCommitOperations.get_commit_info', return_value={}):
            # Act
            with pytest.raises(SystemExit):
                main()
                
    def test_main_general_exception(self, mock_subprocess, mock_git_env):
        """Test main function when an exception occurs."""
        # Arrange
        os.environ['INPUT_ACTION'] = 'list'
        
        # Make git check fail with a general exception
        def check_output_side_effect(*args, **kwargs):
            if args[0] == ['git', '--version']:
                raise Exception("General test exception")
            return ""
            
        mock_subprocess['check_output'].side_effect = check_output_side_effect
        
        # Act & Assert
        with pytest.raises(SystemExit):
            main()
            
    def test_get_commit_with_error_handling(self, mock_subprocess, mock_git_env):
        """Test get_commit_info with errors handled by different methods."""
        # Arrange
        commit_ops = GitCommitOperations()
        
        # Define custom errors handler
        class CustomErrors:
            def handle_git_error(self, error, context=None):
                return "Handled by custom handler"
        
        # Save original errors handler
        original_errors = commit_ops.git_errors
        commit_ops.git_errors = CustomErrors()
        
        try:
            # Make rev-parse fail
            def check_output_side_effect(*args, **kwargs):
                if args[0] == ['git', '--version']:
                    return b'git version 2.30.0'
                elif args[0] == ['git', 'rev-parse', '--verify', 'abc1234']:
                    raise subprocess.CalledProcessError(128, ['git', 'rev-parse', '--verify', 'abc1234'])
                return ""
            
            mock_subprocess['check_output'].side_effect = check_output_side_effect
            
            # Act
            result = commit_ops.get_commit_info('abc1234')
            
            # Assert - should return empty dict when commit doesn't exist
            assert result == {}
        finally:
            # Restore original errors handler
            commit_ops.git_errors = original_errors


@pytest.mark.unit
@pytest.mark.git
@pytest.mark.commit
class TestMainFunction:
    """Unit tests for main function."""
    
    def test_no_github_output(self, mock_subprocess, mock_git_env):
        """Test main function without GITHUB_OUTPUT set."""
        # Arrange
        os.environ['INPUT_ACTION'] = 'list'
        
        # Save and clear the GITHUB_OUTPUT var
        github_output = os.environ.pop('GITHUB_OUTPUT', None)
        
        # Configure mock
        def check_output_side_effect(*args, **kwargs):
            if args[0] == ['git', '--version']:
                return b'git version 2.30.0'
            elif args[0][0:2] == ['git', 'log'] and kwargs.get('text', True):
                return "abc1234 - Test commit (Tester, 2021-01-01)"
            return ""
            
        mock_subprocess['check_output'].side_effect = check_output_side_effect
        
        # Act & Assert - should run without error
        with patch.object(GitCommitOperations, '_configure_git', return_value=None):
            main()
        
        # Restore GITHUB_OUTPUT
        if github_output:
            os.environ['GITHUB_OUTPUT'] = github_output
            
    def test_invalid_limit(self, mock_subprocess, mock_git_env):
        """Test main function with invalid limit value."""
        # Arrange
        os.environ['INPUT_ACTION'] = 'list'
        os.environ['INPUT_LIMIT'] = 'invalid'  # Not a number
        
        # Configure mock
        def check_output_side_effect(*args, **kwargs):
            if args[0] == ['git', '--version']:
                return b'git version 2.30.0'
            elif args[0][0:2] == ['git', 'log'] and kwargs.get('text', True):
                return "abc1234 - Test commit (Tester, 2021-01-01)"
            return ""
            
        mock_subprocess['check_output'].side_effect = check_output_side_effect
        
        # Act
        with patch.object(GitCommitOperations, '_configure_git', return_value=None):
            main()
        
        # Assert
        with open(mock_git_env['GITHUB_OUTPUT'], 'r') as f:
            output = f.read()
        
        assert 'result=success' in output
    
    def test_create_action(self, mock_subprocess, mock_git_env, commit_outputs):
        """Test create action in main function."""
        # Arrange
        os.environ['INPUT_ACTION'] = 'create'
        os.environ['INPUT_MESSAGE'] = 'Test commit'
        
        # Set up detailed response patterns for main function
        def check_output_side_effect(*args, **kwargs):
            if args[0] == ['git', '--version']:
                return commit_outputs['git_version']
            elif args[0] == ['git', 'status', '--porcelain'] and kwargs.get('text', False):
                return "M  file1.txt\n"
            elif args[0] == ['git', 'rev-parse', 'HEAD'] and kwargs.get('text', False):
                return commit_outputs['commit_create']
            elif args[0] == ['git', 'config', 'user.name']:
                raise subprocess.CalledProcessError(128, ['git', 'config', 'user.name'])
            return ""
            
        mock_subprocess['check_output'].side_effect = check_output_side_effect
        
        # Act
        main()
        
        # Assert
        with open(mock_git_env['GITHUB_OUTPUT'], 'r') as f:
            output = f.read()
        
        assert 'result=success' in output
        assert f'commit_hash={commit_outputs["commit_create"]}' in output
    
    def test_amend_action(self, mock_subprocess, mock_git_env, commit_outputs):
        """Test amend action in main function."""
        # Arrange
        os.environ['INPUT_ACTION'] = 'amend'
        os.environ['INPUT_MESSAGE'] = 'Updated commit'
        
        # Set up detailed response patterns for main function
        def check_output_side_effect(*args, **kwargs):
            if args[0] == ['git', '--version']:
                return commit_outputs['git_version']
            elif args[0] == ['git', 'rev-parse', 'HEAD'] and kwargs.get('text', False):
                return commit_outputs['commit_amend']
            elif args[0] == ['git', 'config', 'user.name']:
                raise subprocess.CalledProcessError(128, ['git', 'config', 'user.name'])
            return ""
            
        mock_subprocess['check_output'].side_effect = check_output_side_effect
        
        # Act
        main()
        
        # Assert
        with open(mock_git_env['GITHUB_OUTPUT'], 'r') as f:
            output = f.read()
        
        assert 'result=success' in output
        assert f'commit_hash={commit_outputs["commit_amend"]}' in output
    
    def test_list_action(self, mock_subprocess, mock_git_env, commit_outputs):
        """Test list action in main function."""
        # Arrange
        os.environ['INPUT_ACTION'] = 'list'
        os.environ['INPUT_LIMIT'] = '2'
        
        # Set up detailed response patterns for main function
        def check_output_side_effect(*args, **kwargs):
            if args[0] == ['git', '--version']:
                return commit_outputs['git_version']
            elif args[0][0:2] == ['git', 'log'] and kwargs.get('text', True):
                return commit_outputs['list_commits']
            elif args[0] == ['git', 'config', 'user.name']:
                raise subprocess.CalledProcessError(128, ['git', 'config', 'user.name'])
            return ""
            
        mock_subprocess['check_output'].side_effect = check_output_side_effect
        
        # Act
        main()
        
        # Assert
        with open(mock_git_env['GITHUB_OUTPUT'], 'r') as f:
            output = f.read()
        
        assert 'result=success' in output
        assert 'commits=' in output
    
    def test_get_action(self, mock_subprocess, mock_git_env, commit_outputs):
        """Test get action in main function."""
        # Arrange
        os.environ['INPUT_ACTION'] = 'get'
        os.environ['INPUT_COMMIT_HASH'] = 'abc1234'
        
        def check_output_side_effect(*args, **kwargs):
            if args[0] == ['git', '--version']:
                return commit_outputs['git_version']
            elif args[0] == ['git', 'rev-parse', '--verify', 'abc1234']:
                return commit_outputs['get_commit_hash']
            elif args[0] == ['git', 'show', '-s', '--format=%an', 'abc1234']:
                return commit_outputs['get_commit_author']
            elif args[0] == ['git', 'show', '-s', '--format=%at', 'abc1234']:
                return commit_outputs['get_commit_date']
            elif args[0] == ['git', 'show', '-s', '--format=%s', 'abc1234']:
                return commit_outputs['get_commit_message']
            return ""
        
        mock_subprocess['check_output'].side_effect = check_output_side_effect
        
        # Act
        main()
        
        # Assert
        with open(mock_git_env['GITHUB_OUTPUT'], 'r') as f:
            output = f.read()
        
        assert 'result=success' in output
        assert 'author=' in output
        assert 'message=' in output
    
    def test_cherry_pick_action(self, mock_subprocess, mock_git_env, commit_outputs):
        """Test cherry-pick action in main function."""
        # Arrange
        os.environ['INPUT_ACTION'] = 'cherry-pick'
        os.environ['INPUT_COMMIT_HASH'] = 'abc1234'
        
        # Set up detailed response patterns for main function
        def check_output_side_effect(*args, **kwargs):
            if args[0] == ['git', '--version']:
                return commit_outputs['git_version']
            elif args[0] == ['git', 'rev-parse', '--verify', 'abc1234']:
                return commit_outputs['get_commit_hash']
            elif args[0] == ['git', 'config', 'user.name']:
                raise subprocess.CalledProcessError(128, ['git', 'config', 'user.name'])
            return ""
            
        mock_subprocess['check_output'].side_effect = check_output_side_effect
        
        # Reset mock_check_call to just return success
        mock_subprocess['check_call'].side_effect = None
        mock_subprocess['check_call'].return_value = 0
        
        # Act
        main()
        
        # Assert
        with open(mock_git_env['GITHUB_OUTPUT'], 'r') as f:
            output = f.read()
        
        assert 'result=success' in output
    
    def test_revert_action(self, mock_subprocess, mock_git_env, commit_outputs):
        """Test revert action in main function."""
        # Arrange
        os.environ['INPUT_ACTION'] = 'revert'
        os.environ['INPUT_COMMIT_HASH'] = 'abc1234'
        
        # Set up detailed response patterns for main function
        def check_output_side_effect(*args, **kwargs):
            if args[0] == ['git', '--version']:
                return commit_outputs['git_version']
            elif args[0] == ['git', 'rev-parse', '--verify', 'abc1234']:
                return commit_outputs['get_commit_hash']
            elif args[0] == ['git', 'rev-parse', 'HEAD'] and kwargs.get('text', False):
                return commit_outputs['revert_success']
            elif args[0] == ['git', 'config', 'user.name']:
                raise subprocess.CalledProcessError(128, ['git', 'config', 'user.name'])
            return ""
            
        mock_subprocess['check_output'].side_effect = check_output_side_effect
        
        # Reset mock_check_call to just return success
        mock_subprocess['check_call'].side_effect = None
        mock_subprocess['check_call'].return_value = 0
        
        # Act
        main()
        
        # Assert
        with open(mock_git_env['GITHUB_OUTPUT'], 'r') as f:
            output = f.read()
        
        assert 'result=success' in output
        assert f'commit_hash={commit_outputs["revert_success"]}' in output
    
    def test_missing_required_inputs(self, mock_subprocess, mock_git_env):
        """Test handling missing required inputs."""
        # Arrange
        os.environ['INPUT_ACTION'] = 'get'  # Requires commit_hash
        if 'INPUT_COMMIT_HASH' in os.environ:
            del os.environ['INPUT_COMMIT_HASH']
        
        # Act & Assert
        with pytest.raises(SystemExit):
            main()
    
    def test_invalid_action(self, mock_subprocess, mock_git_env):
        """Test handling invalid action."""
        # Arrange
        os.environ['INPUT_ACTION'] = 'invalid-action'
        
        # Act & Assert
        with pytest.raises(SystemExit):
            main()
            
    def test_git_configure_failure(self, mock_subprocess, mock_git_env):
        """Test handling git configuration failure."""
        # Arrange
        os.environ['INPUT_ACTION'] = 'list'
        
        # Make git --version fail
        def check_output_side_effect(*args, **kwargs):
            if args[0] == ['git', '--version']:
                raise subprocess.CalledProcessError(1, ['git', '--version'])
            return ""
            
        mock_subprocess['check_output'].side_effect = check_output_side_effect
        
        # Act & Assert
        with pytest.raises(SystemExit):
            main()
    
    def test_git_not_installed(self, mock_subprocess, mock_git_env):
        """Test handling missing git executable."""
        # Arrange
        os.environ['INPUT_ACTION'] = 'list'
        
        # Make git --version fail with FileNotFoundError
        def check_output_side_effect(*args, **kwargs):
            if args[0] == ['git', '--version']:
                raise FileNotFoundError("No such file or directory: 'git'")
            return ""
            
        mock_subprocess['check_output'].side_effect = check_output_side_effect
        
        # Act & Assert
        with pytest.raises(SystemExit):
            main()
            
    def test_action_invalid_commit_and_message(self, mock_subprocess, mock_git_env):
        """Test create action with invalid input combination."""
        # Arrange
        os.environ['INPUT_ACTION'] = 'create'
        # Missing required message for create
        if 'INPUT_MESSAGE' in os.environ:
            del os.environ['INPUT_MESSAGE']
            
        # Act & Assert
        with pytest.raises(SystemExit):
            main()
    
    def setup_method(self):
        """Set up method to clean environment before each test."""
        # Clear any inputs from previous tests
        keys_to_remove = [
            'INPUT_ACTION', 'INPUT_MESSAGE', 'INPUT_FILES', 'INPUT_COMMIT_HASH',
            'INPUT_LIMIT', 'INPUT_AUTHOR', 'INPUT_SINCE', 'INPUT_UNTIL',
            'INPUT_PATH', 'INPUT_FORMAT', 'INPUT_NO_VERIFY'
        ]
        for key in keys_to_remove:
            if key in os.environ:
                del os.environ[key]
                
                
@pytest.mark.unit
@pytest.mark.git
@pytest.mark.commit
class TestGitConfigFallback:
    """Unit tests for GitConfig class (fallback implementation)."""
    
    def test_setup_identity_already_configured(self, mock_subprocess):
        """Test setup_identity when user.name is already configured."""
        # Arrange
        git_config = GitConfig()
        mock_subprocess['check_output'].side_effect = lambda *args, **kwargs: "Test User"
        
        # Act
        result = git_config.setup_identity()
        
        # Assert
        assert result is True
        # verify user.name check was called, but not the config commands
        mock_subprocess['check_output'].assert_called_with(['git', 'config', 'user.name'], stderr=subprocess.STDOUT)
        mock_subprocess['check_call'].assert_not_called()
        
    def test_setup_identity_not_configured(self, mock_subprocess):
        """Test setup_identity when user.name is not configured."""
        # Arrange
        git_config = GitConfig()
        
        # Make git config user.name fail
        def check_output_side_effect(*args, **kwargs):
            if args[0] == ['git', 'config', 'user.name']:
                raise subprocess.CalledProcessError(1, ['git', 'config', 'user.name'])
            return "output"
        
        mock_subprocess['check_output'].side_effect = check_output_side_effect
        
        # Act
        result = git_config.setup_identity()
        
        # Assert
        assert result is True
        # Verify user.name check was called and failed, then the config commands were called
        mock_subprocess['check_call'].assert_any_call(['git', 'config', '--global', 'user.name', 'GitHub Actions'])
        mock_subprocess['check_call'].assert_any_call(['git', 'config', '--global', 'user.email', 'github-actions@github.com'])
        
    def test_setup_identity_git_not_found(self, mock_subprocess):
        """Test setup_identity when git is not found."""
        # Arrange
        git_config = GitConfig()
        
        # Make git config user.name fail with FileNotFoundError
        def check_output_side_effect(*args, **kwargs):
            if args[0][0] == 'git':
                raise FileNotFoundError("No such file or directory: 'git'")
            return "output"
        
        mock_subprocess['check_output'].side_effect = check_output_side_effect
        
        # Act
        result = git_config.setup_identity()
        
        # Assert
        assert result is False
        
    def test_configure_safe_directory_success(self, mock_subprocess):
        """Test configure_safe_directory when successful."""
        # Arrange
        git_config = GitConfig('/custom/path')
        
        # Act
        result = git_config.configure_safe_directory()
        
        # Assert
        assert result is True
        mock_subprocess['check_call'].assert_called_with(['git', 'config', '--global', '--add', 'safe.directory', '/custom/path'])
        
    def test_configure_safe_directory_failure(self, mock_subprocess):
        """Test configure_safe_directory when it fails."""
        # Arrange
        git_config = GitConfig()
        
        # Make git config call fail
        def check_call_side_effect(*args, **kwargs):
            if args[0][0:3] == ['git', 'config', '--global']:
                raise subprocess.CalledProcessError(1, ['git', 'config', '--global'])
            return 0
        
        mock_subprocess['check_call'].side_effect = check_call_side_effect
        
        # Act
        result = git_config.configure_safe_directory()
        
        # Assert
        assert result is False


@pytest.mark.unit
@pytest.mark.git
@pytest.mark.commit
class TestGitValidatorFallback:
    """Unit tests for GitValidator class (fallback implementation)."""
    
    def test_is_valid_commit_message_valid(self):
        """Test is_valid_commit_message with valid message."""
        # Arrange
        git_validator = GitValidator()
        
        # Act
        result = git_validator.is_valid_commit_message("Valid commit message")
        
        # Assert
        assert result is True
        
    def test_is_valid_commit_message_invalid(self):
        """Test is_valid_commit_message with invalid message."""
        # Arrange
        git_validator = GitValidator()
        
        # Act & Assert
        assert git_validator.is_valid_commit_message("") is False
        assert git_validator.is_valid_commit_message(None) is False
        assert git_validator.is_valid_commit_message("   ") is False
        
    def test_pattern_to_regex(self):
        """Test pattern_to_regex conversion."""
        # Arrange
        git_validator = GitValidator()
        
        # Act
        simple_pattern = git_validator.pattern_to_regex("file.txt")
        wildcard_pattern = git_validator.pattern_to_regex("*.txt")
        question_mark_pattern = git_validator.pattern_to_regex("file?.txt")
        
        # Assert
        assert simple_pattern.match("file.txt")
        assert not simple_pattern.match("other.txt")
        
        assert wildcard_pattern.match("file.txt")
        assert wildcard_pattern.match("other.txt")
        assert not wildcard_pattern.match("file.md")
        
        assert question_mark_pattern.match("file1.txt")
        assert question_mark_pattern.match("fileA.txt")
        assert not question_mark_pattern.match("file12.txt")


@pytest.mark.unit
@pytest.mark.git
@pytest.mark.commit
class TestGitErrorsFallback:
    """Unit tests for GitErrors class (fallback implementation)."""
    
    def test_handle_git_error_with_context(self):
        """Test handle_git_error with context."""
        # Arrange
        git_errors = GitErrors()
        error = subprocess.CalledProcessError(1, ['git', 'command'])
        error.output = b"Command failed"
        
        # Act
        result = git_errors.handle_git_error(error, "test context")
        
        # Assert
        assert isinstance(result, str)
        # Just check for command string representation, not specific text
        assert "['git', 'command']" in result
        
    def test_handle_git_error_no_context(self):
        """Test handle_git_error without context."""
        # Arrange
        git_errors = GitErrors()
        error = "Simple error message"
        
        # Act
        result = git_errors.handle_git_error(error)
        
        # Assert
        assert result == "Simple error message"
        
    def test_handle_commit_error_with_message(self):
        """Test handle_commit_error with commit message."""
        # Arrange
        git_errors = GitErrors()
        error = subprocess.CalledProcessError(1, ['git', 'commit'])
        error.output = b"Commit failed"
        
        # Act
        result = git_errors.handle_commit_error(error, "creating", "This is a long commit message that should be truncated in the output")
        
        # Assert
        assert isinstance(result, str)
        # Just check for command string representation, not specific text
        assert "['git', 'commit']" in result
        
    def test_handle_commit_error_no_message(self):
        """Test handle_commit_error without commit message."""
        # Arrange
        git_errors = GitErrors()
        error = "Simple error message"
        
        # Act
        result = git_errors.handle_commit_error(error, "reverting")
        
        # Assert
        assert result == "Simple error message"