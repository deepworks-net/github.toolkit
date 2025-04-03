#!/usr/bin/env python3

import os
import sys
import subprocess
from typing import Optional, Dict, Union

class GitBranchOperations:
    """Handles atomic Git branch operations."""
    
    def __init__(self):
        self._configure_git()
    
    def _configure_git(self) -> None:
        """Configure git for safe directory operations."""
        try:
            subprocess.check_call(['git', 'config', '--global', '--add', 'safe.directory', '/github/workspace'])
        except subprocess.CalledProcessError as e:
            print(f"Error configuring git: {e}")
            sys.exit(1)
    
    def create_branch(self, branch_name: str, start_point: Optional[str] = None) -> bool:
        """
        Create a new git branch.
        
        Args:
            branch_name: The name of the branch to create
            start_point: Optional reference to start from
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            cmd = ['git', 'branch', branch_name]
            if start_point:
                cmd.append(start_point)
            subprocess.check_call(cmd)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error creating branch {branch_name}: {e}")
            return False
            
    def delete_branch(self, branch_name: str, force: bool = False, remote: bool = False) -> bool:
        """
        Delete a git branch locally and optionally from remote.
        
        Args:
            branch_name: The name of the branch to delete
            force: Whether to force delete
            remote: Whether to also delete from remote
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Delete local branch
            delete_flag = '-D' if force else '-d'
            subprocess.check_call(['git', 'branch', delete_flag, branch_name])
            
            # Delete remote branch if requested
            if remote:
                subprocess.check_call(['git', 'push', 'origin', f'--delete', branch_name])
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error deleting branch {branch_name}: {e}")
            return False
            
    def checkout_branch(self, branch_name: str, create: bool = False) -> bool:
        """
        Checkout a branch, creating it if requested.
        
        Args:
            branch_name: The name of the branch
            create: Whether to create the branch if it doesn't exist
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            cmd = ['git', 'checkout']
            if create:
                cmd.append('-b')
            cmd.append(branch_name)
            subprocess.check_call(cmd)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error checking out branch {branch_name}: {e}")
            return False
            
    def list_branches(self, all_branches: bool = False, remote: bool = False) -> list:
        """
        List branches.
        
        Args:
            all_branches: Include all branches
            remote: Include remote branches
            
        Returns:
            list: List of branch names
        """
        try:
            cmd = ['git', 'branch']
            if all_branches:
                cmd.append('--all')
            if remote:
                cmd.append('-r')
            output = subprocess.check_output(cmd, text=True)
            # Clean branch names (remove asterisk and whitespace)
            branches = []
            for line in output.strip().split('\n'):
                if line:
                    branch = line.strip()
                    if branch.startswith('*'):
                        branch = branch[1:].strip()
                    branches.append(branch)
            return branches
        except subprocess.CalledProcessError as e:
            print(f"Error listing branches: {e}")
            return []

def main():
    """Main entry point for the action."""
    branch_ops = GitBranchOperations()
    
    # Get inputs
    action = os.environ.get('INPUT_ACTION')
    branch_name = os.environ.get('INPUT_BRANCH_NAME')
    start_point = os.environ.get('INPUT_START_POINT')
    force = os.environ.get('INPUT_FORCE', 'false').lower() == 'true'
    remote = os.environ.get('INPUT_REMOTE', 'false').lower() == 'true'
    create = os.environ.get('INPUT_CREATE', 'false').lower() == 'true'
    all_branches = os.environ.get('INPUT_ALL', 'false').lower() == 'true'
    
    result = False
    output = None
    
    # Execute requested operation
    if action == 'create':
        result = branch_ops.create_branch(branch_name, start_point)
    elif action == 'delete':
        result = branch_ops.delete_branch(branch_name, force, remote)
    elif action == 'checkout':
        result = branch_ops.checkout_branch(branch_name, create)
    elif action == 'list':
        output = branch_ops.list_branches(all_branches, remote)
        result = True
    else:
        print(f"Invalid action: {action}")
        sys.exit(1)
    
    # Set output
    if output is not None:
        print(f"::set-output name=branches::{','.join(output)}")
    
    if not result:
        sys.exit(1)

if __name__ == "__main__":
    main()