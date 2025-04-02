#!/usr/bin/env python3

import pytest
import os
import sys
import subprocess
from unittest.mock import call

# Add parent directory to path to import module under test
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the module under test
from main import GitBranchOperations


@pytest.mark.unit
class TestGitBranchOperations:
    """Unit tests for GitBranchOperations class."""
    
    def test_create_branch_success(self, mock_subprocess, mock_git_env):
        """Test successful branch creation."""
        # Arrange
        branch_ops = GitBranchOperations()
        
        # Act
        result = branch_ops.create_branch('feature/test-branch', 'main')
        
        # Assert
        assert result is True
        assert mock_subprocess['check_call'].call_count == 3
        expected_calls = [
            call(['git', 'config', '--global', '--add', 'safe.directory', '/github/workspace']),
            call(['git', 'checkout', 'main']),
            call(['git', 'pull', 'origin', 'main']),
            call(['git', 'checkout', '-b', 'feature/test-branch'])
        ]
        mock_subprocess['check_call'].assert_has_calls(expected_calls)
    
    def test_delete_branch_success(self, mock_subprocess, mock_git_env, branch_outputs):
        """Test successful branch deletion."""
        # Arrange
        branch_ops = GitBranchOperations()
        mock_subprocess['check_output'].return_value = 'main'  # Current branch
        
        # Act
        result = branch_ops.delete_branch('feature/test-branch')
        
        # Assert
        assert result is True
        expected_calls = [
            call(['git', 'branch', '--show-current'], text=True),
            call(['git', 'branch', '-d', 'feature/test-branch'])
        ]
        mock_subprocess['check_output'].assert_has_calls(expected_calls[0:1])
        mock_subprocess['check_call'].assert_has_calls(expected_calls[1:2])
    
    def test_delete_current_branch(self, mock_subprocess, mock_git_env):
        """Test deleting the current branch."""
        # Arrange
        branch_ops = GitBranchOperations()
        mock_subprocess['check_output'].return_value = 'feature/test-branch'  # Current branch
        
        # Act
        result = branch_ops.delete_branch('feature/test-branch')
        
        # Assert
        assert result is True
        expected_calls = [
            call(['git', 'branch', '--show-current'], text=True),
            call(['git', 'checkout', 'main']),
            call(['git', 'branch', '-d', 'feature/test-branch'])
        ]
        mock_subprocess['check_output'].assert_has_calls(expected_calls[0:1])
        mock_subprocess['check_call'].assert_has_calls(expected_calls[1:3])
    
    def test_delete_remote_branch(self, mock_subprocess, mock_git_env):
        """Test deleting a branch locally and remotely."""
        # Arrange
        branch_ops = GitBranchOperations()
        mock_subprocess['check_output'].return_value = 'main'  # Current branch
        
        # Act
        result = branch_ops.delete_branch('feature/test-branch', remote=True)
        
        # Assert
        assert result is True
        expected_calls = [
            call(['git', 'branch', '-d', 'feature/test-branch']),
            call(['git', 'push', 'origin', '--delete', 'feature/test-branch'])
        ]
        mock_subprocess['check_call'].assert_has_calls(expected_calls[0:2])
    
    def test_list_branches(self, mock_subprocess, mock_git_env, branch_outputs):
        """Test listing branches."""
        # Arrange
        branch_ops = GitBranchOperations()
        mock_subprocess['check_output'].return_value = branch_outputs['list_local']
        
        # Act
        result = branch_ops.list_branches()
        
        # Assert
        assert len(result) == 3
        assert 'main' in result
        assert 'develop' in result
        assert 'feature/test-branch' in result
        mock_subprocess['check_output'].assert_called_once_with(['git', 'branch'], text=True)
    
    def test_list_branches_with_pattern(self, mock_subprocess, mock_git_env, branch_outputs):
        """Test listing branches with a pattern filter."""
        # Arrange
        branch_ops = GitBranchOperations()
        mock_subprocess['check_output'].return_value = branch_outputs['list_pattern']
        
        # Act
        result = branch_ops.list_branches(pattern='feature/*')
        
        # Assert
        assert len(result) == 2
        assert 'feature/test-branch' in result
        assert 'feature/another-branch' in result
        mock_subprocess['check_output'].assert_called_once_with(['git', 'branch', '--list', 'feature/*'], text=True)
    
    def test_checkout_branch(self, mock_subprocess, mock_git_env):
        """Test checking out a branch."""
        # Arrange
        branch_ops = GitBranchOperations()
        
        # Act
        result = branch_ops.checkout_branch('feature/test-branch')
        
        # Assert
        assert result is True
        mock_subprocess['check_call'].assert_called_with(['git', 'checkout', 'feature/test-branch'])
    
    def test_merge_branch(self, mock_subprocess, mock_git_env):
        """Test merging a branch."""
        # Arrange
        branch_ops = GitBranchOperations()
        
        # Act
        result = branch_ops.merge_branch('feature/test-branch')
        
        # Assert
        assert result is True
        mock_subprocess['check_call'].assert_called_with(['git', 'merge', 'feature/test-branch'])


@pytest.mark.unit
class TestMainFunction:
    """Unit tests for main function."""
    
    def test_create_action(self, mock_subprocess, mock_git_env):
        """Test create action in main function."""
        # Arrange
        os.environ['INPUT_ACTION'] = 'create'
        os.environ['INPUT_BRANCH_NAME'] = 'feature/test-branch'
        os.environ['INPUT_BASE_BRANCH'] = 'develop'
        
        mock_subprocess['check_output'].return_value = 'feature/test-branch'
        
        # Import main here to ensure env vars are set
        from main import main
        
        # Act
        main()  # Should not raise an exception
        
        # Assert
        with open(mock_git_env['GITHUB_OUTPUT'], 'r') as f:
            output = f.read()
        
        assert 'result=success' in output
        assert 'current_branch=feature/test-branch' in output
    
    def test_list_action(self, mock_subprocess, mock_git_env, branch_outputs):
        """Test list action in main function."""
        # Arrange
        os.environ['INPUT_ACTION'] = 'list'
        os.environ['INPUT_PATTERN'] = 'feature/*'
        
        branch_list = ['feature/test-branch', 'feature/another-branch']
        mock_subprocess['check_output'].side_effect = [
            'main',  # Current branch
            branch_outputs['list_pattern']  # Branch list
        ]
        
        # Import main here to ensure env vars are set
        from main import main
        
        # Act
        main()  # Should not raise an exception
        
        # Assert
        with open(mock_git_env['GITHUB_OUTPUT'], 'r') as f:
            output = f.read()
        
        assert 'result=success' in output
        assert 'branches=feature/test-branch,feature/another-branch' in output
        assert 'current_branch=main' in output