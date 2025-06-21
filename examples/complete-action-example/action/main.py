#!/usr/bin/env python3
"""
File Operations Action - LCMCP Implementation Example

This action demonstrates the Loosely Coupled Modular Composition Pattern
with complete encapsulation and explicit interfaces.
"""

import os
import sys
import glob
import shutil
import base64
from pathlib import Path
from typing import Optional, List, Union, Tuple


class FileOperations:
    """Handles atomic file system operations following LCMCP principles."""
    
    def __init__(self):
        # No external dependencies or state
        pass
    
    def create_file(self, file_path: str, content: str = "", 
                   encoding: str = "utf-8", create_dirs: bool = True,
                   overwrite: bool = False) -> Tuple[bool, str]:
        """
        Create a new file with specified content.
        
        Args:
            file_path: Path where file should be created
            content: Content to write to file
            encoding: File encoding
            create_dirs: Create parent directories if needed
            overwrite: Overwrite if file exists
            
        Returns:
            Tuple of (success, message)
        """
        try:
            path = Path(file_path)
            
            # Check if file exists and overwrite is False
            if path.exists() and not overwrite:
                return False, f"File already exists: {file_path}"
            
            # Create parent directories if requested
            if create_dirs:
                path.parent.mkdir(parents=True, exist_ok=True)
            
            # Handle different encodings
            if encoding == "base64":
                content_bytes = base64.b64decode(content)
                path.write_bytes(content_bytes)
            else:
                path.write_text(content, encoding=encoding)
            
            return True, f"File created: {file_path}"
            
        except Exception as e:
            return False, f"Error creating file: {str(e)}"
    
    def read_file(self, file_path: str, encoding: str = "utf-8") -> Tuple[bool, str]:
        """
        Read content from a file.
        
        Args:
            file_path: Path to file to read
            encoding: File encoding
            
        Returns:
            Tuple of (success, content or error message)
        """
        try:
            path = Path(file_path)
            
            if not path.exists():
                return False, f"File not found: {file_path}"
            
            if not path.is_file():
                return False, f"Not a file: {file_path}"
            
            # Handle different encodings
            if encoding == "base64":
                content = base64.b64encode(path.read_bytes()).decode('ascii')
            else:
                content = path.read_text(encoding=encoding)
            
            return True, content
            
        except Exception as e:
            return False, f"Error reading file: {str(e)}"
    
    def update_file(self, file_path: str, content: str,
                   encoding: str = "utf-8") -> Tuple[bool, str]:
        """
        Update an existing file's content.
        
        Args:
            file_path: Path to file to update
            content: New content
            encoding: File encoding
            
        Returns:
            Tuple of (success, message)
        """
        try:
            path = Path(file_path)
            
            if not path.exists():
                return False, f"File not found: {file_path}"
            
            # Handle different encodings
            if encoding == "base64":
                content_bytes = base64.b64decode(content)
                path.write_bytes(content_bytes)
            else:
                path.write_text(content, encoding=encoding)
            
            return True, f"File updated: {file_path}"
            
        except Exception as e:
            return False, f"Error updating file: {str(e)}"
    
    def delete_file(self, file_path: str) -> Tuple[bool, str]:
        """
        Delete a file.
        
        Args:
            file_path: Path to file to delete
            
        Returns:
            Tuple of (success, message)
        """
        try:
            path = Path(file_path)
            
            if not path.exists():
                return False, f"File not found: {file_path}"
            
            if path.is_dir():
                return False, f"Cannot delete directory with file operation: {file_path}"
            
            path.unlink()
            return True, f"File deleted: {file_path}"
            
        except Exception as e:
            return False, f"Error deleting file: {str(e)}"
    
    def copy_file(self, file_path: str, destination: str,
                 create_dirs: bool = True, overwrite: bool = False) -> Tuple[bool, str]:
        """
        Copy a file to a new location.
        
        Args:
            file_path: Source file path
            destination: Destination path
            create_dirs: Create parent directories if needed
            overwrite: Overwrite if destination exists
            
        Returns:
            Tuple of (success, message)
        """
        try:
            src = Path(file_path)
            dst = Path(destination)
            
            if not src.exists():
                return False, f"Source file not found: {file_path}"
            
            if dst.exists() and not overwrite:
                return False, f"Destination already exists: {destination}"
            
            # Create parent directories if requested
            if create_dirs:
                dst.parent.mkdir(parents=True, exist_ok=True)
            
            shutil.copy2(src, dst)
            return True, f"File copied: {file_path} -> {destination}"
            
        except Exception as e:
            return False, f"Error copying file: {str(e)}"
    
    def move_file(self, file_path: str, destination: str,
                 create_dirs: bool = True, overwrite: bool = False) -> Tuple[bool, str]:
        """
        Move a file to a new location.
        
        Args:
            file_path: Source file path
            destination: Destination path
            create_dirs: Create parent directories if needed
            overwrite: Overwrite if destination exists
            
        Returns:
            Tuple of (success, message)
        """
        try:
            src = Path(file_path)
            dst = Path(destination)
            
            if not src.exists():
                return False, f"Source file not found: {file_path}"
            
            if dst.exists() and not overwrite:
                return False, f"Destination already exists: {destination}"
            
            # Create parent directories if requested
            if create_dirs:
                dst.parent.mkdir(parents=True, exist_ok=True)
            
            shutil.move(str(src), str(dst))
            return True, f"File moved: {file_path} -> {destination}"
            
        except Exception as e:
            return False, f"Error moving file: {str(e)}"
    
    def search_files(self, pattern: str) -> Tuple[bool, List[str]]:
        """
        Search for files matching a glob pattern.
        
        Args:
            pattern: Glob pattern to search for
            
        Returns:
            Tuple of (success, list of matching files or error message)
        """
        try:
            # Use Path.glob for recursive patterns
            if '**' in pattern:
                base_path = Path('.')
                matches = list(base_path.glob(pattern))
                files = [str(f) for f in matches if f.is_file()]
            else:
                # Use glob.glob for simple patterns
                matches = glob.glob(pattern)
                files = [f for f in matches if os.path.isfile(f)]
            
            return True, files
            
        except Exception as e:
            return False, [f"Error searching files: {str(e)}"]
    
    def get_file_info(self, file_path: str) -> Tuple[bool, dict]:
        """
        Get information about a file.
        
        Args:
            file_path: Path to file
            
        Returns:
            Tuple of (success, info dict or error message)
        """
        try:
            path = Path(file_path)
            
            if not path.exists():
                return False, {"error": f"File not found: {file_path}"}
            
            info = {
                "exists": True,
                "size": path.stat().st_size,
                "is_file": path.is_file(),
                "is_dir": path.is_dir(),
                "absolute_path": str(path.absolute())
            }
            
            return True, info
            
        except Exception as e:
            return False, {"error": f"Error getting file info: {str(e)}"}


def main():
    """Main entry point for the action."""
    file_ops = FileOperations()
    
    # Get inputs from environment variables
    action = os.environ.get('INPUT_ACTION')
    file_path = os.environ.get('INPUT_FILE_PATH')
    content = os.environ.get('INPUT_CONTENT', '')
    destination = os.environ.get('INPUT_DESTINATION')
    pattern = os.environ.get('INPUT_PATTERN')
    encoding = os.environ.get('INPUT_ENCODING', 'utf-8')
    create_dirs = os.environ.get('INPUT_CREATE_DIRS', 'true').lower() == 'true'
    overwrite = os.environ.get('INPUT_OVERWRITE', 'false').lower() == 'true'
    
    # Initialize output variables
    result = False
    message = ""
    outputs = {}
    
    # Execute requested operation
    if action == 'create':
        if not file_path:
            print("Error: file_path is required for create action")
            sys.exit(1)
        result, message = file_ops.create_file(file_path, content, encoding, create_dirs, overwrite)
        if result:
            outputs['file_created'] = file_path
            _, info = file_ops.get_file_info(file_path)
            if isinstance(info, dict) and 'size' in info:
                outputs['file_size'] = str(info['size'])
    
    elif action == 'read':
        if not file_path:
            print("Error: file_path is required for read action")
            sys.exit(1)
        result, content_or_error = file_ops.read_file(file_path, encoding)
        if result:
            outputs['file_content'] = content_or_error
            message = f"File read successfully: {file_path}"
        else:
            message = content_or_error
    
    elif action == 'update':
        if not file_path:
            print("Error: file_path is required for update action")
            sys.exit(1)
        result, message = file_ops.update_file(file_path, content, encoding)
        if result:
            _, info = file_ops.get_file_info(file_path)
            if isinstance(info, dict) and 'size' in info:
                outputs['file_size'] = str(info['size'])
    
    elif action == 'delete':
        if not file_path:
            print("Error: file_path is required for delete action")
            sys.exit(1)
        result, message = file_ops.delete_file(file_path)
        if result:
            outputs['file_deleted'] = file_path
    
    elif action == 'copy':
        if not file_path or not destination:
            print("Error: file_path and destination are required for copy action")
            sys.exit(1)
        result, message = file_ops.copy_file(file_path, destination, create_dirs, overwrite)
    
    elif action == 'move':
        if not file_path or not destination:
            print("Error: file_path and destination are required for move action")
            sys.exit(1)
        result, message = file_ops.move_file(file_path, destination, create_dirs, overwrite)
    
    elif action == 'search':
        if not pattern:
            print("Error: pattern is required for search action")
            sys.exit(1)
        result, files_or_error = file_ops.search_files(pattern)
        if result:
            outputs['files_found'] = ','.join(files_or_error)
            message = f"Found {len(files_or_error)} files"
        else:
            message = files_or_error[0] if files_or_error else "Search failed"
    
    else:
        print(f"Invalid action: {action}")
        sys.exit(1)
    
    # Always check file existence for file_path operations
    if file_path and action != 'search':
        _, info = file_ops.get_file_info(file_path)
        if isinstance(info, dict):
            outputs['file_exists'] = str(info.get('exists', False)).lower()
    
    # Set outputs
    outputs['operation_status'] = 'success' if result else 'failure'
    
    # Write outputs to GITHUB_OUTPUT
    github_output = os.environ.get('GITHUB_OUTPUT')
    if github_output:
        with open(github_output, 'a') as f:
            for key, value in outputs.items():
                # Escape newlines in output values
                escaped_value = value.replace('\n', '%0A').replace('\r', '%0D')
                f.write(f"{key}={escaped_value}\n")
    
    # Print message for logging
    print(message)
    
    # Exit with appropriate code
    if not result:
        sys.exit(1)


if __name__ == "__main__":
    main()