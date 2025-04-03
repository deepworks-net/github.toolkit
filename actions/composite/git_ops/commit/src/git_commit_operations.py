#!/usr/bin/env python3

import os
import sys
import subprocess
from typing import Optional, Dict, List, Union

class GitCommitOperations:
    """Handles atomic Git commit operations."""
    
    def __init__(self):
        self._configure_git()
    
    def _configure_git(self) -> None:
        """Configure git for safe directory operations."""
        try:
            subprocess.check_call(['git', 'config', '--global', '--add', 'safe.directory', '/github/workspace'])
        except subprocess.CalledProcessError as e:
            print(f"Error configuring git: {e}")
            sys.exit(1)
    
    def create_commit(self, message: str, files: Optional[List[str]] = None, 
                    all_changes: bool = False, amend: bool = False) -> bool:
        """
        Create a new git commit.
        
        Args:
            message: The commit message
            files: Specific files to commit (optional)
            all_changes: Whether to commit all changes
            amend: Whether to amend the previous commit
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Stage files if specified
            if files:
                for file in files:
                    subprocess.check_call(['git', 'add', file])
            elif all_changes:
                subprocess.check_call(['git', 'add', '--all'])
            
            # Create commit
            cmd = ['git', 'commit']
            if amend:
                cmd.append('--amend')
            cmd.extend(['-m', message])
            
            subprocess.check_call(cmd)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error creating commit: {e}")
            return False
            
    def get_commit_info(self, commit_id: str = 'HEAD') -> Dict[str, str]:
        """
        Get information about a specific commit.
        
        Args:
            commit_id: The commit ID or reference
            
        Returns:
            dict: Commit information
        """
        try:
            # Get commit info
            format_str = '%H%n%an%n%ae%n%at%n%s'
            output = subprocess.check_output(
                ['git', 'show', '-s', f'--format={format_str}', commit_id], 
                text=True
            ).strip().split('\n')
            
            if len(output) >= 5:
                return {
                    'hash': output[0],
                    'author': output[1],
                    'email': output[2],
                    'date': output[3],
                    'message': output[4]
                }
            return {}
        except subprocess.CalledProcessError as e:
            print(f"Error getting commit info: {e}")
            return {}
            
    def revert_commit(self, commit_id: str, no_edit: bool = True) -> bool:
        """
        Revert a specific commit.
        
        Args:
            commit_id: The commit ID to revert
            no_edit: Whether to skip edit of commit message
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            cmd = ['git', 'revert', commit_id]
            if no_edit:
                cmd.append('--no-edit')
            
            subprocess.check_call(cmd)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error reverting commit {commit_id}: {e}")
            return False
            
    def list_commits(self, max_count: int = 10, format_string: str = '%h %s') -> List[str]:
        """
        List recent commits.
        
        Args:
            max_count: Maximum number of commits to list
            format_string: Format string for output
            
        Returns:
            list: List of formatted commit strings
        """
        try:
            output = subprocess.check_output(
                ['git', 'log', f'--format={format_string}', f'-n{max_count}'], 
                text=True
            )
            return output.strip().split('\n') if output.strip() else []
        except subprocess.CalledProcessError as e:
            print(f"Error listing commits: {e}")
            return []

def main():
    """Main entry point for the action."""
    commit_ops = GitCommitOperations()
    
    # Get inputs
    action = os.environ.get('INPUT_ACTION')
    message = os.environ.get('INPUT_MESSAGE')
    files_input = os.environ.get('INPUT_FILES', '')
    files = files_input.split(',') if files_input else None
    all_changes = os.environ.get('INPUT_ALL', 'false').lower() == 'true'
    amend = os.environ.get('INPUT_AMEND', 'false').lower() == 'true'
    commit_id = os.environ.get('INPUT_COMMIT_ID', 'HEAD')
    no_edit = os.environ.get('INPUT_NO_EDIT', 'true').lower() == 'true'
    max_count = int(os.environ.get('INPUT_MAX_COUNT', '10'))
    format_string = os.environ.get('INPUT_FORMAT', '%h %s')
    
    result = False
    output = None
    
    # Execute requested operation
    if action == 'create':
        result = commit_ops.create_commit(message, files, all_changes, amend)
    elif action == 'info':
        output = commit_ops.get_commit_info(commit_id)
        result = bool(output)
    elif action == 'revert':
        result = commit_ops.revert_commit(commit_id, no_edit)
    elif action == 'list':
        output = commit_ops.list_commits(max_count, format_string)
        result = True
    else:
        print(f"Invalid action: {action}")
        sys.exit(1)
    
    # Set output
    if action == 'info' and output:
        for key, value in output.items():
            print(f"::set-output name={key}::{value}")
    elif action == 'list' and output:
        print(f"::set-output name=commits::{','.join(output)}")
    
    if not result:
        sys.exit(1)

if __name__ == "__main__":
    main()