#!/usr/bin/env python3

import pytest
import os
import sys
import subprocess
import tempfile
import shutil
from pathlib import Path

# Add parent directory to path to import module under test
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the module under test
from main import GitCommitOperations


@pytest.fixture
def git_repo():
    """Create a temporary git repository for integration testing."""
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()
    
    # Save the current working directory
    original_dir = os.getcwd()
    
    # Change to the temporary directory
    os.chdir(temp_dir)
    
    # Initialize a git repository
    subprocess.run(['git', 'init'], check=True)
    subprocess.run(['git', 'config', 'user.name', 'Test User'], check=True)
    subprocess.run(['git', 'config', 'user.email', 'test@example.com'], check=True)
    
    # Create a test file and commit it
    with open('test.txt', 'w') as f:
        f.write('Initial content')
    
    subprocess.run(['git', 'add', 'test.txt'], check=True)
    subprocess.run(['git', 'commit', '-m', 'Initial commit'], check=True)
    
    yield temp_dir
    
    # Change back to the original directory
    os.chdir(original_dir)
    
    # Clean up the temporary directory
    shutil.rmtree(temp_dir)


@pytest.mark.integration
@pytest.mark.git
@pytest.mark.commit
class TestGitCommitOperationsIntegration:
    """Integration tests for GitCommitOperations class."""
    
    def test_create_commit(self, git_repo):
        """Test creating a commit in a real git repository."""
        # Arrange
        commit_ops = GitCommitOperations()
        
        # Create a new file
        with open('feature.txt', 'w') as f:
            f.write('New feature content')
        
        # Act
        result, commit_hash = commit_ops.create_commit("Add feature", ["feature.txt"])
        
        # Assert
        assert result is True
        assert commit_hash is not None
        
        # Verify the commit was created
        log_output = subprocess.check_output(['git', 'log', '-1', '--pretty=format:%s'], text=True)
        assert log_output == "Add feature"
        
        # Verify the file was committed
        status_output = subprocess.check_output(['git', 'status', '--porcelain'], text=True)
        assert 'feature.txt' not in status_output
    
    def test_amend_commit(self, git_repo):
        """Test amending a commit in a real git repository."""
        # Arrange
        commit_ops = GitCommitOperations()
        
        # Create a file and commit it
        with open('file1.txt', 'w') as f:
            f.write('Initial file')
        
        result, original_hash = commit_ops.create_commit("Initial file", ["file1.txt"])
        
        # Create another file
        with open('file2.txt', 'w') as f:
            f.write('Additional file')
        
        # Act - Amend the commit with a new file
        result, amended_hash = commit_ops.amend_commit("Updated commit message", ["file2.txt"])
        
        # Assert
        assert result is True
        assert amended_hash != original_hash
        
        # Verify the commit message was updated
        log_output = subprocess.check_output(['git', 'log', '-1', '--pretty=format:%s'], text=True)
        assert log_output == "Updated commit message"
        
        # Verify both files are in the same commit
        files_output = subprocess.check_output(['git', 'show', '--name-only', '--format='], text=True).strip().split('\n')
        assert 'file1.txt' in files_output
        assert 'file2.txt' in files_output
    
    def test_list_commits(self, git_repo):
        """Test listing commits in a real git repository."""
        # Arrange
        commit_ops = GitCommitOperations()
        
        # Create multiple commits
        for i in range(3):
            file_name = f'file{i}.txt'
            with open(file_name, 'w') as f:
                f.write(f'Content for {file_name}')
            
            commit_ops.create_commit(f"Add {file_name}", [file_name])
        
        # Act
        commits = commit_ops.list_commits(limit=3)
        
        # Assert
        assert len(commits) == 3
        assert "Add file2.txt" in commits[0]
        assert "Add file1.txt" in commits[1]
        assert "Add file0.txt" in commits[2]
    
    def test_get_commit_info(self, git_repo):
        """Test getting commit information in a real git repository."""
        # Arrange
        commit_ops = GitCommitOperations()
        
        # Create a commit with a known message
        with open('feature.txt', 'w') as f:
            f.write('Feature content')
        
        result, commit_hash = commit_ops.create_commit("Feature commit message", ["feature.txt"])
        
        # Act
        commit_info = commit_ops.get_commit_info(commit_hash)
        
        # Assert
        assert commit_info['hash'] == commit_hash
        assert commit_info['message'] == "Feature commit message"
        assert commit_info['author'] == "Test User"
        assert 'date' in commit_info
    
    def test_cherry_pick_commit(self, git_repo):
        """Test cherry-picking a commit in a real git repository."""
        # Arrange
        commit_ops = GitCommitOperations()
        
        # Create a feature branch with a commit
        subprocess.run(['git', 'checkout', '-b', 'feature'], check=True)
        
        with open('feature.txt', 'w') as f:
            f.write('Feature content')
        
        result, feature_commit = commit_ops.create_commit("Add feature", ["feature.txt"])
        
        # Go back to main branch
        subprocess.run(['git', 'checkout', 'master'], check=True)
        
        # Act - Cherry-pick the feature commit
        result = commit_ops.cherry_pick_commit(feature_commit)
        
        # Assert
        assert result is True
        
        # Verify the file is now in the main branch
        assert os.path.exists('feature.txt')
        
        # Verify the commit message is the same
        log_output = subprocess.check_output(['git', 'log', '-1', '--pretty=format:%s'], text=True)
        assert log_output == "Add feature"
    
    def test_revert_commit(self, git_repo):
        """Test reverting a commit in a real git repository."""
        # Arrange
        commit_ops = GitCommitOperations()
        
        # Create a file
        with open('to_revert.txt', 'w') as f:
            f.write('Content that will be reverted')
        
        result, commit_to_revert = commit_ops.create_commit("Add file to revert", ["to_revert.txt"])
        
        # Act
        result, revert_commit = commit_ops.revert_commit(commit_to_revert)
        
        # Assert
        assert result is True
        assert revert_commit is not None
        
        # Verify a revert commit was created
        log_output = subprocess.check_output(['git', 'log', '-1', '--pretty=format:%s'], text=True)
        assert "Revert" in log_output
        assert "Add file to revert" in log_output
        
        # The file should still exist but be removed in the commit
        assert os.path.exists('to_revert.txt')
        status_output = subprocess.check_output(['git', 'status', '--porcelain'], text=True)
        assert status_output.strip() == "", "Working directory should be clean after revert"