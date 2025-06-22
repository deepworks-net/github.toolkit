#!/usr/bin/env python3

import pytest
import os
import sys
from pathlib import Path
from unittest.mock import patch

# Add parent directory to path to import module under test
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import FileOperations


@pytest.mark.unit
class TestFileOperations:
    """Unit tests for FileOperations class."""
    
    def test_create_file_success(self, temp_dir):
        """Test successful file creation."""
        # Arrange
        file_ops = FileOperations()
        file_path = os.path.join(temp_dir, 'test.txt')
        content = 'Test content'
        
        # Act
        result, message = file_ops.create_file(file_path, content)
        
        # Assert
        assert result is True
        assert 'created' in message.lower()
        assert Path(file_path).exists()
        assert Path(file_path).read_text() == content
    
    def test_create_file_with_dirs(self, temp_dir):
        """Test file creation with directory creation."""
        # Arrange
        file_ops = FileOperations()
        file_path = os.path.join(temp_dir, 'subdir', 'nested', 'test.txt')
        content = 'Nested content'
        
        # Act
        result, message = file_ops.create_file(file_path, content, create_dirs=True)
        
        # Assert
        assert result is True
        assert Path(file_path).exists()
        assert Path(file_path).read_text() == content
    
    def test_create_file_no_overwrite(self, sample_files):
        """Test file creation when file exists and overwrite is False."""
        # Arrange
        file_ops = FileOperations()
        existing_file = sample_files['text_file']
        
        # Act
        result, message = file_ops.create_file(existing_file, 'New content', overwrite=False)
        
        # Assert
        assert result is False
        assert 'already exists' in message.lower()
    
    def test_read_file_success(self, sample_files):
        """Test successful file reading."""
        # Arrange
        file_ops = FileOperations()
        file_path = sample_files['text_file']
        
        # Act
        result, content = file_ops.read_file(file_path)
        
        # Assert
        assert result is True
        assert content == 'Hello, World!'
    
    def test_read_nonexistent_file(self, temp_dir):
        """Test reading a file that doesn't exist."""
        # Arrange
        file_ops = FileOperations()
        file_path = os.path.join(temp_dir, 'nonexistent.txt')
        
        # Act
        result, message = file_ops.read_file(file_path)
        
        # Assert
        assert result is False
        assert 'not found' in message.lower()
    
    def test_update_file_success(self, sample_files):
        """Test successful file update."""
        # Arrange
        file_ops = FileOperations()
        file_path = sample_files['text_file']
        new_content = 'Updated content'
        
        # Act
        result, message = file_ops.update_file(file_path, new_content)
        
        # Assert
        assert result is True
        assert 'updated' in message.lower()
        assert Path(file_path).read_text() == new_content
    
    def test_delete_file_success(self, sample_files):
        """Test successful file deletion."""
        # Arrange
        file_ops = FileOperations()
        file_path = sample_files['text_file']
        
        # Act
        result, message = file_ops.delete_file(file_path)
        
        # Assert
        assert result is True
        assert 'deleted' in message.lower()
        assert not Path(file_path).exists()
    
    def test_copy_file_success(self, sample_files, temp_dir):
        """Test successful file copy."""
        # Arrange
        file_ops = FileOperations()
        source = sample_files['text_file']
        destination = os.path.join(temp_dir, 'copied.txt')
        
        # Act
        result, message = file_ops.copy_file(source, destination)
        
        # Assert
        assert result is True
        assert 'copied' in message.lower()
        assert Path(destination).exists()
        assert Path(source).read_text() == Path(destination).read_text()
    
    def test_move_file_success(self, sample_files, temp_dir):
        """Test successful file move."""
        # Arrange
        file_ops = FileOperations()
        source = sample_files['text_file']
        destination = os.path.join(temp_dir, 'moved.txt')
        original_content = Path(source).read_text()
        
        # Act
        result, message = file_ops.move_file(source, destination)
        
        # Assert
        assert result is True
        assert 'moved' in message.lower()
        assert Path(destination).exists()
        assert not Path(source).exists()
        assert Path(destination).read_text() == original_content
    
    def test_search_files_success(self, sample_files):
        """Test successful file search."""
        # Arrange
        file_ops = FileOperations()
        pattern = '*.txt'
        
        # Change to temp directory for relative search
        original_cwd = os.getcwd()
        temp_dir = Path(sample_files['text_file']).parent
        os.chdir(temp_dir)
        
        try:
            # Act
            result, files = file_ops.search_files(pattern)
            
            # Assert
            assert result is True
            assert isinstance(files, list)
            assert len(files) > 0
            # Check that at least one of our sample files is found
            file_names = [Path(f).name for f in files]
            assert 'sample.txt' in file_names
        finally:
            os.chdir(original_cwd)
    
    def test_get_file_info_success(self, sample_files):
        """Test successful file info retrieval."""
        # Arrange
        file_ops = FileOperations()
        file_path = sample_files['text_file']
        
        # Act
        result, info = file_ops.get_file_info(file_path)
        
        # Assert
        assert result is True
        assert isinstance(info, dict)
        assert info['exists'] is True
        assert info['is_file'] is True
        assert info['size'] > 0
    
    def test_base64_encoding(self, temp_dir):
        """Test base64 encoding operations."""
        # Arrange
        file_ops = FileOperations()
        file_path = os.path.join(temp_dir, 'base64_test.txt')
        original_content = 'Hello, World!'
        # Encode to base64
        import base64
        encoded_content = base64.b64encode(original_content.encode()).decode()
        
        # Act - Create with base64
        result, message = file_ops.create_file(file_path, encoded_content, encoding='base64')
        
        # Assert creation
        assert result is True
        
        # Act - Read with base64
        result, read_content = file_ops.read_file(file_path, encoding='base64')
        
        # Assert reading
        assert result is True
        assert read_content == encoded_content


@pytest.mark.unit
class TestMainFunction:
    """Unit tests for main function."""
    
    def test_create_action_success(self, mock_github_env, temp_dir):
        """Test create action in main function."""
        # Arrange
        file_path = os.path.join(temp_dir, 'test_main.txt')
        os.environ['INPUT_ACTION'] = 'create'
        os.environ['INPUT_FILE_PATH'] = file_path
        os.environ['INPUT_CONTENT'] = 'Test content from main'
        
        # Import main here to ensure env vars are set
        from main import main
        
        # Act
        main()  # Should not raise an exception
        
        # Assert
        assert Path(file_path).exists()
        with open(mock_github_env['GITHUB_OUTPUT'], 'r') as f:
            output = f.read()
        
        assert 'operation_status=success' in output
        assert f'file_created={file_path}' in output
    
    def test_read_action_success(self, mock_github_env, sample_files):
        """Test read action in main function."""
        # Arrange
        file_path = sample_files['text_file']
        os.environ['INPUT_ACTION'] = 'read'
        os.environ['INPUT_FILE_PATH'] = file_path
        
        # Import main here to ensure env vars are set
        from main import main
        
        # Act
        main()  # Should not raise an exception
        
        # Assert
        with open(mock_github_env['GITHUB_OUTPUT'], 'r') as f:
            output = f.read()
        
        assert 'operation_status=success' in output
        assert 'file_content=Hello, World!' in output
    
    def test_invalid_action(self, mock_github_env):
        """Test invalid action in main function."""
        # Arrange
        os.environ['INPUT_ACTION'] = 'invalid_action'
        
        # Import main here to ensure env vars are set
        from main import main
        
        # Act & Assert
        with pytest.raises(SystemExit) as exc_info:
            main()
        
        assert exc_info.value.code == 1