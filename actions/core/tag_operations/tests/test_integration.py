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
from main import GitTagOperations


@pytest.fixture
def git_repo():
    """Create a temporary git repository for testing."""
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()
    cwd = os.getcwd()
    
    try:
        # Change to the temporary directory
        os.chdir(temp_dir)
        
        # Initialize a git repository
        subprocess.check_call(['git', 'init'])
        
        # Configure git user
        subprocess.check_call(['git', 'config', 'user.email', 'test@example.com'])
        subprocess.check_call(['git', 'config', 'user.name', 'Test User'])
        
        # Create a file and commit it
        with open('test.txt', 'w') as f:
            f.write('Hello, world!')
        
        subprocess.check_call(['git', 'add', 'test.txt'])
        subprocess.check_call(['git', 'commit', '-m', 'Initial commit'])
        
        # Set GITHUB_OUTPUT environment variable
        github_output = os.path.join(temp_dir, 'github_output')
        with open(github_output, 'w') as f:
            f.write('')
        os.environ['GITHUB_OUTPUT'] = github_output
        
        yield temp_dir
        
    finally:
        # Change back to the original directory
        os.chdir(cwd)
        
        # Clean up the temporary directory
        shutil.rmtree(temp_dir)


@pytest.mark.integration
class TestGitTagOperationsIntegration:
    """Integration tests for GitTagOperations class using real git commands."""
    
    def test_create_and_delete_tag(self, git_repo):
        """Test creating and deleting a tag."""
        # Arrange
        tag_ops = GitTagOperations()
        
        # Act - Create
        create_result = tag_ops.create_tag('v1.0.0')
        
        # Check if tag exists
        exists_result = tag_ops.check_tag_exists('v1.0.0')
        
        # Act - Delete
        delete_result = tag_ops.delete_tag('v1.0.0')
        
        # Check if tag exists after deletion
        exists_after_delete = tag_ops.check_tag_exists('v1.0.0')
        
        # Assert
        assert create_result is True, "Failed to create tag"
        assert exists_result is True, "Tag should exist after creation"
        assert delete_result is True, "Failed to delete tag"
        assert exists_after_delete is False, "Tag should not exist after deletion"
    
    def test_create_annotated_tag(self, git_repo):
        """Test creating an annotated tag and retrieving its message."""
        # Arrange
        tag_ops = GitTagOperations()
        message = "Release v1.0.0"
        
        # Act
        create_result = tag_ops.create_tag('v1.0.0', message=message)
        
        # Get tag message
        tag_message = tag_ops.get_tag_message('v1.0.0')
        
        # Assert
        assert create_result is True, "Failed to create annotated tag"
        assert message in tag_message, "Tag message not found"
    
    def test_create_tag_at_reference(self, git_repo):
        """Test creating a tag at a specific reference."""
        # Arrange
        tag_ops = GitTagOperations()
        
        # Get current commit SHA
        commit_sha = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
        
        # Act
        create_result = tag_ops.create_tag('v1.0.0', ref=commit_sha)
        
        # Assert
        assert create_result is True, "Failed to create tag at reference"
        assert tag_ops.check_tag_exists('v1.0.0') is True, "Tag should exist"
    
    def test_list_tags_with_pattern(self, git_repo):
        """Test listing tags with pattern filtering."""
        # Arrange
        tag_ops = GitTagOperations()
        
        # Create multiple tags
        tag_ops.create_tag('v1.0.0')
        tag_ops.create_tag('v1.1.0')
        tag_ops.create_tag('v2.0.0')
        
        # Act
        v1_tags = tag_ops.list_tags(pattern='v1.*')
        all_tags = tag_ops.list_tags()
        
        # Assert
        assert len(v1_tags) == 2, "Should have 2 tags matching v1.*"
        assert 'v1.0.0' in v1_tags, "v1.0.0 should be in filtered tags"
        assert 'v1.1.0' in v1_tags, "v1.1.0 should be in filtered tags"
        assert 'v2.0.0' not in v1_tags, "v2.0.0 should not be in filtered tags"
        
        assert len(all_tags) == 3, "Should have 3 tags total"
    
    def test_tag_validation(self, git_repo):
        """Test tag name validation."""
        # Arrange
        tag_ops = GitTagOperations()
        
        # Act & Assert
        assert tag_ops.create_tag('valid-tag') is True, "Valid tag creation should succeed"
        assert tag_ops.create_tag('invalid tag') is False, "Invalid tag with space should fail"
        assert tag_ops.create_tag('invalid^tag') is False, "Invalid tag with ^ should fail"
    
    def test_force_tag_creation(self, git_repo):
        """Test force creating a tag that already exists."""
        # Arrange
        tag_ops = GitTagOperations()
        
        # Create a tag
        tag_ops.create_tag('v1.0.0', message="Original message")
        
        # Act - Try to create the same tag without force (should fail)
        result_without_force = tag_ops.create_tag('v1.0.0', message="New message")
        
        # Try to create the same tag with force
        result_with_force = tag_ops.create_tag('v1.0.0', message="New message", force=True)
        
        # Get the tag message
        tag_message = tag_ops.get_tag_message('v1.0.0')
        
        # Assert
        assert result_without_force is False, "Creating existing tag without force should fail"
        assert result_with_force is True, "Creating existing tag with force should succeed"
        assert "New message" in tag_message, "Tag message should have been updated"