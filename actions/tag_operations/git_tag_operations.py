#!/usr/bin/env python3

import os
import sys
import subprocess
from typing import Optional, Dict, Union

class GitTagOperations:
    """Handles atomic Git tag operations."""
    
    def __init__(self):
        self._configure_git()
    
    def _configure_git(self) -> None:
        """Configure git for safe directory operations."""
        try:
            subprocess.check_call(['git', 'config', '--global', '--add', 'safe.directory', '/github/workspace'])
        except subprocess.CalledProcessError as e:
            print(f"Error configuring git: {e}")
            sys.exit(1)
    
    def create_tag(self, tag_name: str, message: Optional[str] = None) -> bool:
        """
        Create a new git tag.
        
        Args:
            tag_name: The name of the tag to create
            message: Optional message for annotated tag
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if message:
                subprocess.check_call(['git', 'tag', '-a', tag_name, '-m', message])
            else:
                subprocess.check_call(['git', 'tag', tag_name])
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error creating tag {tag_name}: {e}")
            return False
            
    def delete_tag(self, tag_name: str, remote: bool = False) -> bool:
        """
        Delete a git tag locally and optionally from remote.
        
        Args:
            tag_name: The name of the tag to delete
            remote: Whether to also delete from remote
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Delete local tag
            subprocess.check_call(['git', 'tag', '-d', tag_name])
            
            # Delete remote tag if requested
            if remote:
                subprocess.check_call(['git', 'push', 'origin', f':refs/tags/{tag_name}'])
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error deleting tag {tag_name}: {e}")
            return False
            
    def push_tag(self, tag_name: str) -> bool:
        """
        Push a specific tag to remote.
        
        Args:
            tag_name: The name of the tag to push
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            subprocess.check_call(['git', 'push', 'origin', f'refs/tags/{tag_name}'])
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error pushing tag {tag_name}: {e}")
            return False
            
    def list_tags(self, pattern: Optional[str] = None) -> list:
        """
        List all tags, optionally filtered by pattern.
        
        Args:
            pattern: Optional pattern to filter tags
            
        Returns:
            list: List of tag names
        """
        try:
            cmd = ['git', 'tag']
            if pattern:
                cmd.extend(['-l', pattern])
            output = subprocess.check_output(cmd, text=True)
            return output.strip().split('\n') if output.strip() else []
        except subprocess.CalledProcessError as e:
            print(f"Error listing tags: {e}")
            return []

def main():
    """Main entry point for the action."""
    tag_ops = GitTagOperations()
    
    # Get inputs
    action = os.environ.get('INPUT_ACTION')
    tag_name = os.environ.get('INPUT_TAG_NAME')
    message = os.environ.get('INPUT_MESSAGE')
    remote = os.environ.get('INPUT_REMOTE', 'false').lower() == 'true'
    pattern = os.environ.get('INPUT_PATTERN')
    
    result = False
    output = None
    
    # Execute requested operation
    if action == 'create':
        result = tag_ops.create_tag(tag_name, message)
        if result and remote:
            result = tag_ops.push_tag(tag_name)
    elif action == 'delete':
        result = tag_ops.delete_tag(tag_name, remote)
    elif action == 'push':
        result = tag_ops.push_tag(tag_name)
    elif action == 'list':
        output = tag_ops.list_tags(pattern)
        result = True
    else:
        print(f"Invalid action: {action}")
        sys.exit(1)
    
    # Set output
    if output is not None:
        print(f"::set-output name=tags::{','.join(output)}")
    
    if not result:
        sys.exit(1)

if __name__ == "__main__":
    main()