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
        mock_subprocess['check_output'].side_effect = [
            commit_outputs['git_version'],  # git --version
            commit_outputs['commit_create']  # git rev-parse HEAD
        ]
        
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
        mock_subprocess['check_output'].side_effect = [
            commit_outputs['git_version'],  # git --version
            commit_outputs['commit_create']  # git rev-parse HEAD
        ]
        
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
        mock_subprocess['check_call'].side_effect = [
            0,  # git config successful
            0,  # git add successful
            subprocess.CalledProcessError(1, ['git', 'commit', '-m', 'Message'])  # git commit fails
        ]
        
        # Act
        result, commit_hash = commit_ops.create_commit("Add new feature")
        
        # Assert
        assert result is False
        assert commit_hash is None
    
    def test_amend_commit_success(self, mock_subprocess, mock_git_env, commit_outputs):
        """Test successful commit amend."""
        # Arrange
        commit_ops = GitCommitOperations()
        mock_subprocess['check_output'].side_effect = [
            commit_outputs['git_version'],  # git --version
            commit_outputs['commit_amend']  # git rev-parse HEAD
        ]
        
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
        mock_subprocess['check_output'].side_effect = [
            commit_outputs['git_version'],  # git --version
            commit_outputs['commit_amend']  # git rev-parse HEAD
        ]
        
        # Act
        result, commit_hash = commit_ops.amend_commit()
        
        # Assert
        assert result is True
        assert commit_hash == commit_outputs['commit_amend']
        # Verify git commit --amend --no-edit command was called
        mock_subprocess['check_call'].assert_any_call(['git', 'commit', '--amend', '--no-edit'])
    
    def test_list_commits(self, mock_subprocess, mock_git_env, commit_outputs):
        """Test listing commits."""
        # Arrange
        commit_ops = GitCommitOperations()
        mock_subprocess['check_output'].side_effect = [
            commit_outputs['git_version'],  # git --version
            commit_outputs['list_commits']  # git log
        ]
        
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
        mock_subprocess['check_output'].side_effect = [
            commit_outputs['git_version'],  # git --version
            commit_outputs['list_commits_author']  # git log --author
        ]
        
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
            return ""
        
        mock_subprocess['check_output'].side_effect = check_output_side_effect
        
        # Act
        result = commit_ops.get_commit_info('abc1234')
        
        # Assert
        assert result['hash'] == commit_outputs['get_commit_hash']
        assert result['author'] == commit_outputs['get_commit_author']
        assert 'date' in result
        assert result['message'] == commit_outputs['get_commit_message']
    
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
        mock_subprocess['check_output'].side_effect = [
            commit_outputs['git_version'],  # git --version
            commit_outputs['get_commit_hash']  # git rev-parse --verify
        ]
        mock_subprocess['check_call'].side_effect = [
            0,  # git config successful
            subprocess.CalledProcessError(1, ['git', 'cherry-pick', 'abc1234'])  # cherry-pick fails
        ]
        
        # Act
        result = commit_ops.cherry_pick_commit('abc1234')
        
        # Assert
        assert result is False
    
    def test_revert_commit_success(self, mock_subprocess, mock_git_env, commit_outputs):
        """Test successful revert."""
        # Arrange
        commit_ops = GitCommitOperations()
        mock_subprocess['check_output'].side_effect = [
            commit_outputs['git_version'],  # git --version
            commit_outputs['get_commit_hash'],  # git rev-parse --verify
            commit_outputs['revert_success']  # git rev-parse HEAD
        ]
        
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
        mock_subprocess['check_output'].side_effect = [
            commit_outputs['git_version'],  # git --version
            commit_outputs['get_commit_hash']  # git rev-parse --verify
        ]
        mock_subprocess['check_call'].side_effect = [
            0,  # git config successful
            subprocess.CalledProcessError(1, ['git', 'revert', '--no-edit', 'abc1234'])  # revert fails
        ]
        
        # Act
        result, revert_hash = commit_ops.revert_commit('abc1234')
        
        # Assert
        assert result is False
        assert revert_hash is None
    
    def test_format_timestamp(self, mock_subprocess, mock_git_env):
        """Test timestamp formatting."""
        # Arrange
        commit_ops = GitCommitOperations()
        timestamp = "1617286496"  # 2023-04-01 12:34:56
        
        # Act
        result = commit_ops._format_timestamp(timestamp)
        
        # Assert
        assert "2023" in result
        assert ":" in result  # Should contain time with colons


@pytest.mark.unit
@pytest.mark.git
@pytest.mark.commit
class TestMainFunction:
    """Unit tests for main function."""
    
    def test_create_action(self, mock_subprocess, mock_git_env, commit_outputs):
        """Test create action in main function."""
        # Arrange
        os.environ['INPUT_ACTION'] = 'create'
        os.environ['INPUT_MESSAGE'] = 'Test commit'
        
        mock_subprocess['check_output'].side_effect = [
            commit_outputs['git_version'],  # git --version
            "M  file1.txt\n",  # git status --porcelain
            commit_outputs['commit_create']  # git rev-parse HEAD
        ]
        
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
        
        mock_subprocess['check_output'].side_effect = [
            commit_outputs['git_version'],  # git --version
            commit_outputs['commit_amend']  # git rev-parse HEAD
        ]
        
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
        
        mock_subprocess['check_output'].side_effect = [
            commit_outputs['git_version'],  # git --version
            commit_outputs['list_commits']  # git log
        ]
        
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
        
        mock_subprocess['check_output'].side_effect = [
            commit_outputs['git_version'],  # git --version
            commit_outputs['get_commit_hash']  # git rev-parse --verify
        ]
        
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
        
        mock_subprocess['check_output'].side_effect = [
            commit_outputs['git_version'],  # git --version
            commit_outputs['get_commit_hash'],  # git rev-parse --verify
            commit_outputs['revert_success']  # git rev-parse HEAD
        ]
        
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