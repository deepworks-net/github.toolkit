import os
import sys
import pytest
import subprocess
from pathlib import Path

# Add src directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from git_commit_operations import GitCommitOperations

class TestGitCommitOperationsIntegration:
    """Integration tests for GitCommitOperations class."""
    
    def test_create_and_list_commit(self, git_repo):
        commit_ops = GitCommitOperations()
        
        # Create a new file
        test_file = Path(git_repo) / "new_file.txt"
        test_file.write_text("New content")
        
        # Create commit
        result = commit_ops.create_commit(
            'Test commit message', 
            files=['new_file.txt']
        )
        assert result is True
        
        # List commits to verify creation
        commits = commit_ops.list_commits(max_count=1)
        assert len(commits) == 1
        assert 'Test commit message' in commits[0]
    
    def test_get_commit_info(self, git_repo):
        commit_ops = GitCommitOperations()
        
        # Create a commit with known message
        test_file = Path(git_repo) / "info_test.txt"
        test_file.write_text("Info test content")
        
        commit_ops.create_commit(
            'Get info test commit', 
            files=['info_test.txt']
        )
        
        # Get commit info
        info = commit_ops.get_commit_info('HEAD')
        
        assert info.get('message') == 'Get info test commit'
        assert info.get('author') == 'Test User'
        assert info.get('email') == 'test@example.com'
    
    def test_revert_commit(self, git_repo):
        commit_ops = GitCommitOperations()
        
        # Create a file and commit it
        test_file = Path(git_repo) / "revert_test.txt"
        test_file.write_text("Revert test content")
        
        commit_ops.create_commit(
            'Commit to revert', 
            files=['revert_test.txt']
        )
        
        # Get the commit hash
        commit_hash = commit_ops.get_commit_info('HEAD')['hash']
        
        # Create another file and commit it
        second_file = Path(git_repo) / "second_file.txt"
        second_file.write_text("Second file content")
        
        commit_ops.create_commit(
            'Second commit', 
            files=['second_file.txt']
        )
        
        # Revert the first commit
        result = commit_ops.revert_commit(commit_hash)
        assert result is True
        
        # Check that the file no longer exists or has been modified
        # (this depends on the specific behavior of the test - may need adjustment)
        commits = commit_ops.list_commits(max_count=1)
        assert 'Revert' in commits[0]