#!/usr/bin/env python3

import pytest
import os
import sys
import subprocess
from unittest.mock import call, patch

# Add parent directory to path to import module under test
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the module under test
from main import GitCommitOperations, main


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
        assert "Test commit (John Doe, 2 days ago)" in short_result
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