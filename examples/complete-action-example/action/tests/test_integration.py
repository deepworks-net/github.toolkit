#!/usr/bin/env python3

import pytest
import os
import sys
from pathlib import Path

# Add parent directory to path to import module under test
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import FileOperations


@pytest.mark.integration
class TestFileOperationsIntegration:
    """Integration tests for file operations workflows."""
    
    def test_complete_file_lifecycle(self, temp_dir, mock_github_env):
        """Test the complete lifecycle: create, read, update, copy, move, delete."""
        # Arrange
        file_ops = FileOperations()
        original_file = os.path.join(temp_dir, 'lifecycle_test.txt')
        copied_file = os.path.join(temp_dir, 'copied_lifecycle.txt')
        moved_file = os.path.join(temp_dir, 'moved_lifecycle.txt')
        content_v1 = 'Initial content'
        content_v2 = 'Updated content'
        
        # Act & Assert - Create
        result, message = file_ops.create_file(original_file, content_v1)
        assert result is True
        assert Path(original_file).exists()
        
        # Act & Assert - Read
        result, content = file_ops.read_file(original_file)
        assert result is True
        assert content == content_v1
        
        # Act & Assert - Update
        result, message = file_ops.update_file(original_file, content_v2)
        assert result is True
        result, content = file_ops.read_file(original_file)
        assert content == content_v2
        
        # Act & Assert - Copy
        result, message = file_ops.copy_file(original_file, copied_file)
        assert result is True
        assert Path(copied_file).exists()
        assert Path(original_file).exists()  # Original should still exist
        
        # Act & Assert - Move copied file
        result, message = file_ops.move_file(copied_file, moved_file)
        assert result is True
        assert Path(moved_file).exists()
        assert not Path(copied_file).exists()  # Source should be gone
        
        # Act & Assert - Delete
        result, message = file_ops.delete_file(original_file)
        assert result is True
        assert not Path(original_file).exists()
        
        result, message = file_ops.delete_file(moved_file)
        assert result is True
        assert not Path(moved_file).exists()
    
    def test_directory_operations_workflow(self, temp_dir, mock_github_env):
        """Test workflow involving directory creation and nested files."""
        # Arrange
        file_ops = FileOperations()
        nested_path = os.path.join(temp_dir, 'level1', 'level2', 'level3', 'deep_file.txt')
        content = 'Deep nested content'
        
        # Act & Assert - Create with directory creation
        result, message = file_ops.create_file(nested_path, content, create_dirs=True)
        assert result is True
        assert Path(nested_path).exists()
        assert Path(nested_path).read_text() == content
        
        # Act & Assert - Search for created file
        original_cwd = os.getcwd()
        os.chdir(temp_dir)
        
        try:
            result, files = file_ops.search_files('**/*.txt')
            assert result is True
            # Should find our deep nested file
            found_files = [Path(f).name for f in files]
            assert 'deep_file.txt' in found_files
        finally:
            os.chdir(original_cwd)
    
    def test_error_handling_workflow(self, temp_dir, mock_github_env):
        """Test error handling across different operations."""
        # Arrange
        file_ops = FileOperations()
        nonexistent_file = os.path.join(temp_dir, 'does_not_exist.txt')
        readonly_dir = os.path.join(temp_dir, 'readonly')
        
        # Create readonly directory
        Path(readonly_dir).mkdir()
        
        # Act & Assert - Try to read nonexistent file
        result, message = file_ops.read_file(nonexistent_file)
        assert result is False
        assert 'not found' in message.lower()
        
        # Act & Assert - Try to update nonexistent file
        result, message = file_ops.update_file(nonexistent_file, 'content')
        assert result is False
        assert 'not found' in message.lower()
        
        # Act & Assert - Try to delete nonexistent file
        result, message = file_ops.delete_file(nonexistent_file)
        assert result is False
        assert 'not found' in message.lower()
        
        # Act & Assert - Try to copy nonexistent file
        result, message = file_ops.copy_file(nonexistent_file, os.path.join(temp_dir, 'copy.txt'))
        assert result is False
        assert 'not found' in message.lower()
    
    def test_encoding_workflow(self, temp_dir, mock_github_env):
        """Test different encoding operations in sequence."""
        # Arrange
        file_ops = FileOperations()
        utf8_file = os.path.join(temp_dir, 'utf8.txt')
        ascii_file = os.path.join(temp_dir, 'ascii.txt')
        base64_file = os.path.join(temp_dir, 'base64.txt')
        
        utf8_content = 'UTF-8 content with émojis 🎉'
        ascii_content = 'Simple ASCII content'
        
        import base64
        base64_content = base64.b64encode(b'Binary-like content').decode()
        
        # Act & Assert - UTF-8
        result, message = file_ops.create_file(utf8_file, utf8_content, encoding='utf-8')
        assert result is True
        
        result, read_content = file_ops.read_file(utf8_file, encoding='utf-8')
        assert result is True
        assert read_content == utf8_content
        
        # Act & Assert - ASCII
        result, message = file_ops.create_file(ascii_file, ascii_content, encoding='ascii')
        assert result is True
        
        result, read_content = file_ops.read_file(ascii_file, encoding='ascii')
        assert result is True
        assert read_content == ascii_content
        
        # Act & Assert - Base64
        result, message = file_ops.create_file(base64_file, base64_content, encoding='base64')
        assert result is True
        
        result, read_content = file_ops.read_file(base64_file, encoding='base64')
        assert result is True
        assert read_content == base64_content
    
    def test_main_function_integration(self, temp_dir, mock_github_env):
        """Test main function with different action sequences."""
        from main import main
        
        # Test 1: Create -> Read sequence
        file_path = os.path.join(temp_dir, 'integration_test.txt')
        content = 'Integration test content'
        
        # Create file
        os.environ.update({
            'INPUT_ACTION': 'create',
            'INPUT_FILE_PATH': file_path,
            'INPUT_CONTENT': content
        })
        
        main()
        assert Path(file_path).exists()
        
        # Read file
        os.environ.update({
            'INPUT_ACTION': 'read',
            'INPUT_FILE_PATH': file_path,
            'INPUT_CONTENT': ''  # Clear content for read
        })
        
        main()
        
        # Check outputs
        with open(mock_github_env['GITHUB_OUTPUT'], 'r') as f:
            output = f.read()
        
        assert 'operation_status=success' in output
        assert f'file_content={content}' in output
    
    def test_overwrite_protection_workflow(self, temp_dir, mock_github_env):
        """Test overwrite protection across create operations."""
        # Arrange
        file_ops = FileOperations()
        file_path = os.path.join(temp_dir, 'protected.txt')
        original_content = 'Original content'
        new_content = 'New content'
        
        # Act & Assert - Create original file
        result, message = file_ops.create_file(file_path, original_content)
        assert result is True
        
        # Act & Assert - Try to create again without overwrite
        result, message = file_ops.create_file(file_path, new_content, overwrite=False)
        assert result is False
        assert 'already exists' in message.lower()
        
        # Verify original content is preserved
        result, content = file_ops.read_file(file_path)
        assert content == original_content
        
        # Act & Assert - Create with overwrite
        result, message = file_ops.create_file(file_path, new_content, overwrite=True)
        assert result is True
        
        # Verify new content
        result, content = file_ops.read_file(file_path)
        assert content == new_content