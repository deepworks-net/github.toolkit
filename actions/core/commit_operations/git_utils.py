#!/usr/bin/env python3

# Import the original classes to maintain backward compatibility
import os
import subprocess
import re
from typing import Optional, List, Dict, Union, Tuple, Pattern

class GitConfig:
    def __init__(self, workspace_path=None):
        """Initialize GitConfig with workspace path."""
        self.workspace_path = workspace_path or os.environ.get('GITHUB_WORKSPACE', '/github/workspace')
    
    def setup_identity(self):
        """Set up a default Git identity for actions if not already configured."""
        try:
            # Try to get current user.name
            try:
                subprocess.check_output(['git', 'config', 'user.name'], stderr=subprocess.STDOUT)
            except subprocess.CalledProcessError:
                # If not set, configure a default identity for the action
                subprocess.check_call(['git', 'config', '--global', 'user.name', 'GitHub Actions'])
                subprocess.check_call(['git', 'config', '--global', 'user.email', 'github-actions@github.com'])
                print("Configured default Git identity for operations")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("Failed to set up Git identity")
            return False
    
    def configure_safe_directory(self):
        """Configure the workspace as a safe directory."""
        try:
            subprocess.check_call(['git', 'config', '--global', '--add', 'safe.directory', self.workspace_path])
            return True
        except subprocess.CalledProcessError:
            print(f"Failed to add {self.workspace_path} as safe directory")
            return False

class GitValidator:
    def is_valid_commit_message(self, message: str) -> bool:
        """Validate a commit message."""
        if not message or not message.strip():
            return False
        return True
    
    def is_valid_tag_name(self, tag_name: str) -> bool:
        """Validate a Git tag name."""
        if not tag_name:
            return False
        if tag_name.startswith('-'):
            return False
        if '..' in tag_name:
            return False
        invalid_chars = r'[\s~^:?*[\]\\]'
        if re.search(invalid_chars, tag_name):
            return False
        return True
    
    def pattern_to_regex(self, pattern: str) -> Pattern:
        """Convert a glob pattern to regex."""
        regex = re.escape(pattern)
        regex = regex.replace('\\*', '.*').replace('\\?', '.')
        regex = f'^{regex}$'
        return re.compile(regex)

class GitErrors:
    def handle_git_error(self, error, context=None):
        """Handle general Git errors."""
        if context:
            print(f"Error in {context}: {error}")
        else:
            print(f"Git error: {error}")
        return str(error)
    
    def handle_commit_error(self, error, action, message=None):
        """Handle commit-related errors."""
        # To maintain compatibility with the test suite
        if message:
            truncated_message = message[:50] + "..." if len(message) > 50 else message
            error_msg = f"Error {action} commit '{truncated_message}': {error}"
            print(error_msg)
            # For test_handle_error_output_formatting test
            return error_msg
        else:
            print(f"Error {action} commit: {error}")
            print("You may need to resolve conflicts manually if they exist.")
            # For test_handle_commit_error_no_message test
            return str(error)
    
    def handle_tag_error(self, error, action, tag):
        """Handle tag-related errors."""
        print(f"Error {action} tag {tag}: {error}")
        return str(error)
    
    def handle_push_error(self, error, ref):
        """Handle push-related errors."""
        print(f"Error pushing {ref}: {error}")
        return str(error)