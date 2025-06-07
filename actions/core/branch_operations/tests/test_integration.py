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


@pytest.mark.integration
class TestBranchOperationsIntegration:
    """Integration tests for branch operations."""
    
    def test_branch_lifecycle(self, mock_subprocess, mock_git_env, branch_outputs):
        """Test the complete lifecycle of a branch: create, list, checkout, merge, delete."""
        # Arrange
        branch_ops = GitBranchOperations()
        branch_name = "feature/test-lifecycle"
        
        # Configure mock outputs for different stages
        mock_subprocess['check_output'].side_effect = [
            'main',                           # Current branch check during create
            branch_outputs['list_local'],     # List branches
            branch_name,                      # Current branch after checkout
            'main',                           # Current branch after merge
            branch_name,                      # Current branch check during delete
            'main'                            # Current branch after delete
        ]
        
        # Act - Create branch
        create_result = branch_ops.create_branch(branch_name, 'main')
        
        # Act - List branches to verify creation
        list_result = branch_ops.list_branches()
        
        # Act - Checkout branch
        checkout_result = branch_ops.checkout_branch(branch_name)
        
        # Act - Merge branch
        merge_result = branch_ops.merge_branch(branch_name, 'main')
        
        # Act - Delete branch
        delete_result = branch_ops.delete_branch(branch_name)
        
        # Assert all operations were successful
        assert create_result is True
        assert 'main' in list_result
        assert 'develop' in list_result
        assert checkout_result is True
        assert merge_result is True
        assert delete_result is True
        
        # Verify sequence of operations
        expected_calls = [
            # Create branch
            call(['git', 'checkout', 'main']),
            call(['git', 'pull', 'origin', 'main']),
            call(['git', 'checkout', '-b', branch_name]),
            
            # List branches (check_output call)
            
            # Checkout branch
            call(['git', 'checkout', branch_name]),
            
            # Merge branch
            call(['git', 'merge', branch_name]),
            
            # Delete branch
            call(['git', 'checkout', 'main']),
            call(['git', 'branch', '-d', branch_name])
        ]
        
        # Check that calls were made in the correct order
        check_call_calls = mock_subprocess['check_call'].call_args_list
        for expected, actual in zip(expected_calls, check_call_calls):
            assert expected == actual
    
    def test_remote_operations(self, mock_subprocess, mock_git_env):
        """Test remote branch operations: create, push, delete remote."""
        # Arrange
        branch_ops = GitBranchOperations()
        branch_name = "feature/remote-test"
        
        # Configure mock outputs
        mock_subprocess['check_output'].return_value = 'main'  # Current branch
        
        # Act - Create and push branch
        create_result = branch_ops.create_branch(branch_name, 'main')
        push_result = branch_ops.push_branch(branch_name)
        
        # Act - Delete branch including remote
        delete_result = branch_ops.delete_branch(branch_name, remote=True)
        
        # Assert all operations were successful
        assert create_result is True
        assert push_result is True
        assert delete_result is True
        
        # Verify remote operations
        expected_remote_calls = [
            call(['git', 'push', 'origin', branch_name]),
            call(['git', 'push', 'origin', '--delete', branch_name])
        ]
        
        # Check that remote calls were made
        check_call_calls = mock_subprocess['check_call'].call_args_list
        for expected in expected_remote_calls:
            assert expected in check_call_calls
    
    def test_force_operations(self, mock_subprocess, mock_git_env):
        """Test force operations on branches."""
        # Arrange
        branch_ops = GitBranchOperations()
        branch_name = "feature/force-test"
        
        # Configure mock outputs
        mock_subprocess['check_output'].return_value = 'main'  # Current branch
        
        # Act - Force checkout
        checkout_result = branch_ops.checkout_branch(branch_name, force=True)
        
        # Act - Force delete 
        delete_result = branch_ops.delete_branch(branch_name, force=True)
        
        # Act - Force push
        push_result = branch_ops.push_branch(branch_name, force=True)
        
        # Assert all operations were successful
        assert checkout_result is True
        assert delete_result is True
        assert push_result is True
        
        # Verify force flags were used
        expected_force_calls = [
            call(['git', 'checkout', '-f', branch_name]),
            call(['git', 'branch', '-D', branch_name]),
            call(['git', 'push', 'origin', '--force', branch_name])
        ]
        
        # Check that force flags were included
        check_call_calls = mock_subprocess['check_call'].call_args_list
        for expected in expected_force_calls:
            assert expected in check_call_calls