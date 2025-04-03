import os
import sys
import pytest
import subprocess
from unittest.mock import patch, MagicMock

# Add src directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from git_branch_operations import GitBranchOperations

class TestGitBranchOperations:
    """Unit tests for GitBranchOperations class."""
    
    @patch('subprocess.check_call')
    def test_create_branch(self, mock_check_call):
        branch_ops = GitBranchOperations()
        result = branch_ops.create_branch('test-branch')
        
        assert result is True
        mock_check_call.assert_called_with(['git', 'branch', 'test-branch'])
    
    @patch('subprocess.check_call')
    def test_create_branch_with_start_point(self, mock_check_call):
        branch_ops = GitBranchOperations()
        result = branch_ops.create_branch('test-branch', 'main')
        
        assert result is True
        mock_check_call.assert_called_with(['git', 'branch', 'test-branch', 'main'])
    
    @patch('subprocess.check_call')
    def test_delete_branch(self, mock_check_call):
        branch_ops = GitBranchOperations()
        result = branch_ops.delete_branch('test-branch')
        
        assert result is True
        mock_check_call.assert_called_with(['git', 'branch', '-d', 'test-branch'])
    
    @patch('subprocess.check_call')
    def test_delete_branch_force(self, mock_check_call):
        branch_ops = GitBranchOperations()
        result = branch_ops.delete_branch('test-branch', force=True)
        
        assert result is True
        mock_check_call.assert_called_with(['git', 'branch', '-D', 'test-branch'])
    
    @patch('subprocess.check_call')
    def test_delete_branch_remote(self, mock_check_call):
        branch_ops = GitBranchOperations()
        result = branch_ops.delete_branch('test-branch', remote=True)
        
        assert result is True
        mock_check_call.assert_any_call(['git', 'branch', '-d', 'test-branch'])
        mock_check_call.assert_any_call(['git', 'push', 'origin', '--delete', 'test-branch'])
    
    @patch('subprocess.check_call')
    def test_checkout_branch(self, mock_check_call):
        branch_ops = GitBranchOperations()
        result = branch_ops.checkout_branch('test-branch')
        
        assert result is True
        mock_check_call.assert_called_with(['git', 'checkout', 'test-branch'])
    
    @patch('subprocess.check_call')
    def test_checkout_branch_create(self, mock_check_call):
        branch_ops = GitBranchOperations()
        result = branch_ops.checkout_branch('test-branch', create=True)
        
        assert result is True
        mock_check_call.assert_called_with(['git', 'checkout', '-b', 'test-branch'])
    
    @patch('subprocess.check_output')
    def test_list_branches(self, mock_check_output):
        mock_check_output.return_value = "* main\n  develop\n  feature/test\n"
        
        branch_ops = GitBranchOperations()
        result = branch_ops.list_branches()
        
        assert result == ['main', 'develop', 'feature/test']
        mock_check_output.assert_called_with(['git', 'branch'], text=True)
    
    @patch('subprocess.check_output')
    def test_list_branches_all(self, mock_check_output):
        mock_check_output.return_value = "* main\n  develop\n  remotes/origin/main\n"
        
        branch_ops = GitBranchOperations()
        result = branch_ops.list_branches(all_branches=True)
        
        assert result == ['main', 'develop', 'remotes/origin/main']
        mock_check_output.assert_called_with(['git', 'branch', '--all'], text=True)
    
    @patch('subprocess.check_output')
    def test_list_branches_remote(self, mock_check_output):
        mock_check_output.return_value = "  remotes/origin/main\n  remotes/origin/develop\n"
        
        branch_ops = GitBranchOperations()
        result = branch_ops.list_branches(remote=True)
        
        assert result == ['remotes/origin/main', 'remotes/origin/develop']
        mock_check_output.assert_called_with(['git', 'branch', '-r'], text=True)