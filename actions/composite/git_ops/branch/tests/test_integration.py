import os
import sys
import pytest
import subprocess
from pathlib import Path

# Add src directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from git_branch_operations import GitBranchOperations

class TestGitBranchOperationsIntegration:
    """Integration tests for GitBranchOperations class."""
    
    def test_create_and_list_branch(self, git_repo):
        branch_ops = GitBranchOperations()
        
        # Create a new branch
        result = branch_ops.create_branch('test-branch')
        assert result is True
        
        # List branches to verify creation
        branches = branch_ops.list_branches()
        assert 'test-branch' in branches
    
    def test_checkout_branch(self, git_repo):
        branch_ops = GitBranchOperations()
        
        # Create and checkout branch
        result = branch_ops.checkout_branch('feature-branch', create=True)
        assert result is True
        
        # Verify current branch
        output = subprocess.check_output(['git', 'branch', '--show-current'], text=True).strip()
        assert output == 'feature-branch'
    
    def test_delete_branch(self, git_repo):
        branch_ops = GitBranchOperations()
        
        # Create a branch
        branch_ops.create_branch('delete-me')
        
        # Verify branch exists
        branches_before = branch_ops.list_branches()
        assert 'delete-me' in branches_before
        
        # Delete the branch
        result = branch_ops.delete_branch('delete-me')
        assert result is True
        
        # Verify branch is deleted
        branches_after = branch_ops.list_branches()
        assert 'delete-me' not in branches_after