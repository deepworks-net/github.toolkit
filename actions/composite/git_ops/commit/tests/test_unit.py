import os
import sys
import pytest
import subprocess
from unittest.mock import patch, MagicMock

# Add src directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from git_commit_operations import GitCommitOperations

class TestGitCommitOperations:
    """Unit tests for GitCommitOperations class."""
    
    @patch('subprocess.check_call')
    def test_create_commit(self, mock_check_call):
        commit_ops = GitCommitOperations()
        result = commit_ops.create_commit('Test commit')
        
        assert result is True
        mock_check_call.assert_called_with(['git', 'commit', '-m', 'Test commit'])
    
    @patch('subprocess.check_call')
    def test_create_commit_with_files(self, mock_check_call):
        commit_ops = GitCommitOperations()
        result = commit_ops.create_commit('Test commit', files=['file1.txt', 'file2.txt'])
        
        assert result is True
        mock_check_call.assert_any_call(['git', 'add', 'file1.txt'])
        mock_check_call.assert_any_call(['git', 'add', 'file2.txt'])
        mock_check_call.assert_any_call(['git', 'commit', '-m', 'Test commit'])
    
    @patch('subprocess.check_call')
    def test_create_commit_all_changes(self, mock_check_call):
        commit_ops = GitCommitOperations()
        result = commit_ops.create_commit('Test commit', all_changes=True)
        
        assert result is True
        mock_check_call.assert_any_call(['git', 'add', '--all'])
        mock_check_call.assert_any_call(['git', 'commit', '-m', 'Test commit'])
    
    @patch('subprocess.check_call')
    def test_create_commit_amend(self, mock_check_call):
        commit_ops = GitCommitOperations()
        result = commit_ops.create_commit('Test commit', amend=True)
        
        assert result is True
        mock_check_call.assert_called_with(['git', 'commit', '--amend', '-m', 'Test commit'])
    
    @patch('subprocess.check_output')
    def test_get_commit_info(self, mock_check_output):
        mock_output = "abcdef1234567890\nTest User\ntest@example.com\n1600000000\nTest commit message"
        mock_check_output.return_value = mock_output
        
        commit_ops = GitCommitOperations()
        result = commit_ops.get_commit_info('abcdef')
        
        assert result == {
            'hash': 'abcdef1234567890',
            'author': 'Test User',
            'email': 'test@example.com',
            'date': '1600000000',
            'message': 'Test commit message'
        }
        mock_check_output.assert_called_with(
            ['git', 'show', '-s', '--format=%H%n%an%n%ae%n%at%n%s', 'abcdef'],
            text=True
        )
    
    @patch('subprocess.check_call')
    def test_revert_commit(self, mock_check_call):
        commit_ops = GitCommitOperations()
        result = commit_ops.revert_commit('abcdef')
        
        assert result is True
        mock_check_call.assert_called_with(['git', 'revert', 'abcdef', '--no-edit'])
    
    @patch('subprocess.check_call')
    def test_revert_commit_with_edit(self, mock_check_call):
        commit_ops = GitCommitOperations()
        result = commit_ops.revert_commit('abcdef', no_edit=False)
        
        assert result is True
        mock_check_call.assert_called_with(['git', 'revert', 'abcdef'])
    
    @patch('subprocess.check_output')
    def test_list_commits(self, mock_check_output):
        mock_output = "abcdef Test commit 1\n123456 Test commit 2\n789012 Test commit 3"
        mock_check_output.return_value = mock_output
        
        commit_ops = GitCommitOperations()
        result = commit_ops.list_commits(max_count=3)
        
        assert result == [
            'abcdef Test commit 1',
            '123456 Test commit 2',
            '789012 Test commit 3'
        ]
        mock_check_output.assert_called_with(
            ['git', 'log', '--format=%h %s', '-n3'],
            text=True
        )